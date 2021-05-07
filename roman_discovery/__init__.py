"""Top-level package for Roman Discovery."""

__author__ = """Roman Imankulov"""
__email__ = "roman.imankulov@gmail.com"
__version__ = "0.2.0"


from roman_discovery.discovery import IRule, ModuleRule, ObjectRule, discover

__all__ = (
    "discover",
    "IRule",
    "ModuleRule",
    "ObjectRule",
)
