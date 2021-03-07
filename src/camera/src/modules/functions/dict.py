import copy

def merge(base, add):
    """
    Deep merges `add` over `base`.
    This will return a new dict. The input dicts `base` and `add` stay untouched.
    """

    base = copy.deepcopy(base)
    add = copy.deepcopy(add)

    for key, value in add.items():
        # if key in base.keys():
        if isinstance(value, dict):
            if isinstance(base[key], dict):
                base[key] = merge(base[key], value)
            else:
                base[key] = value
        else:
            base[key] = value

    return base
