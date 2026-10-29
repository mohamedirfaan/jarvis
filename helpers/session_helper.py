from adapters.tool_adapter import ToolAdapter
from constants.context_type import ContextType
def parseSessionHistory(sessionHistory):
    history = []
    for session in sessionHistory:
        currHistory = {"content": session[2]}
        role = session[4]
        if role == ContextType.TOOL_CALL.value or role == ContextType.TOOL_RESULT.value:
            currHistory["role"] = "function"
            currHistory["name"] = session[2]
        elif role == ContextType.AGENT_SPAWN.value:
            currHistory["role"] = "tool"
            currHistory["tool_call_id"] = ToolAdapter().getToolId(session[2])
        elif role == ContextType.ASSISTANT.value:
            currHistory["role"] = "assistant"
        elif role == ContextType.USER.value:
            currHistory["role"] = "user"
        history.append(currHistory)
    return history


class SessionHelper:
    def __init__(self, sessionAdapter):
        self.adapter = sessionAdapter

    def getSessionHistory(self, sessionId):
        return parseSessionHistory(self.adapter.getSessionHistory(sessionId))