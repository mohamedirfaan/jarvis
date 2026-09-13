import json
from PromptHelper.PlanPromptHelper import PlanPromptHelper
from adapters.PlanAdapter import PlanAdapter
from cache import ToolDataLoader


class OrchestratorAgent:
    def __init__(self, inputContext):
        self.inputContext = inputContext
        self._registry = None
        self._isActive = True
        self._isTerminalConditionMet = False
        self.promptBuilder = PlanPromptHelper()
        self.associated_agents = None
        self.registerWorkerAgents(inputContext.getAgentName())
        self.planAdapter = PlanAdapter()

    def setRegistry(self, registry):
        self._registry = registry

    def registerWorkerAgents(self, agentName):
        toolData = ToolDataLoader.getToolData()
        orchestrators = toolData["orchestrators"]
        for orchestrator in orchestrators:
            if orchestrator["name"] == agentName:
                self.associated_agents = orchestrator["agents"]
                break


    def run(self):
        print("orchestrator agent started")
        while self.isActive() and not self._isTerminalConditionMet:
            self.executeCycle()
        print("orchestrator agent stopped")

    def  isActive(self):
        return self._isActive

    def setIsActive(self, status):
        self._isActive = status

    def executeCycle(self):
        status = self._registry.getComponent("SESSION_ADAPTER").getStatus(self.inputContext.getSessionId())[0][0]
        try:
            if status == 'planning':
                self.handlePlanningPhase()
            elif status == 'running':
                self.handleRunningPhase()
        except Exception as e:
            print(e)

    def handlePlanningPhase(self):
        aiClient = self._registry.getComponent("AI_CLIENT_ADAPTER")
        planningPrompt = self.promptBuilder.generatePlanningPrompt(self.inputContext.getSessionId(),
                                                                   self._registry.getComponent("SESSION_ADAPTER"),
                                                                   self._registry.getComponent("TOOL_ADAPTER"),
                                                                   self._registry.getComponent("AGENT_ADAPTER"), self.associated_agents)
        response = aiClient.send(planningPrompt)
        print(response)
        self.planAdapter = self.promptBuilder.parsePlanStepsAndGetPlanAdapter(json.loads(response))
        self._registry.getComponent("SESSION_ADAPTER").updateStatus(self.inputContext.getSessionId(), "running")


    def handleRunningPhase(self):
        step = self.planAdapter.getNextStep()
        stepType = step.getStepType()
        if stepType == "agent":
            self.spawnAgent(step)
        elif stepType == "tool":
            self.executeTool(step)
            self.setTerminationConditionMet(True)

    def shutDown(self):
        self._registry.getComponent("SESSION_ADAPTER").updateStatus(self.inputContext.getSessionId(), "closed")
        self._isActive = False

    def setTerminationConditionMet(self, status):
        self._isTerminalConditionMet = status


    def spawnAgent(self, step):
        pass

    def executeTool(self, step):
        toolName = step.getName()
        print("executing tool")
        if toolName == "speak":
            print(step.getStepInput()[0])