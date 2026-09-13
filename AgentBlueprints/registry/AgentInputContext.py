class AgentInputContext:
    def __init__(self):
        self.__sessionId = None
        self.__agentName = None

    def setSessionId(self, sessionId):
        self.__sessionId = sessionId

    def setAgentName(self, agentName):
        self.__agentName = agentName

    def getAgentName(self):
        return self.__agentName

    def getSessionId(self):
        return self.__sessionId
