import importlib
from agent_blueprints.orchestrator_agent import OrchestratorAgent
from agent_blueprints.registry.agent_component_registry import AgentComponentRegistry
from agent_blueprints.registry.agent_input_context import AgentInputContext
from ai_clients.ai_client import AIClient
from adapters.agent_adapter import AgentAdapter
from adapters.tool_adapter import ToolAdapter
from repositories.execution_repository import ExecutionDAO
from repositories.plan_step_repository import PlanStepDAO
from repositories.session_repository import SessionDAO


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