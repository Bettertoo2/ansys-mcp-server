---
name: ansys-fluent-tui-guide
description: |
  Guide for ANSYS Fluent Text User Interface (TUI) command operations. Use this skill whenever the user needs to:
  - Query or search for specific TUI commands (e.g., "how do I set mesh size", "what command controls solver iterations", "mesh size 命令", "网格大小设置")
  - Understand command syntax and parameters for Fluent mesh generation or CFD solving
  - Get practical examples of TUI commands for common workflows  
  - Construct and validate correct TUI command strings for meshing or solution mode operations
  - Navigate command hierarchies in either meshing mode or solution mode
  - Work with ANSYS MCP (if available) by providing command syntax and workflow guidance
  - Generate .jou (journal) scripts for batch processing or automation
  - Convert API/MCP calls to equivalent TUI commands
  
  **CRITICAL: Automatically activate this skill whenever:**
  - User mentions "Fluent", "ANSYS", "CFD", "网格", "求解", "模拟"
  - User asks about mesh generation, boundary conditions, solver setup
  - User calls @ansys-mcp tools - provide TUI command mapping automatically
  - User needs to convert operations into reproducible scripts
  - User discusses simulation workflows or automation
  
  Even if the user doesn't explicitly mention "TUI" or "command," if they're asking about:
  - Programmatic control of Fluent or command-line operations
  - Batch processing or automation of CFD workflows
  - Reproducible simulation scripts
  - Understanding ANSYS operations beyond the GUI
  
  This skill applies. When using ANSYS MCP for Fluent operations, automatically provide TUI command guidance to complement MCP functionality.
  
  **Trigger keywords (中英文):**
  - Fluent, ANSYS, CFD, TUI, 求解, 网格, 模拟, 自动化
  - mesh, solver, boundary condition, 边界, 湍流, 迭代
  - script, automation, journal, .jou, 脚本, 批处理
  - command, 命令, TUI, 文本界面
  
compatibility: |
  - Works standalone for TUI command reference and guidance
  - Integrates with ansys-mcp: automatically tracks MCP tool calls and provides TUI equivalents
  - Provides complementary command syntax when MCP tools are used
  - Automatically generates .jou scripts from MCP operations
  - Can convert between PyFluent API, MCP tools, and TUI commands
---

# ANSYS Fluent TUI Command Guide Skill

## What This Skill Does

This skill provides comprehensive guidance for working with ANSYS Fluent 2024 R2 Text User Interface (TUI) commands. It helps users understand, find, and correctly construct TUI commands for both mesh generation (meshing mode) and CFD solving (solution mode).

## When to Use This Skill

Use this skill when:
- **Finding commands**: User asks "How do I set..." or "What command controls..." in Fluent
- **Understanding syntax**: User needs clarification on command format, arguments, or parameters
- **Building scripts**: User is writing batch files, Python scripts, or journal files for Fluent automation
- **Constructing workflows**: User needs step-by-step TUI commands for a specific simulation task
- **Validating commands**: User wants to verify their command syntax before executing
- **Command discovery**: User explores available commands in meshing or solution mode

## Skill Structure

### TUI Basics (Always Start Here)

ANSYS Fluent TUI uses a hierarchical command structure with forward slashes separating levels:

```
/menu/submenu/command [arguments]
```

**Key principles:**
- Commands can be abbreviated to minimum unique characters (e.g., `m/s` = `mesh/size`)
- Full paths can be used directly without interactive navigation
- Arguments can be numbers, strings, or lists
- Help is available via `/help` or by typing `?`

### Two Main Command Modes

**1. Meshing Mode** - Used for mesh generation and import
- Categories: boundary, cad-assemblies, diagnostics, display, file, material-point, mesh, objects, parallel, preferences, report, scoped-sizing, size-functions
- Focus on mesh operations and preparation

**2. Solution Mode** - Used for CFD setup, solving, and post-processing
- Categories: adjoint, define, display, file, mesh, parallel, plot, preferences, report, server, solve, surface, turbo-workflow, turbo-post, views
- Focus on physics definition, simulation control, and results analysis

## Integration with ANSYS MCP

This skill works seamlessly with ANSYS MCP (if available):

- **When MCP is used for Fluent operations**, automatically provide TUI command context and syntax
- **When user asks about TUI commands**, guide them on equivalent MCP calls if applicable
- **For automation workflows**, combine MCP tool calls with TUI command understanding for optimal results

### Automatic MCP → TUI Command Mapping (Core Feature)

**IMPORTANT: When MCP tools are called, automatically:**

1. **Track the MCP call** with full parameters
2. **Map to TUI equivalent** - show what TUI command does the same thing
3. **Generate .jou script** - provide reproducible script format
4. **Explain the operation** - what happened and why

**MCP Tool Mapping Template:**

```
MCP Tool Called:
  fluent_set_solver(viscous_model="spalart-allmaras")

↓ Maps to TUI:
  /define/models/turbulence spalart-allmaras yes

↓ In .jou Script:
  /define/models/turbulence spalart-allmaras yes

↓ Explanation:
  • Sets the turbulence model to Spalart-Allmaras
  • Required before initializing the flow
  • Related: /define/models/energy enable, /define/models/transient yes
```

### Building Scripts from MCP Operations

When MCP tools are called in sequence, **automatically accumulate and generate the .jou script**:

```
MCP Sequence:
├─ fluent_launch()
├─ fluent_read_case("mesh.cas")
├─ fluent_set_solver(viscous_model="spalart-allmaras")
├─ fluent_set_boundary(zone="inlet", bc_type="velocity-inlet", params={"velocity": 5.0})
└─ fluent_iterate(iterations=500)

↓ Auto-generated .jou script:
/file/read-case "mesh.cas"
/define/models/turbulence spalart-allmaras yes
/define/boundary-conditions/inlet velocity-inlet
/define/boundary-conditions/inlet/velocity 5.0
/solve/iterate 500
```

### Synergy Pattern: MCP + Skill

Every MCP interaction should follow this pattern:

```
┌─────────────────────────────────────────┐
│ MCP Tool is Called                      │
└────────────┬────────────────────────────┘
             │
             ├─→ MCP executes operation (returns result)
             │
             ├─→ Skill automatically:
             │   ├─ Maps to TUI command
             │   ├─ Adds to script buffer
             │   ├─ Explains operation
             │   └─ Suggests related commands
             │
             ↓
     ┌──────────────────────────────┐
     │ User gets 3 things:          │
     ├──────────────────────────────┤
     │ 1. MCP result (execution)    │
     │ 2. TUI mapping (learning)    │
     │ 3. Script (reproducibility)  │
     └──────────────────────────────┘
```

### Example Integration
```
User: "Use ANSYS MCP to set up a mesh with size 0.1"
Skill provides:
- TUI equivalent: /mesh/size 0.1
- Explains what the operation does
- Suggests related TUI commands that may be needed
```

---

## How to Help Users

### 1. Command Lookup

When a user asks about a specific operation, help them find the right command:

```
User: "How do I set the mesh size?"
Skill response: "Use the mesh/size command:
  Syntax: /mesh/size <size_value>
  Example: /mesh/size 0.5
  This sets the global mesh size to 0.5 units"
```

### 2. Syntax Explanation

Break down command syntax clearly:

```
/boundary/boundary-conditions/<zone-type> <property> <value>
  - <zone-type>: inlet, outlet, wall, interior, etc.
  - <property>: velocity-inlet, pressure-outlet, etc.
  - <value>: specific value for the property
```

### 3. Practical Examples

Provide real-world command sequences:

```
# Example: Setting up inlet boundary condition
/define/boundary-conditions/inlet velocity-inlet
/define/boundary-conditions/inlet/velocity 10.5
/define/boundary-conditions/inlet/temperature 300
```

### 4. Command Validation

When users provide commands, verify syntax and suggest improvements:

```
User: "/mesh/refine all 0.1"
Response: "✓ Valid syntax. This refines all regions with size 0.1
Tip: You can also use zone names: /mesh/refine zone_5 0.1"
```

## Common Workflows

### Workflow 1: Basic Mesh Setup
1. `/file/read-mesh "imported_mesh.msh"`
2. `/mesh/size 0.5`
3. `/mesh/check`
4. `/mesh/statistics`

### Workflow 2: Solution Mode Setup
1. `/file/read-case "mesh.cas"`
2. `/define/materials/fluid water`
3. `/define/boundary-conditions/inlet velocity-inlet`
4. `/solve/set/discretization ...`
5. `/solve/iterate 1000`

### Workflow 3: Batch Processing
Users can build complete scripts combining multiple commands:
```
/file/read-mesh "mesh.msh"
/define/materials/fluid air
/define/boundary-conditions/inlet velocity 5
/solve/initialize all
/solve/iterate 500
/file/write-results "results.res"
```

## Data Types & Arguments

**Numbers**: Real or integer values
- Example: `/mesh/size 0.5` or `/solve/iterate 1000`

**Strings**: Text values, quoted if containing spaces
- Example: `/file/read-case "my simulation.cas"`

**Lists/Multiple values**: Comma-separated or space-separated
- Example: `/boundary/list all` or `/display/set-view front`

## Command Categories Reference

### Meshing Mode Categories (13+)

| Category | Purpose | Common Commands |
|----------|---------|-----------------|
| **boundary** | Zone and boundary operations | `/boundary/list`, `/boundary/create` |
| **file** | File I/O operations | `/file/read-mesh`, `/file/write-mesh` |
| **mesh** | Mesh operations and sizing | `/mesh/size`, `/mesh/refine`, `/mesh/check` |
| **display** | Visualization controls | `/display/set-view`, `/display/mesh` |
| **diagnostics** | Mesh diagnostics | `/diagnostics/check-mesh`, `/diagnostics/statistics` |
| **cad-assemblies** | CAD import and management | `/cad-assemblies/import`, `/cad-assemblies/clean` |
| **material-point** | Material point operations | `/material-point/compute` |
| **objects** | Object manipulation | `/objects/list`, `/objects/create` |
| **parallel** | Parallel processing | `/parallel/start`, `/parallel/num-processes` |
| **preferences** | User preferences | `/preferences/display`, `/preferences/memory` |
| **report** | Reporting tools | `/report/create-report` |
| **scoped-sizing** | Scoped mesh sizing | `/scoped-sizing/create-sizing` |
| **size-functions** | Size function operations | `/size-functions/create`, `/size-functions/compute` |

### Solution Mode Categories (15+)

| Category | Purpose | Common Commands |
|----------|---------|-----------------|
| **define** | Physics and BC definition | `/define/materials`, `/define/boundary-conditions` |
| **solve** | Solver control | `/solve/iterate`, `/solve/set/discretization` |
| **file** | File I/O in solution mode | `/file/read-case`, `/file/write-results` |
| **display** | Visualization | `/display/set-view`, `/display/contours` |
| **plot** | Plotting and graphs | `/plot/xy-plot`, `/plot/residuals` |
| **surface** | Surface operations | `/surface/create-isosurface` |
| **mesh** | Mesh adaptation | `/mesh/adapt`, `/mesh/size-function` |
| **adjoint** | Adjoint solver operations | `/adjoint/solve`, `/adjoint/sensitivity` |
| **parallel** | Parallel solving | `/parallel/set/num-processes` |
| **preferences** | User preferences | `/preferences/units`, `/preferences/display` |
| **report** | Report generation | `/report/surface-integrals` |
| **server** | Server operations | `/server/connection-settings` |
| **turbo-workflow** | Turbomachinery workflow | `/turbo-workflow/initialize` |
| **turbo-post** | Turbomachinery post-processing | `/turbo-post/create-report` |
| **views** | View management | `/views/save-view`, `/views/restore-view` |

## Tips for Users

1. **Use abbreviations for faster typing**: `m/s` instead of `mesh/size`
2. **Chain commands with semicolons**: `/mesh/size 0.5; /mesh/check; /mesh/statistics`
3. **Use system commands**: `/system "command"` to execute system shell commands
4. **Query information**: Commands ending with `?` show available options
5. **Help is available**: Type `/help` or `/h` to see available commands at any level
6. **Scripting**: Combine TUI commands into .jou (journal) files for batch processing
7. **Error checking**: Use `/mesh/check` and `/diagnostics/check-mesh` to validate setup

## Advanced Features

- **Aliases**: Create custom command shortcuts for frequently used sequences
- **Scheme Language**: Use Scheme scripting for complex automation (beyond basic TUI)
- **System Integration**: Execute system commands from within Fluent via `/system`
- **Batch Processing**: Run scripts non-interactively for automated workflows
- **Variables**: Define and use variables in scripts for parameterization

## Reference Materials

For detailed command reference and examples, see the `references/` folder:
- **ANSYS_Fluent_TUI_Complete_Reference.md** - Comprehensive reference with 300+ commands
- **ANSYS_Fluent_TUI_Index.json** - Structured index for programmatic lookup
- **README_ANSYS_TUI_Documentation.md** - Navigation guide

## How the Skill Responds

When helping with TUI commands, the skill will:

1. **Identify the operation** the user wants to perform
2. **Locate the relevant command** from the comprehensive reference
3. **Show command syntax** with parameter explanations
4. **Provide working examples** for common use cases
5. **Suggest command shortcuts** where applicable
6. **Explain any prerequisites** or dependencies between commands
7. **Validate user commands** if they provide their own
8. **Suggest optimizations** for batch processing or automation

---

**Last Updated:** 2026-06-10  
**Documentation Version:** ANSYS Fluent 2024 R2  
**Total Commands Covered:** 300+  
**Modes Supported:** Meshing Mode, Solution Mode
