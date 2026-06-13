#!/usr/bin/env python3
"""
ANSYS Fluent TUI Command Query Tool
Helps find and validate TUI commands from the comprehensive reference.
"""

import json
import re
from pathlib import Path

class FluentTUIHelper:
    """Helper class for ANSYS Fluent TUI command operations"""

    def __init__(self, reference_file: str = None):
        """Initialize with reference data"""
        self.commands_db = self._load_reference(reference_file)

    def _load_reference(self, ref_file):
        """Load command reference data"""
        # This would load from the JSON index in a real implementation
        return {
            "meshing_categories": [
                "boundary", "cad-assemblies", "diagnostics", "display",
                "file", "material-point", "mesh", "objects", "parallel",
                "preferences", "report", "scoped-sizing", "size-functions"
            ],
            "solution_categories": [
                "adjoint", "define", "display", "file", "mesh", "parallel",
                "plot", "preferences", "report", "server", "solve", "surface",
                "turbo-workflow", "turbo-post", "views"
            ]
        }

    def search_command(self, keyword: str) -> list:
        """Search for commands by keyword"""
        keyword = keyword.lower()
        results = []

        # Search in categories
        for cat in self.commands_db.get("meshing_categories", []):
            if keyword in cat.lower():
                results.append({"type": "meshing", "category": cat})

        for cat in self.commands_db.get("solution_categories", []):
            if keyword in cat.lower():
                results.append({"type": "solution", "category": cat})

        return results

    def validate_command(self, command: str) -> dict:
        """Validate command syntax"""
        # Basic validation pattern
        pattern = r'^/?[\w\-/]+(\s+[\w\-".]+)*$'

        is_valid = bool(re.match(pattern, command))

        return {
            "command": command,
            "valid": is_valid,
            "has_leading_slash": command.startswith("/"),
            "parts": command.lstrip("/").split("/")
        }

    def get_abbreviation(self, command: str) -> str:
        """Generate command abbreviation"""
        parts = command.lstrip("/").split("/")
        abbrev = "/".join([part[0] for part in parts])
        return abbrev

    def suggest_command(self, operation: str) -> list:
        """Suggest commands for an operation"""
        suggestions = {
            "mesh_size": "/mesh/size",
            "read_mesh": "/file/read-case",
            "iterate": "/solve/iterate",
            "boundary": "/define/boundary-conditions/",
            "materials": "/define/materials/",
            "initialize": "/solve/initialize/",
            "display": "/display/contour",
            "check_mesh": "/diagnostics/check-mesh-quality"
        }
        return suggestions.get(operation.lower(), [])

def main():
    """Example usage"""
    helper = FluentTUIHelper()

    # Example: Search for mesh commands
    mesh_commands = helper.search_command("mesh")
    print(f"Found {len(mesh_commands)} categories with 'mesh':")
    for cmd in mesh_commands:
        print(f"  - {cmd['type']}: {cmd['category']}")

    # Example: Validate a command
    test_cmd = "/mesh/size 0.5"
    validation = helper.validate_command(test_cmd)
    print(f"\nValidation of '{test_cmd}':")
    print(f"  Valid: {validation['valid']}")
    print(f"  Parts: {validation['parts']}")

    # Example: Get abbreviation
    abbrev = helper.get_abbreviation(test_cmd)
    print(f"  Abbreviation: {abbrev}")

if __name__ == "__main__":
    main()
