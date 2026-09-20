import cache.ToolDataLoader

class SimpleAgent:
    def __init__(self, inputContext):
        self.inputContext = inputContext
        self._isActive = True
        self.__registry = None
        self.agent_name = inputContext.getAgentName()
        self._terminate_condition_met = False
        self.available_tools = None
        self.tool_description = None
        self.getAvailableTools()

    def setRegistry(self, registry):
        self.__registry = registry

    def getAvailableTools(self):
        toolData = cache.ToolDataLoader.getToolData()
        agents = toolData["agents"]
        for agent in agents:
            if agent["name"] == self.agent_name:
                self.available_tools = agent["tools"]
                break

    def run(self):
        while self.isActive() and not self._terminate_condition_met:
            self.executeCycle()

    def isActive(self):
        return self._isActive

    def executeCycle(self):
        status = self.getAgentStatus()
        if status == "running":
            pass
        elif status == "paused":
            pass
        elif status == "completed":
            pass
        elif status == "failed":
            pass

    def getAgentStatus(self):
        executionAdapter = self.__registry.getComponent("EXECUTION_ADAPTER")
        return executionAdapter.getExecutionStatus(self.inputContext.getAgentId())[0][0]

    def executeInstruction(self):
        aiClient = self.__registry.getComponent("AI_CLIENT_ADAPTER")
        prompt = self.getToolToExecute()
        response = aiClient.send(prompt)
        self.executeTool(response)

    def executeTool(self, response):
        print(response)

    def getToolToExecute(self):
        aiClient = self.__registry.getComponent("AI_CLIENT_ADAPTER")
        component = self.__registry.getComponent("SESSION_ADAPTER")
        prompt = cache.ToolDataLoader.getPrompt("toolRetrievalPrompt.txt")
        prompt = prompt.replace("{{AGENT_NAME}}", self.agent_name)
        prompt = prompt.replace("{{CONTEXT_HISTORY}}", str(self.parseSessionHistory(component.getSessionHistory())))
        prompt = prompt.replace("{{TOOLS}}", self.getToolDescriptions())
        response = aiClient.send(prompt)
        return response

    def parseSessionHistory(self, history):
        parsedHistory = []
        for i in history:
            currHistory = {"message": i[3], "context_type": i[2]}
            parsedHistory.append(currHistory)
        return parsedHistory

    def getToolDescriptions(self):
        toolData = cache.ToolDataLoader.getToolData()
        tools = toolData["tools"]
        tool_description = ""
        for tool in tools:
            if tool.getToolId() in self.available_tools:
                tool_description += "- Name : " + tool.getName() + " Description : " + tool.getDescription() + " Method: " + tool.getMethod() + " Parameters: " + tool.getParameters() + "\n"
        return tool_description