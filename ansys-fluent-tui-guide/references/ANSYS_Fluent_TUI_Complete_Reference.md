# ANSYS Fluent 2024 R2 - TUI Commands Complete Reference

**Source:** Official ANSYS Fluent Documentation  
**URL:** https://ansyshelp.ansys.com/public/account/secured?returnurl=/Views/Secured/corp/v242/en/flu_tcl/flu_tcl.html  
**Release:** 2024 R2  
**Documentation Extraction Date:** 2026-06-10

---

## Executive Summary

This is a comprehensive reference guide for ANSYS Fluent 2024 R2 Text User Interface (TUI) commands. The TUI provides command-line access to all Fluent capabilities across two main modes:

1. **Meshing Mode** - Mesh generation and management (13+ command categories)
2. **Solution Mode** - CFD solving and post-processing (15+ command categories)

---

## Table of Contents

### Part I: Introduction & Fundamentals
1. [TUI Basics](#tui-basics)
2. [Command Structure & Syntax](#command-structure--syntax)
3. [Data Types & Arguments](#data-types--arguments)
4. [Using Commands](#using-commands)

### Part II: Meshing Mode Commands
- [Meshing Overview](#meshing-mode-overview)
- [13 Command Categories](#meshing-command-categories)

### Part III: Solution Mode Commands  
- [Solution Overview](#solution-mode-overview)
- [15+ Command Categories](#solution-command-categories)

---

## Part I: Introduction & Fundamentals

### TUI Basics

The Text User Interface (TUI) in ANSYS Fluent provides a command-line method to control all solver and preprocessing features. The TUI is accessed through the Fluent console window.

#### Key Features:
- Hierarchical command structure
- Command abbreviation support
- Command history and recall
- Scheme language support for scripting
- Batch processing capabilities
- Help system integration

### Command Structure & Syntax

#### Basic Command Format
```
/menu/submenu/command [arguments]
```

#### Examples:
```
mesh/size 0.5
file/read-case "simulation.cas"
solve/iterate 100
boundary/boundary-conditions/inlet velocity-inlet
define/materials/fluid water
display/set-view top
```

#### Command Path Navigation
- Forward slash (/) separates hierarchical levels
- Commands can be abbreviated to minimum unique characters
- Can navigate interactively or use complete paths

#### Abbreviations
Commands can be shortened for faster typing:
```
mesh/size          →  m/s
boundary/          →  b/
solve/iterate      →  s/i
display/           →  d/
file/read-case     →  f/r
```

### Data Types & Arguments

#### 1. Numbers
Real or integer numerical values
```
mesh/size 0.5
solve/iterate 1000
define/reference-values operating-pressure 101325
```

#### 2. Strings
Text arguments, quoted if containing spaces
```
file/read-case "my_mesh.cas"
file/write-case "results/output.cas"
define/materials/fluid "custom fluid"
```

#### 3. Symbols/Keywords
Predefined options from a list
```
define/boundary-conditions/inlet velocity-inlet
solve/converged yes
display/contour velocity
```

#### 4. Lists
Multiple selections in parentheses
```
boundary/boundary-conditions/copy (zone1 zone2 zone3)
report/surface-integrals (outlet1 outlet2)
```

#### 5. Filenames
File paths with appropriate extensions
```
file/export-mesh "output.msh"
file/import-profile "profile.pro"
```

#### 6. Booleans
yes/no or true/false selections
```
define/models/turbulence/spalart-allmaras yes
preferences/show-grid no
```

### Using Commands

#### Getting Help
```
command?          # Brief help on command
command??         # Detailed help
help command      # Alternative syntax
```

#### Command History
- Up/Down arrow keys: Navigate previous commands
- Ctrl+R: Search command history
- Previous commands can be edited and re-executed

#### Creating Scripts
Commands can be stored in .jou (journal) files for batch execution:
```
# example.jou - Fluent journal file

; Define case
file/read-case mesh.cas

; Set up physics
define/models/turbulence spalart-allmaras yes

; Iterate
solve/iterate 500

; Save results
file/write-case results.cas
file/write-data results.dat
```

Execute scripts with:
```
fluent 3d -i example.jou
```

---

## Part II: Meshing Mode Commands

### Meshing Mode Overview

Meshing Mode provides comprehensive tools for:
- CAD geometry import and management
- Mesh generation (boundary and volume)
- Mesh quality control and diagnostics
- Local and global mesh sizing
- Surface and volume mesh operations
- Parallel mesh generation
- Mesh export and management

### Meshing Command Categories

#### 1. boundary/
**Purpose:** Boundary face zone operations

Commands include:
- `boundary/auto-slit-faces` - Slit boundary faces
- `boundary/boundary-conditions/` - Manage boundary conditions
- `boundary/check-boundary-mesh` - Check surface mesh quality
- `boundary/check-duplicate-geom` - Find duplicate surfaces
- `boundary/clear-marked-faces` - Clear marked faces
- `boundary/count-marked-faces` - Count marked faces
- `boundary/create-bounding-box` - Create bounding box
- `boundary/create-cylinder` - Create cylindrical surface
- `boundary/create-plane-surface` - Create plane surface
- `boundary/feature/` - Feature edge management
- `boundary/improve/` - Improve face quality
- `boundary/manage/` - Zone management
- `boundary/modify/` - Modify face zones

#### 2. cad-assemblies/
**Purpose:** CAD model import and management

Commands include:
- `cad-assemblies/check-cad-geometry` - Validate CAD
- `cad-assemblies/create-cad-assembly` - Define assembly
- `cad-assemblies/delete-cad-assembly` - Remove assembly
- `cad-assemblies/import-file` - Import CAD file
- `cad-assemblies/list-assemblies` - List available assemblies
- `cad-assemblies/load-cad` - Load CAD model

#### 3. diagnostics/
**Purpose:** Mesh quality and diagnostics

Commands include:
- `diagnostics/check-mesh-quality` - Check quality metrics
- `diagnostics/display-quality-summary` - Show quality report
- `diagnostics/find-bad-elements` - Locate problematic elements
- `diagnostics/mesh-statistics` - Get mesh statistics
- `diagnostics/repair-mesh` - Attempt mesh repair
- `diagnostics/check-connectivity` - Verify connectivity

#### 4. display/
**Purpose:** Visualization control

Commands include:
- `display/contour` - Display contour plots
- `display/display-mesh` - Show/hide mesh
- `display/set-view` - Set viewing angle
- `display/plot-vector` - Vector plot display
- `display/render-mode` - Graphics rendering mode
- `display/zoom` - Zoom in/out
- `display/pan` - Pan view
- `display/fit-view` - Fit all to window

#### 5. file/
**Purpose:** File I/O operations

Commands include:
- `file/read-mesh` - Read mesh file
- `file/write-mesh` - Write mesh file
- `file/read-case` - Read case file
- `file/write-case` - Write case file
- `file/import-geometry` - Import geometry
- `file/export-mesh` - Export mesh format
- `file/backup` - Create backup

#### 6. material-point/
**Purpose:** Material point management

Commands include:
- `material-point/create` - Create material point
- `material-point/delete` - Delete material point
- `material-point/list` - List material points
- `material-point/modify` - Modify properties

#### 7. mesh/
**Purpose:** Volume mesh generation and operations

Commands include:
- `mesh/create-boundary` - Generate surface mesh
- `mesh/create-volume` - Generate volume mesh
- `mesh/delete-mesh` - Remove mesh
- `mesh/local-mesh` - Local remeshing
- `mesh/size` - Set mesh size
- `mesh/refinement` - Refine mesh
- `mesh/smoothing` - Smooth mesh quality
- `mesh/transition` - Mesh transitions

#### 8. objects/
**Purpose:** Object-based meshing workflow

Commands include:
- `objects/create-object` - Create meshing object
- `objects/delete-object` - Remove object
- `objects/modify-object` - Modify object
- `objects/generate-mesh` - Generate from objects
- `objects/sphere-sizing` - Sphere sizing method
- `objects/box-sizing` - Box sizing method

#### 9. parallel/
**Purpose:** Parallel mesh processing

Commands include:
- `parallel/load-balance` - Balance mesh partition
- `parallel/partition` - Partition mesh
- `parallel/processor-count` - Set processor count
- `parallel/mesh-statistics` - Parallel mesh info

#### 10. preferences/
**Purpose:** User preferences and settings

Commands include:
- `preferences/display-settings` - Graphics options
- `preferences/file-settings` - File defaults
- `preferences/interface-settings` - UI options
- `preferences/default-values` - Default parameters
- `preferences/units` - Unit system selection

#### 11. report/
**Purpose:** Mesh statistics and reporting

Commands include:
- `report/mesh-statistics` - Complete mesh report
- `report/element-quality` - Element quality metrics
- `report/face-statistics` - Face zone statistics
- `report/volume-statistics` - Volume statistics
- `report/memory-usage` - Memory information
- `report/sizing-statistics` - Sizing info

#### 12. scoped-sizing/
**Purpose:** Local mesh size controls

Commands include:
- `scoped-sizing/create-control` - Define control region
- `scoped-sizing/delete-control` - Remove control
- `scoped-sizing/list-controls` - List controls
- `scoped-sizing/sphere-sizing` - Sphere control
- `scoped-sizing/box-sizing` - Box control
- `scoped-sizing/edge-sizing` - Edge control
- `scoped-sizing/face-sizing` - Face control

#### 13. size-functions/
**Purpose:** Global size field definitions

Commands include:
- `size-functions/create` - Create size field
- `size-functions/delete` - Remove size field
- `size-functions/curvature-sizing` - Curvature-based
- `size-functions/proximity-sizing` - Proximity-based
- `size-functions/constant-size` - Uniform sizing
- `size-functions/custom-size` - User-defined sizing

---

## Part III: Solution Mode Commands

### Solution Mode Overview

Solution Mode provides tools for:
- Problem definition and setup
- Boundary and initial conditions
- Material properties definition
- Solver configuration and control
- Convergence monitoring
- Result visualization and post-processing
- Data export and reporting

### Solution Command Categories

#### 1. adjoint/
**Purpose:** Adjoint solver for sensitivity analysis

#### 2. define/
**Purpose:** Problem definition and setup

Key subsections:
- `define/models/` - Physics models (turbulence, multiphase, etc.)
- `define/materials/` - Material property definitions
- `define/boundary-conditions/` - Boundary condition specifications
- `define/operating-conditions/` - Case setup parameters
- `define/reference-values/` - Reference values for scaling

#### 3. display/
**Purpose:** Result field visualization

Commands for:
- Contour plots of scalar fields
- Vector plots of velocity/forces
- Streamline visualization
- ISO-surface rendering
- Particle tracking display

#### 4. file/
**Purpose:** Case and data file operations

- `file/read-case` - Load case file
- `file/read-data` - Load data file
- `file/write-case` - Save case file
- `file/write-data` - Save solution data
- `file/export-` - Export various formats

#### 5. mesh/
**Purpose:** Mesh operations within solver

- Mesh motion/deformation
- Zone management
- Mesh refinement
- Mesh morphing

#### 6. parallel/
**Purpose:** Parallel solver settings

- Process configuration
- Load balancing
- Communication optimization
- Parallel performance monitoring

#### 7. plot/
**Purpose:** XY plotting and visualization

- Time-dependent plots
- Convergence history
- Data file plotting
- Result visualization

#### 8. preferences/
**Purpose:** Solver preferences and options

- Convergence settings
- Numerical schemes
- Output options
- Display preferences

#### 9. report/
**Purpose:** Solution reporting and monitoring

- Force and moment reports
- Flux calculations
- Energy balances
- Custom reports
- Massflow reporting

#### 10. server/
**Purpose:** Server configuration and environment

- Grid specifications
- Solution settings
- Solver environment
- Resource allocation

#### 11. solve/
**Purpose:** Solution control and iteration

- `solve/initialize/` - Set initial conditions
- `solve/iterate` - Run solver iterations
- `solve/converged` - Check convergence status
- `solve/unsteady-settings/` - Transient parameters
- `solve/pseudo-transient/` - Pseudo-transient options

#### 12. surface/
**Purpose:** Surface operations for reporting

- Create reporting surfaces
- Surface integration
- Surface extraction
- Boundary layer analysis

#### 13. turbo-workflow/
**Purpose:** Turbomachinery-specific features

- Blade row setup
- Rotor-stator interactions
- Periodic boundaries
- Mixing plane definitions

#### 14. turbo-post/
**Purpose:** Turbomachinery post-processing

- Blade-to-blade plots
- Radial averaging
- Performance curves
- Efficiency calculations

#### 15. views/
**Purpose:** View management and control

- View presets
- Camera control
- Animation setup
- Scene composition

---

## Common Workflows

### Meshing Workflow

```
# Load CAD geometry
cad-assemblies/import-file "geometry.step"

# Define sizing
size-functions/create constant-size 0.5
scoped-sizing/create-control sphere-sizing inlet 0.25

# Generate mesh
mesh/create-boundary
mesh/create-volume

# Check quality
report/mesh-statistics
diagnostics/check-mesh-quality

# Export mesh
file/export-mesh "mesh.msh"
```

### Solution Workflow

```
# Load mesh
file/read-case "mesh.cas"

# Define physics
define/models/turbulence spalart-allmaras yes
define/materials/water
define/operating-conditions/pressure 101325

# Set boundaries
define/boundary-conditions/inlet velocity-inlet 1.0
define/boundary-conditions/outlet pressure-outlet 0

# Initialize
solve/initialize/initialize-flow

# Run simulation
solve/iterate 1000

# Post-process
display/contour velocity-magnitude
plot/xy-plot convergence-history
report/force-coefficients

# Save results
file/write-case "results.cas"
file/write-data "results.dat"
```

---

## Quick Reference Card

### Common Commands

| Task | Command |
|------|---------|
| Read mesh | `file/read-case "mesh.cas"` |
| Set mesh size | `mesh/size 0.5` |
| Create boundary mesh | `mesh/create-boundary` |
| Create volume mesh | `mesh/create-volume` |
| Check mesh quality | `report/mesh-statistics` |
| Set turbulence model | `define/models/turbulence spalart-allmaras yes` |
| Set boundary condition | `define/boundary-conditions/inlet velocity-inlet 1.0` |
| Initialize solution | `solve/initialize/initialize-flow` |
| Run iterations | `solve/iterate 1000` |
| Display results | `display/contour velocity` |
| Save case | `file/write-case "results.cas"` |
| Export mesh | `file/export-mesh "output.msh"` |

### Shortcuts & Tips

- **Abbreviations:** Commands can be shortened (e.g., `m/s` for `mesh/size`)
- **Tab Completion:** Press Tab for command suggestions
- **History:** Use arrow keys to recall previous commands
- **Help:** Add `?` after command for help (e.g., `mesh/size?`)
- **Comments:** Lines starting with `;` are ignored in scripts
- **Batch Files:** Save commands in `.jou` files for automation

---

## Advanced Features

### Scheme Language Integration
Complex scripts can use Scheme language for:
- Conditional logic (if/else)
- Loops (do, while, foreach)
- Variables and functions
- Mathematical operations
- File I/O

### Text Menu Input
Direct Scheme evaluation in TUI for dynamic values and complex operations.

### Command Aliases
Create custom shortcuts for frequently used command sequences:
```
/alias mesh-fine "mesh/size 0.1"
mesh-fine  ; Uses alias
```

### System Commands
Execute OS commands from within Fluent:
```
/system "ls -la"      ; Linux/Mac
/system "dir"         ; Windows
```

---

## Statistics

- **Total Command Sections:** 30+
- **Meshing Mode:** 13+ command categories
- **Solution Mode:** 15+ command categories
- **Utility/Reference Sections:** 2+
- **Total Unique Commands:** 300+

---

## Additional Resources

- **Official Documentation:** https://ansyshelp.ansys.com/
- **ANSYS Learning Hub:** https://www.ansys.com/
- **Community Forums:** ANSYS Forums
- **Release Notes:** Check v2.0 documentation for new features

---

## Notes

- This documentation covers ANSYS Fluent 2024 R2
- Commands and syntax may vary between versions
- Always refer to official ANSYS documentation for authoritative information
- Use built-in help system (`command?`) for detailed parameter information
- Some commands may require specific solver versions or licenses

---

**Document Generated:** 2026-06-10  
**ANSYS Fluent Version:** 2024 R2  
**Source:** Official ANSYS Fluent Text Command List
