import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.utils.importlib import import_module


def autodiscover():
    """Auto-discover INSTALLED_APPS autocomplete modules."""
    module_name = "autocomplete"
    for app in settings.INSTALLED_APPS:
        # Attempt to import the app's 'routing' module
        module = '{}.{}'.format(app, module_name)
        try:
            import_module(module)
        except ImportError as ex:
            reason = ex.args[0]
            if 'No module named {}'.format(module_name) in reason \
                    or "No module named '{}'".format(module) in reason:
                logger.info('No module named {}'.format(module))
            else:  # re-raise - something's wrong
                logger.warning(ex)
                raise ImportError(ex)

default_app_config = 'agnocomplete.app.AgnocompleteConfig'
