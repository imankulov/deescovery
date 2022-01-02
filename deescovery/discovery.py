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
    """Generic type for a discovery rule.

    Normally, you use one of its subclasses:
    [ModuleRule][deescovery.discovery.ModuleRule] or
    [ObjectRule][deescovery.discovery.ObjectRule]
    """

    @abc.abstractmethod
    def discover(self, module_name: str) -> None:
        raise NotImplementedError()


@dataclass
class ModuleRule(IRule):
    """Do something with all modules matching the rule.

    For each module, found by [deescovery.discover][], the rule decides if it should
    be processed (calls `module_matcher`), and if the result is positive, calls
    `module_action`.

    **Example:**

    Import all `controllers.py` of the project.


    ```python
    from importlib import import_module
    from flask import Flask, Blueprint
    from deescovery import discover, ModuleRule
    from deescovery.matchers import MatchByPattern, MatchByType

    app = Flask(__name__)

    controller_loader = ModuleRule(
        name="Flask blueprints loader",
        module_matches=MatchByPattern(["*.controllers"]),
        module_action=import_module,
    )

    discover("myapp", [controller_loader])
    ```

    Attributes:
        name: the rule name. Used for logging purposes.
        module_matches: a callable (function) that takes the module name and returns
            True if the module should be processed. You can write your
            own ad-hoc function, or use a [deescovery.matchers.MatchByPattern][]
            class.

        module_action: a callable (function) that takes the module name. The action
            will only be executed if the module matches the pre-condition of
            `module_matches`. The most common action is importing the module to
            execute its content. For example, you can use it to register all API
            controllers that the module contains and defines with decorators.
    """

    name: str
    module_matches: ModuleMatches
    module_action: ModuleAction

    def discover(self, module_name: str) -> None:
        if self.module_matches(module_name):  # type: ignore
            logger.debug(f"{self.name} found module {module_name}")
            self.module_action(module_name)  # type: ignore


@dataclass
class ObjectRule(IRule):
    """Do something with all objects, matching the rules.

    For each module, found by [deescovery.discover][], the rule decides if the module
    should be processed (calls `module_matches`). If the result is positive, the module
    is imported, and all its members are inspected with `object_matches`. If
    the returned value of the object matcher is also True, calls `object_action`.

    **Example:**

    Find all [Flask blueprints](https://flask.palletsprojects.com/en/2.0.x/blueprints/)
    in the files `controllers.py` of the project and register them in the Flask
    application.

    ```python
    from flask import Flask, Blueprint
    from deescovery import discover, ObjectRule
    from deescovery.matchers import MatchByPattern, MatchByType

    app = Flask(__name__)

    blueprints_loader = ObjectRule(
        name="Flask blueprints loader",
        module_matches=MatchByPattern(["*.controllers"]),
        object_matches=MatchByType(Blueprint),
        object_action=app.register_blueprint,
    )

    discover("myapp", [blueprints_loader])
    ```

    Attributes:
        name: the rule name. Used for logging purposes.
        module_matches: a callable (function) that takes the module name and returns
            True if objects of the module should be inspected further with
            `object_matches`. You can write your own ad-hoc function or use a
            [deescovery.matchers.MatchByPattern][] class.
        object_matches: a callable (function) that takes the object and returns
            True if the object should be processed with `object_action`. You can write
            your own ad-hoc function or use one of the classes defined in the
            [deescovery.matchers][] module.
        object_action: a callable (function) that takes the found object.
            The action will only be executed when the object's module pre-condition
            passes the `module_matches` test, and object itself passes the
            pre-condition of `object_matches`.
    """

    name: str
    module_matches: ModuleMatches
    object_matches: ObjectMatches
    object_action: ObjectAction

    def discover(self, module_name: str) -> None:
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
            match specification and the action, if the object matches.  Normally, it's
            a list IRule subclasses: [ModuleRule][deescovery.discovery.ModuleRule] or
            [ObjectRule][deescovery.discovery.ObjectRule].
    """
    for module_name in find_modules(import_path=import_path, recursive=True):
        for rule in rules:
            rule.discover(module_name)
