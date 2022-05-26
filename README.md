<!--intro-start-->
# Deescovery

**Deescovery** is a Python package to find and initialize modules of your Python projects on startup.

- Find and register blueprints in a Flask project.
- Automatically initialize Flask extensions.
- Find all SQLAlchemy models to make alembic happy.
- Find all FastAPI endpoints.
- Collect all Celery tasks.

Initially designed to initialize Flask applications, it was made generic enough to work with any micro-framework or no framework at all.

## Micro-framework initialization problem

Micro-framework-based projects are clean while they're small. Every micro-framework codebase I've seen, has a mess in the project initialization. With time, `create_app()` becomes filled with ad-hoc settings, imports-within-functions, and plug-in initializations.

The Application Factory Pattern, proposed, for example, in the [official Flask documentation](https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/), and the [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure), legitimize this approach.

The nature of `create_app()` leaves no place for the [open-closed principle](https://blog.cleancoder.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html). We update this module every time we add a new plug-in, a new blueprint, or a new package.

```python
# myproject/__init__.py

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from myproject.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from myproject.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
```

_A common Flask application. The code is based on the Flask Mega-Tutorial._

With `deescovery`, you can make the same code shorter, and remove the dependencies from implementation details.

```python
# file: myproject/app.py
from flask import Flask
from deescovery import discover
from deescovery.flask import get_flask_rules


def create_app():
    flask_app = Flask(__name__)
    flask_app.config.from_object("myproject.config")
    discover("myproject", get_flask_rules("myproject", flask_app))
    return flask_app
```


<!--intro-end-->

## Read more

- [Usage with Flask](https://imankulov.github.io/deescovery/flask/)
- [Usage with anything else](https://imankulov.github.io/deescovery/anything_else/)
- [API](https://imankulov.github.io/deescovery/api/deescovery/)
