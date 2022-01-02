"""List of generic matchers."""
import fnmatch
import inspect
from dataclasses import dataclass
from typing import Any, List, Type


@dataclass
class MatchByPattern:
    """Module matcher that selects module names by patterns.

    Constructor accepts the list of Unix shell-style wildcards for module names. E.g.
    the following instance will match all files "models.py" and "models/<something>.py"
    in a flat list of packages inside your application.

        matcher = MatchByPattern(["*.models", "*.models.*"])
    """

    patterns: List[str]

    def __call__(self, value: str) -> bool:
        for pattern in self.patterns:
            if fnmatch.fnmatch(value, pattern):
                return True
        return False


@dataclass
class MatchByType:
    """Object matcher that selects instances by type.

    Constructor accepts a type or a tuple of types. E.g., the following instance will
    find all Flask blueprints in a module.

        from flask import Blueprint
        matcher = MatchByType(Blueprint)
    """

    object_type: Type

    def __call__(self, obj: Any):
        return isinstance(obj, self.object_type)


@dataclass
class MatchBySubclass:
    """Object matcher that select classes that are subclasses of a given type.

    Constructor accepts a type or a tuple of types. E.g., the following instance will
    find all Django models in a model.

        from django.db import models
        matcher = MatchBySubclass(models.Model)
    """

    object_type: Type

    def __call__(self, obj: Any):
        return (
            inspect.isclass(obj)
            and issubclass(obj, self.object_type)
            and obj != self.object_type
        )


@dataclass
class MatchByAttribute:
    """Object matcher that selects having an attribute with the given name.

    Constructor accepts an attribute name as a string. E.g., the following instance
    will find all objects that have an attribute `init_app` (a common way for
    initializing Flask plugins.)

        MatchByAttribute("init_app")
    """

    attribute_name: str

    def __call__(self, obj: Any):
        return hasattr(obj, self.attribute_name)


@dataclass
class MatchByMethod:
    """**Object matcher** that selects objects having a method with a specific name.

    **Example:**

    Find all objects having a method `init_app()` (a common way for initializing Flask
    plugins.)

    ```python
    MatchByMethod("init_app")
    ```

    Attributes:
        method_name: method name as a string.
    """

    method_name: str

    def __call__(self, obj: Any):
        return (
            not inspect.isclass(obj)
            and hasattr(obj, self.method_name)
            and callable(getattr(obj, self.method_name))
        )
