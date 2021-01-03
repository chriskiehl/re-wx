from functools import singledispatch




@singledispatch
def extention_hook(a):
    return 'hello from root handler'


