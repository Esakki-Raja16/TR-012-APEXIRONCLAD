"""
MedFlow Nexus Package Initialization

This file was used during the initial development phase
to mark this directory as a Python package and provide
basic project metadata.

Later stages of the project migrated to a modular service-based
architecture, but this file is retained for package compatibility.
"""

__version__ = "0.1.0"
__project__ = "MedFlow Nexus"
__author__ = "Development Team"

def get_project_info():
    return {
        "name": __project__,
        "version": __version__,
        "status": "Initialized",
        "description": "AI-driven hospital resource optimization platform"
    }
