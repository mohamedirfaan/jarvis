class Chat:
    def __init__(self, messageId, sessionId, context_type, message, created_at):
        self.messageId = messageId
        self.sessionId = sessionId
        self.context_type = context_type
        self.message = message
        self.created_at = created_at

    def getMessageId(self):
        return self.messageId
    def getSessionId(self):
        return self.sessionId
    def getContextType(self):
        return self.context_type
    def getMessage(self):
        return self.message
    def getCreatedAt(self):
        return self.created_at