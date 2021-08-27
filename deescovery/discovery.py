# Note: a number of type-ignore hints is due to an issue with mypy.
# Ref: https://github.com/python/mypy/issues/5485
import abc
import inspect
from dataclasses import dataclass
from importlib import import_module
from logging import getLogger
from typing import Any, Callable, List

from deescovery.contrib import find_modules

ModuleMatches = Callable[[str], bool]
ModuleAction = Callable[[str], Any]
ObjectMatches = Callable[[Any], bool]
ObjectAction = Callable[[Any], Any]


logger = getLogger(__name__)


class IRule(abc.ABC):
    """Generic type for a rule."""

    @abc.abstractmethod
    def discover(self, module_name: str):
        ...


@dataclass
class ModuleRule(IRule):
    """Module rule.

    Defines a rule 'Run <module_action> for all modules matching <module_matches>'.
    """

    name: str
    module_matches: ModuleMatches
    module_action: ModuleAction

    def discover(self, module_name: str):
        if self.module_matches(module_name):  # type: ignore
            logger.debug(f"{self.name} found module {module_name}")
            self.module_action(module_name)  # type: ignore


@dataclass
class ObjectRule(IRule):
    """Object rule.

    Defines a rule 'Run <object_action> for all objects matching <object_matches>
    inside modules matching <module_matches>'.
    """

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
    """Discover all objects.

    Scan the package, find all modules and objects, matching the given set of rules,
    and apply actions defined in them.

    Args:
        import_path: top-level module name to start scanning. Usually, it's a name of
            your application, e.g., "myapp". If your application doesn't have a single
            top-level module, you will probably call it for all top-level modules.
        rules: a list of module and objects rules. Each rule contains the
            match specification and the action, if the object matches.
    """
    for module_name in find_modules(import_path=import_path, recursive=True):
        for rule in rules:
            rule.discover(module_name)
