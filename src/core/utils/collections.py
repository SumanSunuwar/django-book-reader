def deep_update(base_dict, update_with):
    # iterating over items in dict passed for update
    for key, value in update_with.items():
        if isinstance(value, dict):
            base_dict_value = base_dict.get(key)
            # if the value is also a nested dict
            if isinstance(base_dict_value, dict):
                deep_update(base_dict_value, value)
            # if the value is not a nested dict
            else:
                base_dict[key] = value
        # if the value passed is not a dict
        else:
            base_dict[key] = value

    return base_dict
