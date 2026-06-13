@echo off
REM Fluent TUI Script Generator Batch File
REM This generates example .jou scripts for ANSYS Fluent

REM Create CFD Simulation Example
(
echo ; Fluent Journal File - Complete CFD Simulation
echo ; This script sets up and runs a complete CFD analysis
echo.
echo ; Import mesh
echo /file/read-case "mesh.cas"
echo.
echo ; Define turbulence model
echo /define/models/turbulence spalart-allmaras yes
echo.
echo ; Define material
echo /define/materials/fluid water
echo.
echo ; Set operating conditions
echo /define/operating-conditions/pressure 101325
echo.
echo ; Define boundary conditions - Inlet
echo /define/boundary-conditions/inlet velocity-inlet
echo /define/boundary-conditions/inlet/velocity 5.0
echo /define/boundary-conditions/inlet/temperature 300
echo.
echo ; Define boundary conditions - Outlet
echo /define/boundary-conditions/outlet pressure-outlet
echo /define/boundary-conditions/outlet/gauge-pressure 0
echo.
echo ; Initialize solution
echo /solve/initialize/initialize-flow
echo.
echo ; Run solver for 500 iterations
echo /solve/iterate 500
echo.
echo ; Display results
echo /display/contour velocity-magnitude
echo /plot/xy-plot convergence-history
echo.
echo ; Save results
echo /file/write-case "results.cas"
echo /file/write-data "results.dat"
) > cfd_simulation_example.jou

echo Created: cfd_simulation_example.jou

REM Create Mesh Refinement Example
(
echo ; Fluent Journal File - Local Mesh Refinement
echo ; This script demonstrates local mesh refinement operations
echo.
echo /file/read-case "mesh.cas"
echo.
echo ; Perform local refinement at inlet region
echo /mesh/refinement inlet_zone 0.1
echo.
echo ; Check updated mesh
echo /mesh/check
echo /report/mesh-statistics
echo.
echo /file/write-case "mesh_refined.cas"
) > mesh_refinement_example.jou

echo Created: mesh_refinement_example.jou

echo.
echo All example scripts created successfully!
