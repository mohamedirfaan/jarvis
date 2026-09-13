class Plan:
    def __init__(self, step_order, step_type, name, step_input):
        self.step_order = step_order
        self.step_type = step_type
        self.name = name
        self.step_input = step_input

    def getStepOrder(self):
        return self.step_order
    def getStepType(self):
        return self.step_type
    def getName(self):
        return self.name
    def getStepInput(self):
        return self.step_input