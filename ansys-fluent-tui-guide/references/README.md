# ANSYS Fluent TUI Guide Skill - README

## 概述

这是一个全面的 ANSYS Fluent 文本用户界面 (TUI) 命令指导 Skill。它帮助用户查询、理解和正确构建 Fluent TUI 命令，用于网格生成、CFD 求解和后处理工作流。

## Skill 包含内容

### 主要文件

1. **SKILL.md** - Skill 的核心指导文档
   - Skill 的功能和使用时机
   - TUI 基础知识
   - 两种主要模式（网格模式和求解模式）
   - 常见工作流
   - 命令类别参考

2. **references/ANSYS_Fluent_TUI_Complete_Reference.md** - 完整的 TUI 命令参考
   - 从官方 ANSYS Fluent 2024 R2 文档提取
   - 包括 300+ 个 TUI 命令
   - 详细的命令分类和语法说明

3. **references/QUICK_START_CN.md** - 中文快速开始指南
   - TUI 基础
   - 常见工作流示例
   - 如何使用本 Skill
   - 命令参数类型

4. **references/COMMAND_QUICK_REFERENCE.md** - 英文命令快速参考
   - 网格模式命令速查表
   - 求解模式命令速查表
   - 常见命令缩写
   - 数据类型参考

### 脚本

- **scripts/fluent_tui_helper.py** - Python 辅助工具
  - 命令查询功能
  - 命令验证功能
  - 命令建议功能
  - 命令缩写生成

### 测试用例

- **evals/evals.json** - 5 个测试用例
  - 测试命令查询
  - 测试工作流构建
  - 测试命令验证
  - 测试自动化脚本创建

## 如何使用本 Skill

### 场景 1：查询特定命令

**用户问题：**
"我需要在 Fluent 中设置网格大小为 0.1，应该使用什么命令？"

**Skill 响应会包括：**
- 正确的命令：`/mesh/size 0.1`
- 语法解释
- 实际使用示例
- 相关的其他命令

### 场景 2：构建工作流

**用户问题：**
"从导入网格到运行 CFD 模拟，完整的步骤是什么？"

**Skill 响应会包括：**
- 按顺序的完整命令序列
- 每个步骤的说明
- 可复制粘贴的脚本
- 参数说明和可选项

### 场景 3：验证命令

**用户问题：**
"这些命令对吗？/mesh/size 0.5; /mesh/check; /report/mesh-statistics"

**Skill 响应会：**
- 检查每个命令的语法
- 指出任何问题
- 验证命令的逻辑顺序
- 建议改进

### 场景 4：构建自动化脚本

**用户问题：**
"我想创建一个 Fluent 脚本文件来自动运行完整的模拟，包括网格导入、物理设置、迭代求解和结果保存"

**Skill 响应会：**
- 提供完整的 .jou 脚本
- 解释每一行的含义
- 说明如何执行脚本
- 提供参数化示例

## TUI 命令体系

### 两种主要模式

#### 1. 网格模式（Meshing Mode）
用于网格生成和管理，包括 13 个命令类别：
- boundary - 边界操作
- cad-assemblies - CAD 导入
- diagnostics - 诊断工具
- display - 显示控制
- file - 文件 I/O
- material-point - 材料点
- mesh - 网格操作
- objects - 对象网格法
- parallel - 并行处理
- preferences - 偏好设置
- report - 报告工具
- scoped-sizing - 局部网格控制
- size-functions - 网格大小函数

#### 2. 求解模式（Solution Mode）
用于 CFD 求解和后处理，包括 15 个命令类别：
- adjoint - 伴随求解器
- define - 物理定义
- display - 结果显示
- file - 文件操作
- mesh - 网格操作
- parallel - 并行求解
- plot - 绘图工具
- preferences - 求解偏好
- report - 报告和监控
- server - 服务器配置
- solve - 求解控制
- surface - 表面操作
- turbo-workflow - 涡轮机械工作流
- turbo-post - 涡轮机械后处理
- views - 视图管理

## 命令基础

### 命令格式

```
/menu/submenu/command [arguments]
```

### 命令缩写

命令可以缩写到最小的唯一字符：
```
/mesh/size           →  m/s
/file/read-case      →  f/r
/solve/iterate       →  s/i
/define/materials    →  d/m
```

### 数据类型

- **数字**：整数或小数
- **字符串**：文本，包含空格时需要加引号
- **符号**：预定义的关键字
- **列表**：括号中的多个值
- **文件路径**：相对或绝对路径
- **布尔值**：yes/no 或 true/false

## 常见工作流

### 工作流 1：网格导入和检查
```
/file/read-case "mesh.cas"
/mesh/size 0.5
/mesh/check
/report/mesh-statistics
```

### 工作流 2：完整的 CFD 模拟
```
/file/read-case "mesh.cas"
/define/models/turbulence spalart-allmaras yes
/define/materials/fluid water
/define/boundary-conditions/inlet velocity-inlet
/define/boundary-conditions/inlet/velocity 5.0
/solve/initialize/initialize-flow
/solve/iterate 500
/display/contour velocity-magnitude
/file/write-case "results.cas"
```

## 参考文档结构

```
ansys-fluent-tui-guide/
├── SKILL.md                                    # 主要 Skill 文档
├── references/
│   ├── ANSYS_Fluent_TUI_Complete_Reference.md # 完整参考（从官方文档提取）
│   ├── QUICK_START_CN.md                      # 中文快速开始
│   ├── COMMAND_QUICK_REFERENCE.md             # 命令快速参考
│   └── command_index.json                     # 命令索引
├── scripts/
│   └── fluent_tui_helper.py                   # Python 辅助工具
└── evals/
    └── evals.json                             # 测试用例
```

## 文档来源

- **ANSYS Fluent 版本**：2024 R2
- **文档提取日期**：2026-06-10
- **来源 URL**：https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v242/en/flu_tcl/flu_tcl.html

## 特点

✅ **完整性**：包括 300+ 个 TUI 命令  
✅ **分类清晰**：按模式和功能分类  
✅ **实用示例**：每个命令都有实际使用示例  
✅ **工作流指导**：提供常见模拟工作流  
✅ **多语言支持**：包括中英文文档  
✅ **快速查询**：提供速查表和缩写  
✅ **脚本支持**：帮助创建自动化脚本  

## 使用提示

1. **快速查询命令**：使用缩写可以加速输入
2. **获取帮助**：在 Fluent 中输入 `command?` 获得实时帮助
3. **保存脚本**：将命令保存为 .jou 文件实现自动化
4. **链接命令**：使用分号分隔符链接多个命令
5. **注释脚本**：在 .jou 文件中用分号开头的行作为注释

## 获取帮助

如需帮助，你可以：
1. 查看相应的快速参考文档
2. 使用 Skill 查询特定命令
3. 参考完整的命令参考手册
4. 在 Fluent 中使用内置帮助系统

---

**最后更新**：2026-06-10  
**Skill 版本**：1.0  
**支持版本**：ANSYS Fluent 2024 R2+
