import copy

def merge(base, add):
    """
    Deep merges `add` over `base`.
    This will return a new dict. The input dicts `base` and `add` stay untouched.
    """
    A = copy.deepcopy(base)
    B = copy.deepcopy(add)

    for key, value in B.items():
        if isinstance(value, dict):
            # get node or create one
            node = A.setdefault(key, {})
            merge(value, node)
        else:
            A[key] = value

    return A