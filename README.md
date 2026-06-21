# ANSYS MCP Server

**❗本项目目前处于测试阶段**

ANSYS MCP Server 是一个基于 Model Context Protocol (MCP) 的服务器，用于驱动 ANSYS 系列仿真软件，包括 Fluent、Mechanical 和 Geometry。

内置 **[ansys-fluent-tui-guide](./ansys-fluent-tui-guide/)** Skill，自动将每个 MCP 操作映射为对应的 TUI 命令，并生成可复现的 `.jou` 脚本。

## 项目结构

```
mcp/
├── server.py                           ← MCP 服务器主程序
├── requirements.txt
├── .mcp.json.example                   ← MCP 配置文件模板
├── scripts/
│   └── mechanical_start_grpc.py        ← Mechanical gRPC 启动脚本
└── ansys-fluent-tui-guide/            ← TUI 命令指导 Skill
    ├── SKILL.md                        ← Skill 核心定义
    ├── references/                     ← 300+ TUI 命令参考文档
    │   ├── MCP_TUI_MAPPING.md          ← MCP ↔ TUI 完整映射表
    │   └── ANSYS_Fluent_TUI_Complete_Reference.md
    └── scripts/
        └── mcp_tui_auto_mapper.py      ← 自动映射器（已集成到 server.py）
```

## 功能特性

### 🔗 MCP + Skill 联动（核心特性）

每次调用 Fluent MCP 工具时，自动：

| 步骤 | 行为 |
|------|------|
| ① 执行操作 | MCP 工具执行实际的 ANSYS 操作 |
| ② TUI 映射 | 自动映射到等效 TUI 命令 |
| ③ 脚本累积 | 记录操作序列，可随时导出 `.jou` 脚本 |

**新增 MCP 工具：**

| 工具 | 功能 |
|------|------|
| `fluent_get_script` | 获取当前累积的完整 `.jou` 脚本 |
| `fluent_get_mapping_report` | 获取 MCP→TUI 完整映射报告 |
| `fluent_reset_mapper` | 清除映射历史（开始新的工作流） |

### Fluent (CFD) — 19 个工具
- 启动/连接 Fluent solver
- 加载 case/mesh 文件
- 设置求解器参数（湍流模型：laminar / k-epsilon / k-omega / SST / Spalart-Allmaras）
- 设置边界条件和材料
- 初始化流场、迭代计算
- 获取残差值
- 保存 case/data
- 执行 TUI 命令
- 加载和管理 UDF
- **MCP→TUI 自动映射** + 脚本生成

### Mechanical (结构分析) — 11 个工具
- 启动/连接 Mechanical（支持连接已运行的实例）
- 导入几何文件
- 分配材料
- 划分网格
- 施加载荷和约束
- 执行求解
- 提取结果（变形、应力、应变）
- 执行 IronPython 脚本

> **提示：** 连接已运行的 Mechanical 实例时，需要先在 Mechanical 中启动 gRPC 服务器。详见 [辅助脚本](#辅助脚本) 章节。

### Geometry (几何建模) — 10 个工具
- 启动 Geometry 建模器
- 创建几何设计
- 创建基本几何体（方块、圆柱、球体）
- 导入/导出 CAD 文件

## 安装

### 1. 创建虚拟环境

```bash
python -m venv .venv
```

### 2. 激活虚拟环境

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

### Claude Code / Claude Desktop 配置

复制 `.mcp.json.example` 为 `.mcp.json`，并修改以下配置：

```json
{
  "mcpServers": {
    "ansys-mcp": {
      "command": "path/to/.venv/Scripts/python.exe",
      "args": ["-u", "path/to/server.py"],
      "env": {
        "AWP_ROOT242": "path/to/ANSYS/Inc/v242",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### 环境变量

- `AWP_ROOT242`: ANSYS 安装路径（如 `C:\Program Files\ANSYS Inc\v242`）

## 使用方法

启动 MCP 服务器后，可以通过 Claude Code 或其他 MCP 客户端调用以下工具：

### Fluent 工具

| 工具 | 说明 |
|------|------|
| `fluent_launch` | 启动或连接 Fluent |
| `fluent_read_case` | 加载算例文件 |
| `fluent_read_mesh` | 加载网格文件 |
| `fluent_set_solver` | 设置求解器参数 |
| `fluent_set_boundary` | 设置边界条件 |
| `fluent_set_material` | 设置材料 |
| `fluent_initialize` | 初始化流场 |
| `fluent_iterate` | 迭代计算 |
| `fluent_get_residuals` | 获取残差 |
| `fluent_save` | 保存文件 |
| `fluent_tui` | 执行 TUI 命令 |
| `fluent_load_udf` | 加载 UDF |
| `fluent_hook_udf` | 挂钩 UDF 到边界 |
| `fluent_list_udfs` | 列出 UDF 状态 |
| `fluent_status` | 查看状态 |
| `fluent_exit` | 关闭 Fluent |
| `fluent_get_script` | 🆕 导出累积的 .jou 脚本 |
| `fluent_get_mapping_report` | 🆕 获取 MCP→TUI 映射报告 |
| `fluent_reset_mapper` | 🆕 重置映射历史 |

### Mechanical 工具

| 工具 | 说明 |
|------|------|
| `mechanical_launch` | 启动或连接 Mechanical |
| `mechanical_import` | 导入几何 |
| `mechanical_set_material` | 分配材料 |
| `mechanical_mesh` | 划分网格 |
| `mechanical_apply_load` | 施加载荷 |
| `mechanical_solve` | 执行求解 |
| `mechanical_get_result` | 提取结果 |
| `mechanical_list` | 列出几何体/Named Selections |
| `mechanical_script` | 执行脚本 |
| `mechanical_status` | 查看状态 |
| `mechanical_exit` | 关闭 Mechanical |

### Geometry 工具

| 工具 | 说明 |
|------|------|
| `geometry_launch` | 启动 Geometry 建模器 |
| `geometry_create_design` | 创建设计 |
| `geometry_create_block` | 创建方块 |
| `geometry_create_cylinder` | 创建圆柱 |
| `geometry_create_sphere` | 创建球体 |
| `geometry_export` | 导出几何 |
| `geometry_list_bodies` | 列出几何体 |
| `geometry_import_file` | 导入 CAD 文件 |
| `geometry_status` | 查看状态 |
| `geometry_close` | 关闭建模器 |

## MCP + Skill 联动示例

```
用户: 用 ANSYS 做一个 CFD 模拟，入口速度 10 m/s，SA 湍流模型，迭代 1000 步

→ fluent_launch()                         # 启动 Fluent
→ fluent_read_case("mesh.cas")            # 加载网格
→ fluent_set_solver(viscous="spalart-allmaras")  # 设置湍流模型
→ fluent_set_boundary(zone="inlet", velocity=10) # 设置边界
→ fluent_initialize()                     # 初始化
→ fluent_iterate(1000)                    # 求解

→ fluent_get_script()                     # 导出脚本

自动生成的 .jou 脚本：
  /file/read-case "mesh.cas"
  /define/models/turbulence spalart-allmaras yes
  /define/boundary-conditions/inlet velocity-inlet
  /define/boundary-conditions/inlet/velocity 10.0
  /solve/initialize/initialize-flow
  /solve/iterate 1000
```

> 📖 Skill 完整文档：`@ansys-fluent-tui-guide`，300+ TUI 命令参考。

## 注意事项

1. 需要安装 ANSYS 2024 R2 (v242) 或更高版本
2. Fluent、Mechanical 和 Geometry 需要分别启动
3. 首次使用时，ANSYS 可能需要较长时间启动
4. 确保 ANSYS 许可证有效

## 辅助脚本

`scripts/` 目录包含辅助脚本，用于配置和启动 ANSYS 服务。

### mechanical_start_grpc.py

**功能：** 在 Ansys Mechanical 中启动 gRPC 服务器并获取端口号。

**使用场景：** 当需要连接到已运行的 Mechanical 实例时（而非启动新实例），需要先在 Mechanical 中启动 gRPC 服务器。

**使用方法：**

1. **打开 Ansys Mechanical**
   - 启动 Ansys Mechanical 应用程序
   - 打开或创建一个项目

2. **打开 Scripting 控制台**
   - 在 Mechanical 中，点击菜单：`View` → `Scripting`
   - 或使用快捷键打开脚本编辑器

3. **执行脚本**
   - 将 `scripts/mechanical_start_grpc.py` 中的内容复制到脚本编辑器
   - 执行脚本
   - 记录输出的端口号（例如：`Mechanical gRPC Server started on port: 50052`）

4. **连接 MCP Server**
   - 使用 Claude Code 或其他 MCP 客户端
   - 调用 `mechanical_launch` 工具并指定端口：
     ```json
     {
       "port": 50052
     }
     ```

**脚本内容：**
```python
port_number = Ansys.ACT.Mechanical.MechanicalAPI.Instance.ApplicationAPI.StartGrpcServer()
print(f"Mechanical gRPC Server started on port: {port_number}")
print(f"Use this port number to connect via: mechanical_launch(port={port_number})")
```

**注意事项：**
- 该脚本需要在 Ansys Mechanical 内部执行，不能在外部 Python 环境中运行
- 端口号由系统自动分配，每次启动可能不同
- 确保防火墙允许该端口的通信
- gRPC 服务器启动后会一直运行，直到 Mechanical 关闭

## 许可证

MIT License
