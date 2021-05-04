# Note: a number of type-ignore hints is due to an issue with mypy.
# Ref: https://github.com/python/mypy/issues/5485
import abc
import inspect
from dataclasses import dataclass
from importlib import import_module
from logging import getLogger
from typing import Any, Callable, List

from roman_discovery.contrib import find_modules

ModuleMatches = Callable[[str], bool]
ModuleAction = Callable[[str], Any]
ObjectMatches = Callable[[Any], bool]
ObjectAction = Callable[[Any], Any]


logger = getLogger(__name__)


class IRule(abc.ABC):
    @abc.abstractmethod
    def discover(self, module_name: str):
        ...


@dataclass
class ModuleRule(IRule):
    name: str
    module_matches: ModuleMatches
    module_action: ModuleAction

    def discover(self, module_name: str):
        if self.module_matches(module_name):  # type: ignore
            logger.debug(f"{self.name} found module {module_name}")
            self.module_action(module_name)  # type: ignore


@dataclass
class ObjectRule(IRule):
    name: str
    module_matches: ModuleMatches
    object_matches: ObjectMatches
    object_action: ObjectAction

    def discover(self, module_name: str):
        if not self.module_matches(module_name):  # type: ignore
            return
        module_obj = import_module(module_name)
        for object_name, obj in inspect.getmembers(
            module_obj, predicate=self.object_matches  # type: ignore
        ):
            logger.debug(f"{self.name} found {object_name} in {module_name}")
            self.object_action(obj)  # type: ignore


def discover(import_path: str, rules: List[IRule]):
    for module_name in find_modules(import_path=import_path, recursive=True):
        for rule in rules:
            rule.discover(module_name)
