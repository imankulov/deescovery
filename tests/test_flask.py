from flask import Flask

from roman_discovery.flask import discover_flask


def test_discover_flask_should_load_blueprints(sample_project):
    flask_app = Flask("foo")
    discover_flask("sample_project", flask_app)
    assert list(flask_app.blueprints.keys()) == ["users"]


def test_discover_flask_should_load_cli(sample_project):
    flask_app = Flask("foo")
    discover_flask("sample_project", flask_app)
    assert list(flask_app.cli.commands.keys()) == ["users"]


def test_discover_flask_should_initialize_services(sample_project):
    flask_app = Flask("foo")
    discover_flask("sample_project", flask_app)
    from sample_project.services import bar, foo  # noqa

    assert foo.app == flask_app
    assert bar.app == flask_app
