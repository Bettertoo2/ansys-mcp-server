# ANSYS Fluent TUI Guide Skill - 快速开始指南

## 什么是 TUI？

Text User Interface (TUI) 是 ANSYS Fluent 的命令行接口，允许你通过文本命令控制所有求解器和预处理功能。使用 TUI 可以：

- 自动化重复的模拟任务
- 创建批处理脚本（.jou 文件）
- 集成到第三方工作流中
- 进行高效的参数研究

## 命令基础

### 命令格式

所有 TUI 命令遵循层级结构：

```
/menu/submenu/command [arguments]
```

### 简写

命令可以简写到最小的唯一字符：

```
/mesh/size           →  /m/s  或  m/s
/solve/iterate       →  /s/i  或  s/i
/file/read-case      →  /f/r  或  f/r
/define/materials    →  /d/m  或  d/m
```

## 两种主要模式

### 1. 网格模式（Meshing Mode）

处理网格生成和管理的命令。常用命令：

| 任务 | 命令 |
|------|------|
| 导入网格文件 | `/file/read-case "mesh.cas"` |
| 设置网格大小 | `/mesh/size 0.5` |
| 创建边界网格 | `/mesh/create-boundary` |
| 创建体积网格 | `/mesh/create-volume` |
| 检查网格质量 | `/diagnostics/check-mesh-quality` |
| 生成网格统计 | `/report/mesh-statistics` |
| 导出网格 | `/file/export-mesh "output.msh"` |

### 2. 求解模式（Solution Mode）

处理物理定义、边界条件和求解的命令。常用命令：

| 任务 | 命令 |
|------|------|
| 读取案例文件 | `/file/read-case "mesh.cas"` |
| 定义流体材料 | `/define/materials/fluid water` |
| 设置湍流模型 | `/define/models/turbulence spalart-allmaras yes` |
| 设置入口条件 | `/define/boundary-conditions/inlet velocity-inlet` |
| 设置速度 | `/define/boundary-conditions/inlet/velocity 5.0` |
| 初始化流场 | `/solve/initialize/initialize-flow` |
| 运行迭代 | `/solve/iterate 1000` |
| 显示结果 | `/display/contour velocity-magnitude` |
| 保存结果 | `/file/write-case "results.cas"` |

## 常见工作流

### 工作流 1：网格设置和检查

```
# 导入网格
/file/read-case "mesh.cas"

# 设置网格大小
/mesh/size 0.5

# 创建网格（如果需要）
/mesh/create-boundary
/mesh/create-volume

# 检查网格
/diagnostics/check-mesh-quality
/report/mesh-statistics

# 导出网格
/file/export-mesh "output.msh"
```

### 工作流 2：完整的 CFD 模拟

```
# 读取网格
/file/read-case "mesh.cas"

# 定义物理
/define/models/turbulence spalart-allmaras yes
/define/materials/fluid water
/define/operating-conditions/pressure 101325

# 设置边界条件
/define/boundary-conditions/inlet velocity-inlet
/define/boundary-conditions/inlet/velocity 5.0
/define/boundary-conditions/inlet/temperature 300
/define/boundary-conditions/outlet pressure-outlet
/define/boundary-conditions/outlet/gauge-pressure 0

# 初始化
/solve/initialize/initialize-flow

# 运行求解器
/solve/iterate 500

# 显示结果
/display/contour velocity-magnitude
/plot/xy-plot convergence-history

# 保存结果
/file/write-case "results.cas"
/file/write-data "results.dat"
```

## 如何使用本 Skill

### 1. 查询特定命令

**问题示例：**
"我需要设置网格大小为 0.1，应该使用什么命令？"

**Skill 会：**
- 提供 `/mesh/size` 命令
- 解释语法和参数
- 给出 `/mesh/size 0.1` 的实际示例

### 2. 获取工作流帮助

**问题示例：**
"给我一个从导入网格到检查质量的完整步骤序列"

**Skill 会：**
- 提供按顺序的命令
- 解释每个命令的目的
- 提供可复制粘贴的命令序列

### 3. 验证命令语法

**问题示例：**
"这个命令对吗？/mesh/refine all 0.1"

**Skill 会：**
- 检查语法是否有效
- 指出任何潜在问题
- 建议改进或替代方案

### 4. 构建自动化脚本

**问题示例：**
"我想创建一个 Fluent 脚本来自动运行 100 次迭代，如何做？"

**Skill 会：**
- 提供完整的命令序列
- 解释如何保存为 .jou 文件
- 展示如何在 Fluent 中执行

## 命令参数类型

### 数字
```
/mesh/size 0.5
/solve/iterate 1000
```

### 字符串（如需要可加引号）
```
/file/read-case "my_mesh.cas"
/file/write-case "results/output.cas"
```

### 符号/关键字
```
/define/boundary-conditions/inlet velocity-inlet
/display/set-view top
```

### 列表
```
/boundary/boundary-conditions/copy (zone1 zone2 zone3)
/report/surface-integrals (outlet1 outlet2)
```

## 获取帮助

在 Fluent 中可以使用以下方式获取帮助：

```
command?           # 简要帮助
command??          # 详细帮助
/help command      # 另一种方式
```

## 保存为脚本文件

将命令保存到 `.jou` (journal) 文件中可以批量执行：

```
# example.jou
# 注释以分号开头
; 导入网格
/file/read-case "mesh.cas"

; 设置参数
/mesh/size 0.5

; 运行检查
/mesh/check
/report/mesh-statistics

; 保存结果
/file/write-case "output.cas"
```

执行脚本：
```bash
fluent 3d -i example.jou
```

## 需要更多帮助？

- 查看 **ANSYS_Fluent_TUI_Complete_Reference.md** 获取完整的命令参考
- 查看 **command_index.json** 获取所有可用的命令分类
- 在 Fluent 中使用 `command?` 获取实时帮助

---

**最后更新：** 2026-06-10  
**ANSYS Fluent 版本：** 2024 R2
