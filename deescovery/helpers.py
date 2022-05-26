import importlib
import logging

logger = logging.getLogger(__name__)


def import_module(module_name: str) -> None:
    """Import module by its name.

    Calls importlib.import_module() and logs the action with logging.debug().
    """
    logging.debug("Importing module %s", module_name)
    importlib.import_module(module_name)
