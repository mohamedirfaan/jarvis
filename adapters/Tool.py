class Tool:
    def __init__(self, id, name, description, parameters):
        self.id = id
        self.name = name
        self.description = description
        self.parameters = parameters

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getParameters(self):
        return self.parameters