class PlanAdapter:
    def __init__(self):
        self.steps = []
        self.index = 0

    def initializeSteps(self, steps):
        self.steps = steps

    def getNextStep(self):
        if self.index < len(self.steps):
            result = self.steps[self.index]
        else:
            return None
        self.index += 1
        return result

    def addPlanStep(self, step):
        self.steps.append(step)
