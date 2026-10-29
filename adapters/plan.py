class Plan:
    def __init__(self, step_order, step_type, name, step_input, method_name, class_name):
        self.step_order = step_order
        self.step_type = step_type
        self.name = name
        self.step_input = step_input
        self.method_name = method_name
        self.class_name = class_name

    def getStepOrder(self):
        return self.step_order
    def getStepType(self):
        return self.step_type
    def getName(self):
        return self.name
    def getStepInput(self):
        return self.step_input
    def getMethodName(self):
        return self.method_name
    def getClassName(self):
        return self.class_name