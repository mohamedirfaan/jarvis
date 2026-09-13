from AgentBlueprints.OrchestratorAgent import OrchestratorAgent
from AgentBlueprints.registry.AgentComponentRegistry import AgentComponentRegistry
from AgentBlueprints.registry.AgentInputContext import AgentInputContext
from Agents.AIClient import AIClient
from adapters.AgentAdapter import AgentAdapter
from adapters.ToolAdapter import ToolAdapter
from dao.PlanStepDAO import PlanStepDAO
from dao.SessionDAO import SessionDAO


def createOrchestratorAgent(sessionId, agentName):
    inputContext = AgentInputContext()
    inputContext.setAgentName(agentName)
    inputContext.setSessionId(sessionId)
    orchestrator = OrchestratorAgent(inputContext)
    orchestrator.setRegistry(getOrchestratorRegistry())
    return orchestrator


def getOrchestratorRegistry():
    registry = AgentComponentRegistry()
    registry.registerComponent("SESSION_ADAPTER", SessionDAO())
    registry.registerComponent("PLAN_ADAPTER", PlanStepDAO())
    registry.registerComponent("AI_CLIENT_ADAPTER", AIClient())
    registry.registerComponent("TOOL_ADAPTER", ToolAdapter())
    registry.registerComponent("AGENT_ADAPTER", AgentAdapter())
    return registry

