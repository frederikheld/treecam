def merge(base, add):
    """
    Deep merges `add` over `base`.
    """
    for key, value in add.items():
        if isinstance(value, dict):
            # get node or create one
            node = base.setdefault(key, {})
            merge(value, node)
        else:
            base[key] = value

    return base