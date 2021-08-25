# Usage with anything else

When it comes to taming the chaos, opinionated structure and automated discovery can help. The package implements a so-called [visitor pattern](https://refactoring.guru/design-patterns/visitor).

- You describe your application structure, outlining where you keep models, blueprints, controllers, etc.
- You define auto-discovery rules: what your initialization code does when it finds an object of a specific type.
- You let roman-discovery do the rest.

It's specifically helpful for frameworks that define resources on the fly with decorators and expect you to import all necessary modules. For example, it can be helpful for Flask to load all your blueprints, initialize extensions, and import SQLAlchemy models.

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
