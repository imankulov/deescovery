from importlib import import_module
from typing import List

from roman_discovery import IRule
from roman_discovery.discovery import ModuleRule, ObjectRule
from roman_discovery.matchers import (
    MatchByCallableAttribute,
    MatchByPattern,
    MatchByType,
)


def get_flask_rules(import_path: str, flask_app) -> List[IRule]:
    """
    Return a list of rules useful for the Flask application.

    The following rules will be returned:

    - Load SQLAlchemy models (files models.py)
    - Load Flask blueprints (files controllers.py)
    - Load Flask CLI commands (files cli.py)
    - Initialize services (top-level file services.py)

    Args:
        import_path: name of the top-level module of the project (like, "myproject")
        flask_app: a Flask app instance.

    Returns:
        A list of rules, suitable to be passed to "roman_discovery.discover()"
    """
    return [
        models_loader(import_path),
        blueprints_loader(import_path, flask_app),
        commands_loader(import_path, flask_app),
        service_initializer(import_path, flask_app),
    ]


def models_loader(import_path):
    """Load all models."""
    return ModuleRule(
        name="Flask models loader",
        module_matches=MatchByPattern(generate_patterns(import_path, "models")),
        module_action=import_module,
    )


def blueprints_loader(import_path, flask_app):
    """Find and import all blueprints in the application."""
    try:
        from flask import Blueprint
    except ImportError:
        raise RuntimeError("Flask is not installed.")
    return ObjectRule(
        name="Flask blueprints loader",
        module_matches=MatchByPattern(generate_patterns(import_path, "controllers")),
        object_matches=MatchByType(Blueprint),
        object_action=flask_app.register_blueprint,
    )


def commands_loader(import_path, flask_app):
    """Find all commands and register them as Flask CLI commands."""
    try:
        from flask.cli import AppGroup
    except ImportError:
        raise RuntimeError("Flask is not installed.")
    return ObjectRule(
        name="Flask CLI commands loader",
        module_matches=MatchByPattern(generate_patterns(import_path, "cli")),
        object_matches=MatchByType(AppGroup),
        object_action=flask_app.cli.add_command,
    )


def service_initializer(import_path, flask_app):
    """
    Find and initialize all instances of Flask applications.

    Notice that the initialize scans for top-level services files, and doesn't
    walk over all your app's domain package.
    """
    return ObjectRule(
        name="Flask service initializer",
        module_matches=MatchByPattern([f"{import_path}.services"]),
        object_matches=MatchByCallableAttribute("init_app"),
        object_action=lambda obj: obj.init_app(app=flask_app),
    )


def generate_patterns(import_path: str, module_prefix: str) -> list[str]:
    """
    Generate a list of patterns to discover.

    For example, gen_patterns("myapp", "models") generates patterns that make matchers
    discover the content in the following files.

        myapp/users/models.py
        myapp/invoices/models.py
        (etc. for all domain packages beyond "users" and "invoices")
        ...

        myapp/users/models_roles.py
        myapp/users/models_groups.py
        (etc. for all modules started with "models_" in all domain packages)
        ...

        myapp/users/models/roles.py
        myapp/users/models/groups.py
        (if you prefer nested structures)
    """
    return [
        f"{import_path}.*.{module_prefix}",
        f"{import_path}.*.{module_prefix}_*",
        f"{import_path}.*.{module_prefix}.*",
    ]
