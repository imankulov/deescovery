from flask import Flask

from roman_discovery import discover
from roman_discovery.flask import get_flask_rules


def test_discover_flask_should_load_blueprints(sample_project):
    flask_app = Flask("foo")
    rules = get_flask_rules("sample_project", flask_app)
    discover("sample_project", rules)
    assert list(flask_app.blueprints.keys()) == ["users"]


def test_discover_flask_should_load_cli(sample_project):
    flask_app = Flask("foo")
    rules = get_flask_rules("sample_project", flask_app)
    discover("sample_project", rules)
    assert list(flask_app.cli.commands.keys()) == ["users"]


def test_discover_flask_should_initialize_services(sample_project):
    flask_app = Flask("foo")
    rules = get_flask_rules("sample_project", flask_app)
    discover("sample_project", rules)
    from sample_project.services import bar, foo  # noqa

    assert foo.app == flask_app
    assert bar.app == flask_app
