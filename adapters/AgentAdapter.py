from cache import ToolDataLoader
from . import Agent
import json


class AgentAdapter:
    def __init__(self):
        self.agents = None
        self.cachedAgentNames = None
        self.initialize()

    def addAgent(self, agent):
        self.agents.append(agent)

    def removeAgent(self, agent):
        self.agents.remove(agent)

    def getAgentNames(self):
        if self.cachedAgentNames is None:
            self.cachedAgentNames = [agent.name for agent in self.agents]
        return self.cachedAgentNames

    def getAgents(self):
        return self.agents

    def initialize(self):
        self.agents = []
        tools_dict = ToolDataLoader.getToolData()
        simple_agents = tools_dict["agents"]
        for simple_agent in simple_agents:
            agentId = simple_agent["id"]
            name = simple_agent["name"]
            description = simple_agent["description"]
            tools = simple_agent["tools"]
            self.addAgent(Agent.Agent(agentType="simpleAgent", agentId=agentId, name=name, description=description, associated_agents=None, associated_tools=tools))

    def invalidateCaches(self):
        self.cachedAgentNames = None