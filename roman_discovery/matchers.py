import fnmatch
import inspect
from dataclasses import dataclass
from typing import Any, List, Type


@dataclass
class MatchByPattern:
    patterns: List[str]

    def __call__(self, value: str) -> bool:
        for pattern in self.patterns:
            if fnmatch.fnmatch(value, pattern):
                return True
        return False


@dataclass
class MatchByType:
    object_type: Type

    def __call__(self, obj: Any):
        return isinstance(obj, self.object_type)


@dataclass
class MatchByAttribute:
    attribute_name: str

    def __call__(self, obj: Any):
        return hasattr(obj, self.attribute_name)


@dataclass
class MatchByCallableAttribute:
    attribute_name: str

    def __call__(self, obj: Any):
        return (
            not inspect.isclass(obj)
            and hasattr(obj, self.attribute_name)
            and callable(getattr(obj, self.attribute_name))
        )
