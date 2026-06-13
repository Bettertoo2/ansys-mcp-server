# ANSYS Fluent TUI Guide Skill - Command Lookup Reference

This file serves as a quick lookup index for the most common TUI command patterns.

## Meshing Mode - Quick Command Reference

### File Operations
```
/file/read-case "filename.cas"         # Read case file
/file/write-case "filename.cas"        # Write case file
/file/read-mesh "filename.msh"         # Read mesh file
/file/write-mesh "filename.msh"        # Write mesh file
/file/export-mesh "filename.msh"       # Export mesh in different format
```

### Mesh Operations
```
/mesh/size 0.5                         # Set global mesh size
/mesh/create-boundary                  # Generate surface mesh
/mesh/create-volume                    # Generate volume mesh
/mesh/check                            # Check mesh validity
/mesh/refinement region_name 0.25      # Local mesh refinement
/mesh/smoothing                        # Improve mesh quality
```

### Diagnostics & Reporting
```
/diagnostics/check-mesh-quality        # Check quality metrics
/diagnostics/find-bad-elements         # Find problematic elements
/diagnostics/repair-mesh               # Attempt to repair mesh
/report/mesh-statistics                # Complete mesh report
/report/element-quality                # Element quality report
/report/face-statistics                # Face zone statistics
```

### CAD & Geometry
```
/cad-assemblies/import-file "file.step"    # Import CAD geometry
/cad-assemblies/check-cad-geometry         # Validate CAD model
/cad-assemblies/list-assemblies            # List loaded assemblies
```

### Sizing Controls
```
/size-functions/create constant-size 0.5       # Create size field
/scoped-sizing/create-control sphere-sizing    # Create sphere sizing
/scoped-sizing/sphere-sizing region_name 0.25  # Apply sphere sizing
```

### Display
```
/display/display-mesh yes               # Show mesh
/display/set-view top                   # Set viewing angle (top/front/side/iso)
/display/zoom factor                    # Zoom view
/display/fit-view                       # Fit all to window
```

### Parallel
```
/parallel/num-processes 4               # Set number of parallel processes
/parallel/partition                     # Partition mesh for parallel
/parallel/load-balance                  # Balance mesh partition
```

---

## Solution Mode - Quick Command Reference

### File Operations
```
/file/read-case "filename.cas"         # Read case file
/file/read-data "filename.dat"         # Read data file
/file/write-case "filename.cas"        # Write case file
/file/write-data "filename.dat"        # Write solution data
```

### Physics Definition

#### Materials
```
/define/materials/fluid water           # Define water as fluid
/define/materials/fluid air             # Define air as fluid
/define/materials/solid steel           # Define steel as solid
```

#### Models
```
/define/models/turbulence spalart-allmaras yes      # S-A turbulence
/define/models/turbulence k-epsilon yes             # k-epsilon turbulence
/define/models/turbulence k-omega yes               # k-omega turbulence
/define/models/viscous laminar yes                  # Laminar flow
```

#### Operating Conditions
```
/define/operating-conditions/pressure 101325    # Set gauge pressure (Pa)
/define/reference-values/length 1.0             # Reference length
/define/reference-values/area 1.0               # Reference area
/define/reference-values/velocity 1.0           # Reference velocity
```

### Boundary Conditions

#### Inlet
```
/define/boundary-conditions/inlet velocity-inlet             # Velocity inlet
/define/boundary-conditions/inlet/velocity 5.0               # Set velocity
/define/boundary-conditions/inlet/temperature 300            # Set temperature
/define/boundary-conditions/inlet mass-flow-inlet            # Mass flow inlet
```

#### Outlet
```
/define/boundary-conditions/outlet pressure-outlet           # Pressure outlet
/define/boundary-conditions/outlet/gauge-pressure 0          # Gauge pressure
/define/boundary-conditions/outlet outflow                   # Outflow
```

#### Wall
```
/define/boundary-conditions/wall no-slip                     # No-slip wall
/define/boundary-conditions/wall/temperature 300             # Wall temperature
/define/boundary-conditions/wall/heat-flux 1000              # Heat flux
```

### Solver Control

#### Initialize
```
/solve/initialize/initialize-flow                           # Initialize all
/solve/initialize/initialize-flow zone_name                 # Initialize region
```

#### Iterate
```
/solve/iterate 1000                      # Run 1000 iterations
/solve/iterate 100                       # Run 100 iterations
```

#### Check Convergence
```
/solve/converged                         # Check if converged
```

### Visualization & Reporting

#### Display
```
/display/contour velocity-magnitude      # Show velocity magnitude contour
/display/contour pressure                # Show pressure contour
/display/contour temperature             # Show temperature contour
/display/vector velocity                 # Show velocity vectors
/display/streamline velocity             # Show streamlines
/display/set-view top                    # Set viewing angle
```

#### Plotting
```
/plot/xy-plot convergence-history        # Plot convergence history
/plot/xy-plot time-series                # Plot time history
```

#### Reports
```
/report/force-coefficients               # Calculate force coefficients
/report/surface-integrals surface_name   # Calculate surface integrals
/report/massflow zone_name               # Calculate mass flow
```

### Parallel Solving
```
/parallel/num-processes 8                # Use 8 parallel processes
/parallel/load-balance                   # Load balance mesh
```

---

## Common Command Abbreviations

| Full Command | Abbreviation |
|-------------|--------------|
| `/mesh/size` | `/m/s` |
| `/file/read-case` | `/f/r` |
| `/file/write-case` | `/f/w` |
| `/solve/iterate` | `/s/i` |
| `/display/contour` | `/d/c` |
| `/define/materials` | `/d/m` |
| `/define/boundary-conditions` | `/d/b` |
| `/solve/initialize` | `/s/in` |
| `/report/mesh-statistics` | `/r/m` |

---

## Data Type Reference

### Numeric Arguments
```
/mesh/size 0.5              # Decimal number
/solve/iterate 1000         # Integer number
/define/reference-values/velocity 15.2   # Floating point
```

### String Arguments (with/without quotes)
```
/file/read-case "mesh.cas"              # String with spaces requires quotes
/define/materials/fluid water           # Simple keywords don't need quotes
/file/read-case my_mesh.cas             # Simple filenames work without quotes
```

### Boolean Arguments
```
/define/models/turbulence/spalart-allmaras yes    # yes/no
/preferences/show-grid no                         # true/false equivalent
```

### Multiple Arguments/Lists
```
/boundary/boundary-conditions/copy (zone1 zone2 zone3)    # List in parentheses
/report/surface-integrals (outlet1 outlet2)               # Multiple zones
```

---

## Getting Help in TUI

```
command?                    # Brief help for command
command??                   # Detailed help
/help                       # General help
/help command               # Help for specific command
```

---

## Saving Commands as Scripts

Create `.jou` (journal) files with commands:

```
; Fluent Journal File
; This is a comment

/file/read-case "mesh.cas"
/mesh/size 0.5
/mesh/check
/report/mesh-statistics
/file/write-case "output.cas"
```

Execute with:
```bash
fluent 3d -i script.jou
```

---

**Last Updated:** 2026-06-10  
**ANSYS Fluent Version:** 2024 R2
