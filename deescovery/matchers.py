"""Module and object matchers."""
import fnmatch
import inspect
from dataclasses import dataclass
from typing import Any, List, Type


@dataclass
class MatchByPattern:
    """**Module matcher** that selects module names by patterns.

    **Example:**

    ```python
    matcher = MatchByPattern(["*.models", "*.models.*"])
    ```

    Attributes:
        patterns: the list of Unix shell-style wildcards for module names. E.g.
            the following instance will match all files `models.py` and
            `models/<something>.py` in a flat list of packages inside your application.
    """

    patterns: List[str]

    def __call__(self, value: str) -> bool:
        for pattern in self.patterns:
            if fnmatch.fnmatch(value, pattern):
                return True
        return False


@dataclass
class MatchByType:
    """**Object matcher** that selects instances by their type.

    Same as `lambda obj: isintance(obj, object_type)`.

    **Example:**

    Find all Flask blueprints in a module.

    ```python
    from flask import Blueprint
    matcher = MatchByType(Blueprint)
    ```

    Attributes:
        object_type: object type or a list of types.
    """

    object_type: Type

    def __call__(self, obj: Any):
        return isinstance(obj, self.object_type)


@dataclass
class MatchBySubclass:
    """**Object matcher** that select classes that are subclasses of a given type.

    Almost the same as `lambda obj: issubclass(obj, object_type)`.

    **Example:**

    Find all Django models.

    ```python
    from django.db import models
    matcher = MatchBySubclass(models.Model)
    ```

    Attributes:
        object_type: a type or a tuple of types.
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
    """**Object matcher** that selects objects having an attribute with the given name.

    The same as `lambda obj: hasattr(obj, attribute_name)`

    **Example:**

    Find all objects that have an attribute `init_app`.

    ```python
    MatchByAttribute("init_app")
    ```

    Attributes:
        attribute_name: attribute name as a string.
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
