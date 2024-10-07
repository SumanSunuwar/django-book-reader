import os

from .misc import yaml_coerce


def get_settings_from_environment(prefix):
    """Retrieve settings from environment variables with the specified prefix.
    concept:
    for key, value in os.environ.items():
        if key.startswith(prefix):
            # Strip the prefix and coerce value
            settings[key[prefix_len:]] = yaml_coerce(value)
    return settings    """
    prefix_len = len(prefix)
    # Strip the prefix and coerce value
    return {key[prefix_len:]: yaml_coerce(value) for key, value in os.environ.items() if key.startswith(prefix)}
