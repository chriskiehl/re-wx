import wx


def dispatch(func):
    """
    TODO: don't expose this from the module, only mount/patch methods
    TODO: DOCS
    """
    registry = {'default': func}

    def merge_registries(other):
        registry.update(other)

    def register(cls, func=None):
        """
        """
        assert issubclass(cls, wx.Object), "TODO! Explain why it must be one of these!"

        if func is None:
            return lambda f: register(cls, f)
        registry[cls] = func
        return func

    def wrapper(element, parent: wx.Window):
        try:
            return registry[element['type']](element, parent)
        except KeyError:
            return registry['default'](element, parent)

    registry[object] = func
    wrapper.register = register
    wrapper._registry = registry
    wrapper.merge_registries = merge_registries
    wrapper.dispatch = dispatch
    return wrapper


@dispatch
def mount(element, parent):
    raise TypeError(f'''
    Encountered an unknown Type ({element['type']}) while trying to mount. 

    cases: 
     1. typo of rewx type: fix yo' shiz 
     2. that wx-widget isn't supported yet. Plz open issue 
     3. they're trying to use their own component: Register mount and update handlers 
    ''')


@dispatch
def update(element, instance):
    raise TypeError(f'''
        Encountered an unknown Type ({element['type']}) while trying to update 
        a mounted component 

        cases: 
         3. It must be that they're trying to use their own component, but didn't 
          register an update handler: register a handler via @update.register(YOUR_TYPE) 
        ''')
