import os
from typing import Union, Optional, Any


def env(env_var: str) -> str:
    """Simplify to read environment Variable

    Args:
        env_var (str): name of environment variable

    Returns:
        str : value of environment variable
    """
    return os.getenv(env_var)


def nested_get(
    nested_input: Union[dict, list], keys: list, cast_type: Optional[type] = None
) -> Any:
    """Utility function to get a value from a nested dictionary with a default value and optional type casting.

    Args:
        nested_dict (dict): nested dictionary/list
        parameters (list): list of keys
        typ (type): convert to specific type

    Returns:
        any: return value of specific type
    """
    for key in keys:
        if isinstance(nested_input, list):
            try:
                nested_input = nested_input[key]
            except IndexError:
                return None

        elif isinstance(nested_input, dict):
            nested_input = nested_input.get(key, None)

        # Wird dieser Block überhaupt benötigt?
        # else:
        #     return None

        # Verlasse Schleife auf jeden Fall, sobald nested_input == None ist
        if nested_input is None:
            return None

    # convert to correct type if set
    return (
        cast_type(nested_input)
        if cast_type and nested_input is not None
        else nested_input
    )
