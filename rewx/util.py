from typing import Any


def callwith(f, *args, **kwargs):
    def inner(*ignoreargs, **ignorekwargs):
        return f(*args, **kwargs)
    return inner

def eq(target):
    def inner(index, item: dict):
        return item == target
    return inner


def veq(key, val):
    def inner(index: int, item: dict):
        return item[key] == val
    return inner


def extend(collection: list):
    def inner(list):
        return list + collection
    return inner


def exclude(m, keys):
    """
    Exclude from the map any items
    matching the supplied `keys`
    """
    return {k: v for k, v in m.items() if k not in keys}


def identity(x: Any):
    """The identity function.
    Returns whatever was given to it."""
    return x

