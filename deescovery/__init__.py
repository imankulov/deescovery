__author__ = """Roman Imankulov"""
__email__ = "roman.imankulov@gmail.com"
__version__ = "1.0.0"


from deescovery.discovery import IRule, ModuleRule, ObjectRule, discover

__all__ = (
    "discover",
    "IRule",
    "ModuleRule",
    "ObjectRule",
)
