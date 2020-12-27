


def block22(attrs, *body):
    return {
        'type': 'block',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }

def grid(attrs, *body):
    return {
        'type': 'grid',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }


def line(attrs, *body):
    return {
        'type': 'staticline',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }

def vblock22(attrs, *body):
    return {
        'type': 'vblock',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }

def scrollblock(attrs, *body):
    return {
        'type': 'scrolledblock',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }


def input22(attrs, *body):
    return {
        'type': 'input',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }

def text22(attrs, *body):
    return {
        'type': 'statictext',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }

def textctrl(attrs, *body):
    return {
        'type': 'textctrl',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }

def textarea(attrs, *body):
    return {
        'type': 'textarea',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }

def dropdown(attrs, *body):
    return {
        'type': 'dropdown',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }


def listctrl(attrs, *body):
    return {
        'type': 'listctrl',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }

def bitmap(attrs, *body):
    return {
        'type': 'bitmap',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }


def bitmapbtn(attrs, *body):
    return {
        'type': 'bitmapbtn',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }


def gauge(attrs, *body):
    return {
        'type': 'gauge',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }

def button(attrs, *body):
    return {
        'type': 'button',
        'id': 'uuid',
        'attrs': attrs,
        'children': body
    }