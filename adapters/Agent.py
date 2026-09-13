class Agent:
    def __init__(self, agentType, agentId, name, description, associated_agents, associated_tools):
        self.agentType = agentType
        self.agentId = agentId
        self.name = name
        self.description = description
        self.associated_agents = associated_agents
        self.associated_tools = associated_tools

    def getName(self):
        return self.name

    def getDescription(self):
        return self.description

    def getAssociatedAgents(self):
        return self.associated_agents

    def getAssociatedTools(self):
        return self.associated_tools

    def getAgentId(self):
        return self.agentId