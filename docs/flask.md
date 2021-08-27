# Usage with Flask

Using within the opinionated Flask structure was the initial purpose of the package. Use `deescovery.discover()` with
`deescovery.flask.get_flask_rules()`.

The function expects the following project structure.

```
myproject

  app.py
  config.py
  services.py

  # Simple flat structure with one module
  # per role in a domain package.
  foo/
    controllers.py
    models.py
    cli.py


  # Flat structure with multiple modules per
  # role in a domain package. Modules of the same
  # role share the same prefix
  bar/
    controllers_api.py
    controllers_admin.py
    models_users.py
    models_projects.py
    cli_users.py
    cli_projects.py

  # Nested structure with one flat package per role
  baz/
    controllers/
      api.py
      admin.py
    models/
      users.py
      projects.py
    cli/
      users.py
      projects.py
```

With this structure, it will do the following.

- Scan controllers.py, controllers_*.py and controllers/ to find blueprints and attach the blueprints to the flask application.
- Import all files in models.py models_*.py and models/ to help flask-migrate find all the SQLAlchemy models to create migrations.
- Scan cli.py, cli_*.py and cli/ to find flask.cli.AppGroup instances and attach them to Flask's CLI.
- Scan top-level services.py, find all the instances that have `init_app()` methods, and call `obj.init_app(app=flask_app)` for each of them.

An example of your top-level app.py

```python
# file: myproject/app.py
from flask import Flask
from deescovery import discover
from deescovery.flask import get_flask_rules


def app() -> Flask:
    flask_app = Flask(__name__, instance_relative_config=True)
    flask_app.config.from_object("myproject.config")
    flask_rules = get_flask_rules("myproject", flask_app)
    discover("myproject", flask_rules)
    return flask_app
```

An example of your top-level services.py

```python
# file: myproject/services.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate(db=db)
mail = Mail()
```

