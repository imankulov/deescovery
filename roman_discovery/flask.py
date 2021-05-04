from importlib import import_module

from roman_discovery.discovery import ModuleRule, ObjectRule, discover
from roman_discovery.matchers import (
    MatchByCallableAttribute,
    MatchByPattern,
    MatchByType,
)


def discover_flask(import_path, flask_app):
    discover(
        import_path=import_path,
        rules=[
            models_loader(import_path),
            blueprints_loader(import_path, flask_app),
            commands_loader(import_path, flask_app),
            service_initializer(import_path, flask_app),
        ],
    )


def models_loader(import_path):
    """Load all models."""
    return ModuleRule(
        name="Flask models loader",
        module_matches=MatchByPattern(
            [f"{import_path}.*.models", f"{import_path}.*.models.*"]
        ),
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
        module_matches=MatchByPattern(
            [f"{import_path}.*.controllers", f"{import_path}.*.controllers.*"]
        ),
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
        module_matches=MatchByPattern(
            [f"{import_path}.*.cli", f"{import_path}.*.cli.*"]
        ),
        object_matches=MatchByType(AppGroup),
        object_action=flask_app.cli.add_command,
    )


def service_initializer(import_path, flask_app):
    """Find and initialize all instances of Flask applications."""
    return ObjectRule(
        name="Flask service initializer",
        module_matches=MatchByPattern([f"{import_path}.services"]),
        object_matches=MatchByCallableAttribute("init_app"),
        object_action=lambda obj: obj.init_app(app=flask_app),
    )
