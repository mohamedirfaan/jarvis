class Agent:
    def __init__(self):
        self._registry = None

    def setRegistry(self, registry):
        self._registry = registry

    def run(self):
        self.executeCycle()

    def executeCycle(self):
        pass