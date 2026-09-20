class AgentInputContext:
    def __init__(self):
        self.__sessionId = None
        self.__agentName = None
        self.__agentId = None

    def setSessionId(self, sessionId):
        self.__sessionId = sessionId

    def setAgentName(self, agentName):
        self.__agentName = agentName

    def setAgentId(self, agentId):
        self.__agentId = agentId

    def getAgentName(self):
        return self.__agentName

    def getSessionId(self):
        return self.__sessionId

    def getAgentId(self):
        return self.__agentId