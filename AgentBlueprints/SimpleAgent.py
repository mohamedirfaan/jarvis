import json
import cache.ToolDataLoader
import importlib

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
        return self.getAgentStatus()

    def isActive(self):
        return self._isActive

    def executeCycle(self):
        status = self.getAgentStatus()
        if status == "running":
            self.executeInstruction()
        elif status == "paused":
            pass
        elif status == "completed":
            self.shutdown()
        elif status == "failed":
            pass

    def getAgentStatus(self):
        executionAdapter = self.__registry.getComponent("EXECUTION_ADAPTER")
        return executionAdapter.getExecutionStatus(self.inputContext.getAgentId())[0][0]

    def executeInstruction(self):
        response = self.getToolToExecute()
        return self.__registry.getComponent("TOOL_ADAPTER").getTool(json.loads(response)["name"])

    def executeTool(self, response):
        self.__registry.getComponent("SESSION_ADAPTER").addSessionHistoryEntry(self.inputContext.getSessionId(), "tool call", response["name"])
        if response["name"]== "speak":
            print(response["input"])
            self.__registry.getComponent("EXECUTION_ADAPTER").updateAgentExecutionStatus(self.inputContext.getAgentId(), "completed")
            return
        methodName = response.getMethod()
        className = response.getClassName()
        moduleName = response.getModule()
        print(methodName, className)

        tool_Class = getattr(importlib.import_module(moduleName), className)()
        method = getattr(tool_Class, methodName)
        parameters = []
        for i in response["input"].values():
            parameters.append(i)
        tool_result = method(*parameters)
        if tool_result is not None:
            self.__registry.getComponent("SESSION_ADAPTER").addSessionHistoryEntry(
                self.inputContext.getSessionId(), "tool result", str(tool_result)
            )


    def getToolToExecute(self):
        aiClient = self.__registry.getComponent("AI_CLIENT_ADAPTER")
        component = self.__registry.getComponent("SESSION_ADAPTER")
        prompt = cache.ToolDataLoader.getPrompt("toolRetrievalPrompt.txt")
        prompt = prompt.replace("{{AGENT_NAME}}", self.agent_name)
        prompt = prompt.replace("{{CONTEXT_HISTORY}}", str(self.parseSessionHistory(component.getSessionHistory(self.inputContext.getSessionId()))))
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
            if tool['id'] in self.available_tools:
                tool_description += "- Name : " + tool['name'] + " Description : " + tool['description'] + " Method: " + tool['method'] + " Parameters: " + str(tool['parameters']) + "\n"
        return tool_description

    def shutdown(self):
        self._terminate_condition_met = True
