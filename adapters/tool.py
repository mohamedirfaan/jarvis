class Tool:
    def __init__(self, toolId, name, description, module, className, method, parameters):
        self.id = toolId
        self.name = name
        self.description = description
        self.module = module
        self.className = className
        self.method = method
        self.parameters = parameters

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getParameters(self):
        return self.parameters

    def getToolId(self):
        return self.id

    def getMethod(self):
        return self.method

    def getClassName(self):
        return self.className

    def getModule(self):
        return self.module