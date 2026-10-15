import json
from adapters.Tool import Tool
from cache import ToolDataLoader


class ToolAdapter:
    def __init__(self):
        self.tools = None
        self.cachedToolNames = None
        self.initialize()

    def addTool(self, tool):
        self.tools[tool.getName()] = tool
        self.invalidateCaches()

    def removeTool(self, tool):
        self.tools.pop(tool.getName(), None)
        self.invalidateCaches()

    def invalidateCaches(self):
        self.cachedToolNames = None

    def getToolNames(self):
        if self.cachedToolNames is None:
            self.cachedToolNames = [tool.getName() for tool in self.tools]
        return self.cachedToolNames

    def getTools(self):
        return self.tools

    def getTool(self, toolName):
        return self.tools[toolName]

    def initialize(self):
        self.tools = {}
        tools_dict = ToolDataLoader.getToolData()
        tools_dict = tools_dict["tools"]
        for tool in tools_dict:
            toolId = tool["id"]
            name = tool["name"]
            description = tool["description"]
            module = tool["module"]
            method = tool["method"]
            className = tool["class"]
            parameters = tool["parameters"]
            self.addTool(Tool(toolId, name, description, module, className, method, parameters))
        print("tools initialized")
