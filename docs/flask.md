# Usage with Flask

The initial purpose of the package was to serve as a discovery module for the opinionated Flask structure. Out of the box, the deescovery can do the following.

- **Initialize services.** The de-facto standard of initializing Flask extensions is to have classes with the method `init_app()`. The rules will scan top-level services.py of your application, find all the instances that have `init_app()` methods, and call `obj.init_app(app=flask_app)` for each of them.
- **Initialize blueprints.** Scan controllers.py, controllers_*.py and controllers/ to find [Flask blueprints](https://flask.palletsprojects.com/en/2.0.x/blueprints/) and attach them to the flask application.
- **Initialize SQLALchemy.** Import all files in models.py models_*.py and models/ to help [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/) find all the SQLAlchemy models to create migrations.
- **Initialize all commands.** Flask supports [custom commands](https://flask.palletsprojects.com/en/2.0.x/cli/). The rules scan cli.py, cli_*.py and cli/ to find flask.cli.AppGroup instances and attach them to Flask's CLI.

The function expects the following project structure.

```
myproject

  app.py
  config.py
  services.py

  foo/
    controllers.py
    models.py
    cli.py

  bar/
    controllers.py
    models.py
    cli.py

  ...
```

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
