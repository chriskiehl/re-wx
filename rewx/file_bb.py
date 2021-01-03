from file_a import extention_hook


@extention_hook.register(int)
def fn(a):
    return 'Hello from int handler!'


@extention_hook.register(list)
def fn(a):
    return 'Hello from list handler!'