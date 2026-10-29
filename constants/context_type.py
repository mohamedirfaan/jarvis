from enum import Enum

class ContextType(Enum):
    USER = 1
    AGENT_SPAWN = 2
    TOOL_CALL = 3
    ASSISTANT = 4
    TOOL_RESULT = 5