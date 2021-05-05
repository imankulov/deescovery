import pathlib
import sys

import pytest


@pytest.fixture
def collector():
    return []


@pytest.fixture
def sample_project(tmpdir):
    """Return a sample project."""
    tmpdir = pathlib.Path(tmpdir)
    (tmpdir / "sample_project").mkdir()
    (tmpdir / "sample_project" / "__init__.py").write_text("")
    (tmpdir / "sample_project" / "services.py").write_text(services)
    (tmpdir / "sample_project" / "users").mkdir()
    (tmpdir / "sample_project" / "users" / "__init__.py").write_text("")
    (tmpdir / "sample_project" / "users" / "controllers.py").write_text(controllers)
    (tmpdir / "sample_project" / "users" / "cli.py").write_text(cli)
    sys.path.insert(0, tmpdir.as_posix())
    yield tmpdir
    sys.path = sys.path[1:]


services = """
class App():
    app = None
    def init_app(self, app):
        self.app = app

foo = App()
bar = App()
"""

controllers = """
from flask import Blueprint

blueprint = Blueprint("users", __name__)

@blueprint.route("/", methods=["GET"])
def users():
    return ''
"""

cli = """
from flask.cli import AppGroup

app_group = AppGroup("users")
"""
