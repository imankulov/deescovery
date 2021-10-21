# Typer

[Typer](https://typer.tiangolo.com/) is a library to build command-line interfaces. It supports commands and subcommands, and you may use Typer to create the extendable CLI API for your project, sort of like Django management commands.

**File myproject/app.py**

```python
import typer
from deescovery import discover, ObjectRule
from deescovery.matchers import MatchByPattern, MatchByType

typer_app = typer.Typer()

rules = [
    ObjectRule(
        name="Typer CLI loader",
        module_matches=MatchByPattern(["myproject.*.cli"]),
        object_matches=MatchByType(typer.Typer),
        object_action=lambda obj: typer_app.add_typer(obj),
    ),
]

discover("myproject", rules)

if __name__ == "__main__":
    typer_app()
```

**Files that match the module pattern `myproject.*.cli`. For example, `myproject/users/cli.py`**

```python
import typer
app = typer.Typer(name="users")

@app.command("create")
def create(name: str):
    print(f"Creating {name}")

@app.command("delete")
def delete(name: str):
    print(f"Deleting {name}")
```

This configuration creates the sub-command "users" with sub-sub-commands "create" and "delete."

```shell
python myproject/app.py users create Roman
Creating Roman

python myproject/app.py users delete Roman
Deleting Roman
```
