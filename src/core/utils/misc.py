import yaml


def yaml_coerce(value):
    # Check if the value is a string that contains commas
    if isinstance(value, str):
        if ',' in value:
            return [item.strip() for item in value.split(',')]
        return yaml.load(f'dummy: {value}', Loader=yaml.SafeLoader)['dummy']
    return value
