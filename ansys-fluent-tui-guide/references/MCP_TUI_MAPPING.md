# MCP 工具到 TUI 命令的完整映射表

## Fluent MCP 工具 → TUI 命令映射

### 文件操作

| MCP 工具 | 参数 | 等价 TUI 命令 | 说明 |
|---------|------|-------------|------|
| `fluent_read_case` | `file_path="mesh.cas"` | `/file/read-case "mesh.cas"` | 读取案例文件 |
| `fluent_read_mesh` | `file_path="mesh.msh"` | `/file/read-mesh "mesh.msh"` | 读取网格文件 |
| `fluent_save` | `prefix="results"` | `/file/write-case "results.cas"` + `/file/write-data "results.dat"` | 保存案例和数据 |

### 求解器配置

| MCP 工具 | 参数 | 等价 TUI 命令 | 说明 |
|---------|------|-------------|------|
| `fluent_set_solver` | `viscous_model="spalart-allmaras"` | `/define/models/turbulence spalart-allmaras yes` | 设置湍流模型 |
| `fluent_set_solver` | `energy=true` | `/define/models/energy enable` | 启用能量方程 |
| `fluent_set_solver` | `transient=true` | `/define/general/time transient` | 设置瞬态求解 |

### 物理定义

| MCP 工具 | 参数 | 等价 TUI 命令 | 说明 |
|---------|------|-------------|------|
| `fluent_set_material` | `zone="fluid"`, `material="water"` | `/define/materials/fluid water` | 设置流体材料 |
| `fluent_set_material` | `zone="solid"`, `material="steel"` | `/define/materials/solid steel` | 设置固体材料 |

### 边界条件

| MCP 工具 | 参数 | 等价 TUI 命令 | 说明 |
|---------|------|-------------|------|
| `fluent_set_boundary` | `zone="inlet"`, `bc_type="velocity-inlet"`, `params={"velocity": 5.0}` | `/define/boundary-conditions/inlet velocity-inlet` + `/define/boundary-conditions/inlet/velocity 5.0` | 设置速度入口 |
| `fluent_set_boundary` | `zone="outlet"`, `bc_type="pressure-outlet"` | `/define/boundary-conditions/outlet pressure-outlet` | 设置压力出口 |
| `fluent_set_boundary` | `zone="wall"`, `bc_type="wall"` | `/define/boundary-conditions/wall no-slip` | 设置无滑移壁面 |

### 求解控制

| MCP 工具 | 参数 | 等价 TUI 命令 | 说明 |
|---------|------|-------------|------|
| `fluent_initialize` | `method="hybrid"` | `/solve/initialize/initialize-flow` | 初始化流场 |
| `fluent_iterate` | `iterations=500` | `/solve/iterate 500` | 运行 500 次迭代 |
| `fluent_get_residuals` | - | `/solve/monitors/residual` | 获取残差值 |

### 可视化和报告

| MCP 工具 | 参数 | 等价 TUI 命令 | 说明 |
|---------|------|-------------|------|
| 无直接工具 | - | `/display/contour velocity-magnitude` | 显示速度分布 |
| 无直接工具 | - | `/display/vector velocity` | 显示速度矢量 |
| 无直接工具 | - | `/plot/xy-plot convergence-history` | 绘制收敛历史 |

### UDF 操作

| MCP 工具 | 参数 | 等价 TUI 命令 | 说明 |
|---------|------|-------------|------|
| `fluent_load_udf` | `source_file="udf.c"` | `/file/read-udf "udf.c"` | 加载 UDF 源文件 |
| `fluent_hook_udf` | `zone_name="inlet"`, `profile_name="velocity_profile"` | `/define/boundary-conditions/inlet/udf-profile velocity_profile` | 挂钩 UDF 到边界 |

### TUI 直接执行

| MCP 工具 | 参数 | 说明 |
|---------|------|------|
| `fluent_tui` | `command="/mesh/size 0.5"` | 直接执行任意 TUI 命令 |

---

## Mechanical MCP 工具 → TUI/脚本命令映射

| MCP 工具 | 参数 | 等价操作 | 说明 |
|---------|------|--------|------|
| `mechanical_import` | `file_path="geometry.step"` | 导入几何文件 | 读取 STEP/IGES 文件 |
| `mechanical_set_material` | `body="Part1"`, `material="Steel"` | 分配材料属性 | 设置结构材料 |
| `mechanical_mesh` | `element_size=0.001` | 网格划分 | 生成有限元网格 |
| `mechanical_apply_load` | `load_type="force"`, `magnitude=100` | 施加载荷 | 添加力/位移/约束 |
| `mechanical_solve` | - | 求解分析 | 启动 FEA 求解器 |
| `mechanical_get_result` | `result_type="equivalent_stress"` | 提取结果 | 获取应力/应变/变形数据 |

---

## Geometry MCP 工具 → 建模操作映射

| MCP 工具 | 参数 | 等价操作 | 说明 |
|---------|------|--------|------|
| `geometry_launch` | - | 启动建模器 | 启动 Geometry 模块 |
| `geometry_create_design` | `name="MyDesign"` | 创建设计 | 新建几何设计 |
| `geometry_create_block` | `length=0.01`, `width=0.01`, `height=0.01` | 创建方块 | 基本几何体 |
| `geometry_create_cylinder` | `radius=0.005`, `height=0.01` | 创建圆柱 | 基本几何体 |
| `geometry_create_sphere` | `radius=0.005` | 创建球体 | 基本几何体 |
| `geometry_export` | `file_path="output.step"`, `format="step"` | 导出几何 | 保存为标准格式 |
| `geometry_import_file` | `file_path="cad.step"` | 导入 CAD | 读取外部几何 |

---

## 集成使用示例

### 示例 1: MCP + Skill 协同的完整工作流

```
用户输入: "用 ANSYS 设置一个 CFD 模拟"

步骤 1: MCP 启动 Fluent
  → MCP 工具: fluent_launch()
  → Skill 信息: Fluent TUI 基础知识

步骤 2: MCP 加载网格
  → MCP 工具: fluent_read_case("mesh.cas")
  → Skill 显示: /file/read-case "mesh.cas"

步骤 3: MCP 设置湍流模型
  → MCP 工具: fluent_set_solver(viscous_model="spalart-allmaras")
  → Skill 显示: /define/models/turbulence spalart-allmaras yes

步骤 4: MCP 设置边界条件
  → MCP 工具: fluent_set_boundary(zone="inlet", bc_type="velocity-inlet", params={"velocity": 5.0})
  → Skill 显示: 
    /define/boundary-conditions/inlet velocity-inlet
    /define/boundary-conditions/inlet/velocity 5.0

步骤 5: MCP 初始化求解
  → MCP 工具: fluent_initialize()
  → Skill 显示: /solve/initialize/initialize-flow

步骤 6: MCP 迭代计算
  → MCP 工具: fluent_iterate(iterations=500)
  → Skill 显示: /solve/iterate 500

最终: Skill 生成可保存的 .jou 脚本
  /file/read-case "mesh.cas"
  /define/models/turbulence spalart-allmaras yes
  /define/boundary-conditions/inlet velocity-inlet
  /define/boundary-conditions/inlet/velocity 5.0
  /solve/initialize/initialize-flow
  /solve/iterate 500
```

### 示例 2: 直接使用 TUI 命令

```
用户输入: "执行这个 TUI 命令: /mesh/size 0.1"

Skill 验证: ✓ 有效的命令语法
Skill 解释: 设置全局网格大小为 0.1 单位
Skill 建议: 相关命令：
  - /mesh/create-boundary (创建边界网格)
  - /mesh/create-volume (创建体积网格)
  - /mesh/check (检查网格有效性)
```

### 示例 3: 生成自动化脚本

```
用户输入: "使用 MCP 完成一个完整的 CFD 模拟，然后给我脚本"

流程:
1. MCP 执行所有操作
2. Skill 记录每个操作对应的 TUI 命令
3. Skill 生成完整的 .jou 脚本文件
4. 用户可以在任何 Fluent 环境重复执行

生成的脚本:
  ; Fluent CFD 模拟脚本 (由 ANSYS MCP + Skill 生成)
  /file/read-case "mesh.cas"
  /define/models/turbulence spalart-allmaras yes
  /define/materials/fluid water
  /define/boundary-conditions/inlet velocity-inlet
  /define/boundary-conditions/inlet/velocity 5.0
  /define/boundary-conditions/outlet pressure-outlet
  /solve/initialize/initialize-flow
  /solve/iterate 500
  /display/contour velocity-magnitude
  /file/write-case "results.cas"
```

---

## 在 Claude Code 中的使用

### 触发 MCP + Skill 协同

```
@ansys-fluent-tui-guide @ansys-mcp
我需要进行以下 CFD 模拟:
1. 导入网格 mesh.cas
2. 设置水作为流体
3. 使用 Spalart-Allmaras 湍流模型
4. 入口速度 10 m/s
5. 运行 1000 次迭代
6. 保存结果
```

### 只使用 Skill（无需 MCP）

```
@ansys-fluent-tui-guide
给我一个从导入网格到完成 CFD 模拟的完整 TUI 命令序列。
我想要生成一个可以在 Fluent 中直接运行的脚本。
```

### 验证 MCP 生成的操作

```
@ansys-fluent-tui-guide
我用 MCP 执行了以下操作:
- fluent_read_case("mesh.cas")
- fluent_set_solver(viscous_model="k-epsilon")
- fluent_set_boundary(zone="inlet", bc_type="velocity-inlet", params={"velocity": 5.0})

给我对应的 TUI 命令和等价的脚本。
```

---

## 快速参考

### MCP 工具最常用的 10 个

| # | MCP 工具 | 对应 TUI | 用途 |
|---|---------|---------|------|
| 1 | `fluent_launch` | 无 | 启动 Fluent 实例 |
| 2 | `fluent_read_case` | `/file/read-case` | 加载案例文件 |
| 3 | `fluent_set_solver` | `/define/models/turbulence` | 配置求解器 |
| 4 | `fluent_set_boundary` | `/define/boundary-conditions` | 设置边界条件 |
| 5 | `fluent_set_material` | `/define/materials` | 定义材料 |
| 6 | `fluent_initialize` | `/solve/initialize` | 初始化流场 |
| 7 | `fluent_iterate` | `/solve/iterate` | 运行迭代 |
| 8 | `fluent_save` | `/file/write-case/data` | 保存结果 |
| 9 | `fluent_tui` | 任意 TUI 命令 | 直接执行 TUI |
| 10 | `fluent_status` | 无 | 查看连接状态 |

---

**最后更新：** 2026-06-11  
**整合版本：** ansys-fluent-tui-guide v1.0 + ANSYS MCP v242
