# MCP 服务器集成指南 - 自动 TUI 命令追踪

## 概述

`mcp_tui_auto_mapper.py` 是一个独立的 Python 模块，可以与 ANSYS MCP 服务器集成，在每个 MCP 工具调用时自动：

1. 记录 MCP 工具和参数
2. 映射到对应的 TUI 命令
3. 累积命令序列
4. 生成可执行的 .jou 脚本

## 集成到 server.py 的步骤

### 第一步：导入映射器

在 `E:\sci-program\mcp\server.py` 的顶部添加：

```python
# 在现有导入之后添加
import sys
from pathlib import Path

# 添加 Skill 脚本目录到路径
skill_scripts_path = Path("path/to/your/ansys-fluent-tui-guide/scripts")
sys.path.insert(0, str(skill_scripts_path))

from mcp_tui_auto_mapper import map_mcp_call, get_mapping_report, reset_mapper
```

### 第二步：在每个 Fluent 工具后添加映射

在 `server.py` 的 `@app.call_tool()` 中，对于每个 Fluent 工具调用，添加映射调用：

**示例 1：fluent_read_case**

```python
elif name == "fluent_read_case":
    if _fluent_session is None:
        result = "Fluent 未连接，请先执行 fluent_launch"
    else:
        s = _fluent_session
        s.file.read(file_type="case", file_name=os.path.abspath(arguments["file_path"]))
        result = f"已加载: {arguments['file_path']}"
        
        # ↓ 添加这一行
        map_result = map_mcp_call("fluent_read_case", arguments)
```

**示例 2：fluent_set_solver**

```python
elif name == "fluent_set_solver":
    changes = []
    if "viscous_model" in arguments:
        s.setup.models.viscous.model = arguments["viscous_model"]
        changes.append(f"湍流={arguments['viscous_model']}")
    if "energy" in arguments:
        s.setup.models.energy.enabled = arguments["energy"]
        changes.append(f"能量={'on' if arguments['energy'] else 'off'}")
    if "transient" in arguments:
        s.setup.general.time = "transient" if arguments["transient"] else "steady"
        changes.append(f"求解={'瞬态' if arguments['transient'] else '稳态'}")
    
    result = f"求解器: {', '.join(changes)}" if changes else "无变更"
    
    # ↓ 添加这行
    map_result = map_mcp_call("fluent_set_solver", arguments)
```

### 第三步：添加脚本查询工具（可选但推荐）

在 `server.py` 中添加两个新的工具定义：

```python
# 在 FLUENT_TOOLS 列表中添加
Tool(name="fluent_get_script", 
     description="获取当前 MCP 操作序列对应的 .jou 脚本",
     inputSchema={"type": "object", "properties": {}}),

Tool(name="fluent_get_mapping_report",
     description="获取 MCP 到 TUI 的完整映射报告",
     inputSchema={"type": "object", "properties": {}}),

Tool(name="fluent_reset_mapper",
     description="重置 TUI 映射器（清除历史记录）",
     inputSchema={"type": "object", "properties": {}}),
```

### 第四步：实现查询工具的处理

在 `@app.call_tool()` 中添加处理函数：

```python
elif name == "fluent_get_script":
    script = get_mapping_report()
    result = script

elif name == "fluent_get_mapping_report":
    report = get_mapping_report()
    result = report

elif name == "fluent_reset_mapper":
    reset_mapper()
    result = "✓ TUI 映射器已重置"
```

## 使用方式

### 在 Claude Code 中使用

#### 方式 1：获取脚本

```
我想用 MCP 执行一系列操作，然后获得对应的脚本。
@ansys-mcp
1. 启动 Fluent
2. 加载 mesh.cas
3. 设置 Spalart-Allmaras 湍流模型
然后获取脚本。

最后查询：
@ansys-mcp fluent_get_mapping_report
```

#### 方式 2：自动映射显示

当启用映射器后，每个 MCP 调用会自动返回 TUI 映射信息：

```
用户：用 MCP 设置网格大小为 0.1
↓
MCP 执行操作
↓ (同时)
自动返回：
✓ MCP → TUI Mapped
  MCP Tool: fluent_set_solver
  TUI Command: /mesh/size 0.1
```

## 映射器的工作流程

```
1. MCP 工具被调用
   ├─ fluent_set_solver(viscous_model="spalart-allmaras")
   
2. 函数执行
   ├─ MCP 实际执行操作
   ├─ 返回执行结果
   
3. 自动映射
   ├─ map_mcp_call() 被调用
   ├─ 查询 MAPPING_TABLE
   ├─ 生成 TUI 命令：/define/models/turbulence spalart-allmaras yes
   ├─ 存储到历史记录
   
4. 用户查询
   ├─ fluent_get_script() 获取完整脚本
   ├─ fluent_get_mapping_report() 获取完整报告
   
5. 输出
   ├─ .jou 脚本（可直接在 Fluent 执行）
   ├─ 映射报告（包括所有 MCP → TUI 映射）
```

## 映射表支持的工具

### 已实现映射

| MCP 工具 | 支持状态 | TUI 命令数 |
|---------|--------|----------|
| fluent_read_case | ✅ | 1 |
| fluent_read_mesh | ✅ | 1 |
| fluent_save | ✅ | 2 (case + data) |
| fluent_set_solver | ✅ | 3+ (turbulence/energy/time) |
| fluent_set_material | ✅ | 1 |
| fluent_set_boundary | ✅ | 2+ (zone + properties) |
| fluent_initialize | ✅ | 1 |
| fluent_iterate | ✅ | 1 |
| fluent_tui | ✅ | 1 (直接) |

### 可扩展的工具

通过编辑 `MAPPING_TABLE` 字典可以轻松添加新的映射：

```python
"new_fluent_tool": {
    "template": '/tui/command {param1} {param2}',
    "params_map": {"param1": "params_path", "param2": "other_param"},
    "description": "Description of what this does",
    "category": "category_name"
}
```

## 高级用法

### 自定义映射表

编辑 `mcp_tui_auto_mapper.py` 中的 `MAPPING_TABLE`：

```python
MAPPING_TABLE = {
    "your_tool": {
        "template": "/your/tui/command {arg}",
        "params_map": {"arg": "parameter_name"},
        "description": "Your description",
        "category": "your_category"
    }
}
```

### 导出为 JSON

```python
from mcp_tui_auto_mapper import _mapper_instance

json_data = _mapper_instance.export_to_json()
# 包含所有记录的命令和生成的脚本
```

### 编程使用

```python
from mcp_tui_auto_mapper import MCPToTUIMapper

mapper = MCPToTUIMapper()

# 映射单个调用
tui_cmd = mapper.map_mcp_to_tui("fluent_set_solver", 
                                {"viscous_model": "spalart-allmaras"})

# 生成脚本
script = mapper.generate_jou_script()

# 获取报告
report = mapper.get_mapping_report()
```

## 故障排查

### 问题 1：映射器未被触发

**症状：** 调用 MCP 工具后没有看到映射

**解决：**
1. 确认 `mcp_tui_auto_mapper.py` 已正确导入
2. 检查 `map_mcp_call()` 是否在每个工具后被调用
3. 确认工具名称与 MAPPING_TABLE 中的键匹配

### 问题 2：TUI 命令生成不正确

**症状：** 生成的 TUI 命令与预期不符

**解决：**
1. 检查 MAPPING_TABLE 中的模板和参数映射
2. 验证参数路径（如 `params.velocity` vs `velocity`）
3. 检查参数值是否正确传递

### 问题 3：脚本中有多余或缺失的命令

**症状：** 生成的 .jou 脚本不完整或有重复

**解决：**
1. 确认每个 MCP 工具调用都被映射
2. 检查是否调用了 `reset_mapper()` 清除历史
3. 验证映射表中是否有遗漏的工具

## 推荐使用模式

### 交互式工作流

```
用户: @ansys-mcp fluent_launch

MCP: ✓ Fluent 已启动
Auto-Mapper: 记录了启动操作

用户: @ansys-mcp fluent_read_case(file_path="mesh.cas")

MCP: ✓ 已加载 mesh.cas
Auto-Mapper: 
✓ MCP → TUI Mapped
  /file/read-case "mesh.cas"

用户: @ansys-fluent-tui-guide @ansys-mcp fluent_get_mapping_report

Claude: [返回完整报告和生成的 .jou 脚本]
```

### 批量自动化

```
用户: 给我一个完整的 CFD 模拟脚本

@ansys-mcp [执行一系列操作]
@ansys-fluent-tui-guide [自动映射和脚本生成]

结果: 完整的 .jou 脚本，可直接在 Fluent 执行
```

## 性能考虑

- **内存使用**：映射器在内存中保存命令历史。对于长时间运行的会话，可定期调用 `reset_mapper()`
- **映射速度**：映射是 O(1) 操作，不影响 MCP 工具的执行速度
- **脚本生成**：生成脚本是 O(n) 操作，其中 n 是命令数量

## 扩展可能性

1. **Mechanical 支持** - 添加 Mechanical IronPython 映射
2. **Geometry 支持** - 添加 Geometry 建模命令映射
3. **并行处理** - 支持并行会话的独立映射
4. **版本适配** - 为不同 ANSYS 版本维护不同的映射表
5. **IDE 集成** - 直接在 IDE 中显示映射结果

---

**文档版本：** 1.0  
**最后更新：** 2026-06-11  
**兼容性：** ANSYS MCP server.py + mcp_tui_auto_mapper.py
