import importlib
from AgentBlueprints.OrchestratorAgent import OrchestratorAgent
from AgentBlueprints.registry.AgentComponentRegistry import AgentComponentRegistry
from AgentBlueprints.registry.AgentInputContext import AgentInputContext
from Agents.AIClient import AIClient
from adapters.AgentAdapter import AgentAdapter
from adapters.ToolAdapter import ToolAdapter
from dao.ExecutionDAO import ExecutionDAO
from dao.PlanStepDAO import PlanStepDAO
from dao.SessionDAO import SessionDAO


def createOrchestratorAgent(sessionId, agentName):
    execution_adapter = ExecutionDAO()
    agent_id = execution_adapter.createAgentExecution(agentName, "planning")[0][0]
    inputContext = AgentInputContext()
    inputContext.setAgentName(agentName)
    inputContext.setSessionId(sessionId)
    inputContext.setAgentId(agent_id)
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
    registry.registerComponent("EXECUTION_ADAPTER", ExecutionDAO())
    return registry


def createWorkerAgent(sessionId, parentAgentId, step):
    execution_adapter = ExecutionDAO()
    agent_id = execution_adapter.createAgentExecution(step.getName(), 'running', parent_agent_id=parentAgentId)[0][0]
    inputContext = AgentInputContext()
    inputContext.setAgentName(step.getName())
    inputContext.setSessionId(sessionId)
    inputContext.setAgentId(agent_id)

    agent_class = getattr(importlib.import_module(step.getClassName()), step.getName())
    workerAgent = agent_class(inputContext)
    workerAgent.setRegistry(getWorkerAgentRegistry())
    return workerAgent

def getWorkerAgentRegistry():
    registry = AgentComponentRegistry()
    registry.registerComponent("SESSION_ADAPTER", SessionDAO())
    registry.registerComponent("AI_CLIENT_ADAPTER", AIClient())
    registry.registerComponent("EXECUTION_ADAPTER", ExecutionDAO())
    registry.registerComponent("TOOL_ADAPTER", ToolAdapter())
    return registry