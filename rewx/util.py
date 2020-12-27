from pyrsistent.typing import PVector, PMap
from typing import Dict

def callwith(f, *args, **kwargs):
    def inner(*ignoreargs, **ignorekwargs):
        return f(*args, **kwargs)
    return inner

def eq(target):
    def inner(index, item: Dict):
        return item == target
    return inner


def veq(key, val):
    def inner(index: int, item: PMap):
        return item[key] == val
    return inner


def extend(collection: PVector):
    def inner(list):
        return list + collection
    return inner