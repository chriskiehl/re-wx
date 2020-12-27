

registry = {}


class AppDB(object):

    def __init__(self, state):
        self.subscriptions = {}
        self.state = state

    def sub(self, subf):
        def register(f):
            self.subscriptions[subf] = f
            self.notify()
        return Subscriber(register)

    def notify(self):
        for query, updater in self.subscriptions.items():
            updater(query(self.state))

    def setState(self, state):
        self.state = state
        self.notify()


class Subscriber(object):
    def __init__(self, ff):
        self.ff = ff

    def subscribe(self, updater):
        self.ff(updater)



