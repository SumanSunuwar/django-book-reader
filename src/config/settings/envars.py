from core.utils.collections import deep_update
from core.utils.settings import get_settings_from_environment

"""
This takes env variables with a matching prefix, strips out the prefix,
and adds it to the global variables fed to the settings configuration.

For example:
export CORESETTINGS_IN_DOCKER=true (environment variable)

Could then be referred as a global as:
IN_DOCKER (where the value would be True)
"""

# global() is a dictionary of glabal variables
deep_update(globals(), get_settings_from_environment(ENVAR_SETTINGS_PREFIX))  # type: ignore # noqa: F821
