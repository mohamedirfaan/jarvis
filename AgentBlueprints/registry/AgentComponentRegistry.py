class AgentComponentRegistry:
    def __init__(self):
        self.components = {}

    def registerComponent(self, componentName, component):
        self.components[componentName] = component

    def getComponent(self, componentName):
        return self.components[componentName]

    def getAllComponents(self):
        return self.components