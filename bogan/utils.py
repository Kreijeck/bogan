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

    # convert to correct type None type if cast type is known
    if nested_input is None:
        if cast_type == "dict":
            return {}
        elif cast_type == "list":
            return []
        else:
            return None
    
    # Bei positiv Ergebnis konvertiere input, wenn bekannt. Ansonsten das normale value
    return cast_type(nested_input) if cast_type else nested_input
