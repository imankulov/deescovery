# Roman Discovery

## Background

Micro-framework-based projects are clean while they're small. Every micro-framework codebase I've seen suffer from the same problem: a mess in the project initialization module. Sooner or later, your entry point package becomes a soup of ad-hoc environment reads, imports-within-functions, and plug-in initializations.

The infamous `create_app()` is a boiling broth where architectural rules, dependencies, and common sense don't exist.  The core of The Application Factory Pattern, proposed, for example, in the [official Flask documentation](https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/), and the [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure), legitimize this pattern.

It would be OK to keep that ugly, primordial mess hidden behind a layer of abstraction, but the primitive nature of `create_app()` leaves no place for the [open-closed principle](https://blog.cleancoder.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html). We need to get back to this module every time we add a new plug-in, a new blueprint, or a new package.

## Discovery to the rescue

When it comes to taming the chaos, opinionated structure and automated discovery can help.

- You describe your application structure, outlining where you keep models, blueprints, controllers, etc.
- You define auto-discovery rules: what your initialization code does when it finds an object of a specific type.
- You let roman-discovery do the rest.

It's specifically helpful for frameworks that define resources on the fly with decorators and expect you to import all necessary modules. For example, it can be helpful for Flask to load all your blueprints, initialize extensions, and import SQLAlchemy models.

[Visitor pattern](https://refactoring.guru/design-patterns/visitor) is the best name for the approach you like finding patterns in implementation details.


## Install

```shell
pip install roman-discovery
```

## Glossary

I find it helpful to add some semantic colors to the packages and modules of the app. For this, I introduce the terms "domain package" and "module role."

**Domain package** -- one of the multiple top-level packages of the application that contains the business logic. Adepts of domain-driven design would define domain packages as containers to encapsulate [bounded contexts](https://martinfowler.com/bliki/BoundedContext.html).

**Module Role** -- a group of modules or packages (directories with `__init__.py` files) used for the same purpose. I prefer express roles with module prefixes or second-level packages. For example, files `models_users.py` and `models_groups.py` can have the "Models" role and keep your model definitions, and files `controllers_users.py` and `controller_groups.py` can have the "Controllers" role and keep the code for your controllers.

## Usage with Flask

Using within the opinionated Flask structure was the initial purpose of the package. Use `roman_discovery.discover()` with
`roman_discovery.flask.get_flask_rules()`.

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
from roman_discovery import discover
from roman_discovery.flask import get_flask_rules


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


## Usage with anything else

You can create your own discovery rules with the `discover()` function, `ModuleRule` and `ObjectRule`. Optionally, you can take advantage of custom matchers, defined in `roman_discovery.matchers`.

For example, that's how you print all modules and all callable objects within the `roman_discovery` itself.

```python
from roman_discovery import discover, ModuleRule, ObjectRule

module_printer = ModuleRule(
    name="module printer",
    module_matches=lambda module_name: True,
    module_action=lambda module_name: print(f"Found module {module_name}"),
)

object_printer = ObjectRule(
    name="object printer",
    module_matches=lambda module_name: True,
    object_matches=callable,
    object_action=lambda obj: print(f"Found callable object {obj!r}"),
)

discover("roman_discovery", rules=[module_printer, object_printer])
```

## Why the "roman" prefix?

I use it as my own "pseudo-namespace." If I ever abandon the project, at least the package doesn't occupy a common name.
