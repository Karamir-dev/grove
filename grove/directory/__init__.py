"""
Directory module for Grove.

This module provides utilities to manage project directories
such as creating folder structures and preparing workspace paths.

Exports:
    create_directory (function): Creates a directory with optional parents and error handling.
"""
from .create import create_directory

__all__ = ['create_directory']

