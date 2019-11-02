import logging


def move_property(metadata_view, source_property, target_property):
    source_property_split = source_property.split('.')
    target_property_split = target_property.split('.')

    if _is_source_property_multivalue(metadata_view, source_property_split):
        _replace_keys_in_dictionary(metadata_view, source_property_split, target_property_split)
    else:
        old_value = _delete_key_from_dictionary(metadata_view, source_property_split)
        _add_key_value_to_dictionary(metadata_view, target_property_split, old_value)

    return metadata_view


def delete_property(metadata_view, source_property):
    source_property_split = source_property.split('.')
    _delete_key_from_dictionary(metadata_view, source_property_split)
    return metadata_view


def _is_source_property_multivalue(metadata_view, source_property_split):
    if len(source_property_split) == 1:
        if isinstance(metadata_view, list):
            return any(source_property_split[0] in metadata_dictionary for metadata_dictionary in metadata_view)
    elif source_property_split[0] in metadata_view:
        return _is_source_property_multivalue(metadata_view[source_property_split[0]], source_property_split[1:])

    return False


def _replace_keys_in_dictionary(metadata_view, nested_source_keys, nested_target_keys):
    if len(nested_source_keys) != len(nested_target_keys):
        raise Exception(
            f"ERROR: Cannot migration a multivalue object at one nested level to a different nested level. Attempted "
            f"to migrate {'.'.join(nested_source_keys)} to {'.'.join(nested_target_keys)}")
    if len(nested_source_keys) > 1:
        if any([source_partial_key != target_partial_key for source_partial_key, target_partial_key in
                zip(nested_source_keys[:-1], nested_target_keys[:-1])]):
            raise Exception(
                f"ERROR: Cannot migration a multivalue object at one nested level to a different nested level. "
                f"Attempted to migrate {'.'.join(nested_source_keys)} to {'.'.join(nested_target_keys)}")

    if len(nested_source_keys) == 1 and isinstance(metadata_view, list):
        for metadata_dict in metadata_view:
            if nested_source_keys[0] in metadata_dict:
                metadata_dict[nested_target_keys[0]] = metadata_dict.pop(nested_source_keys[0])
    elif nested_source_keys[0] in metadata_view:
        _replace_keys_in_dictionary(metadata_view[nested_source_keys[0]], nested_source_keys[1:],
                                    nested_target_keys[1:])
    else:
        logging.warning(
            f"Was not able to find key {nested_source_keys[0]} in metadata schema source view {metadata_view}!")
        return


def _add_key_value_to_dictionary(dictionary, nested_keys, value):
    if len(nested_keys) == 1:
        dictionary[nested_keys[0]] = value
        return
    else:
        if nested_keys[0] not in dictionary:
            dictionary[nested_keys[0]] = {}
        return _add_key_value_to_dictionary(dictionary[nested_keys[0]], nested_keys[1:], value)


def _delete_key_from_dictionary(dictionary, nested_keys):
    if len(nested_keys) == 1 and nested_keys[0] in dictionary:
        value = dictionary[nested_keys[0]]
        del dictionary[nested_keys[0]]
        return value
    elif nested_keys[0] in dictionary:
        return _delete_key_from_dictionary(dictionary[nested_keys[0]], nested_keys[1:])
    else:
        logging.warning(f"Was not able to find key {nested_keys[0]} in metadata schema source view {dictionary}!")
        return
