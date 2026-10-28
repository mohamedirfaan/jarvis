from adapters.PlanAdapter import PlanAdapter
from adapters.Plan import Plan
import cache.ToolDataLoader

def buildToolDescriptions(toolAdapter, associated_tools):
    toolDescription = ""
    for tool in toolAdapter.getTools().values():
        if tool.getToolId() in associated_tools:
            toolDescription += "- Name : " + tool.getName() + " Description : " + tool.getDescription() + " Method: " + tool.getMethod() + " Parameters: " + str(tool.getParameters()) + "\n"
    return toolDescription

def buildAgentDescriptions(agentAdapter, associated_agents):
    agentDescriptions = ""
    for agent in agentAdapter.getAgents():
        if agent.getAgentId() in associated_agents:
            agentDescriptions += "- Name : "+ agent.getName() + " Description : " + agent.getDescription() + " Class Name: " + agent.getClassName() + "\n"
    return agentDescriptions

class PlanPromptHelper:
    def __init__(self):
        self.planPromptPath = "C:\\Code\\Jarvis\\prompts\\planning_prompt.txt"

    def generatePlanningPrompt(self, toolAdapter, agentAdapter, associated_agents, associated_tools):
        promptTemplate = cache.ToolDataLoader.getPrompt("planning_prompt.txt")


        promptTemplate = promptTemplate.replace("{{AVAILABLE_AGENTS}}", buildAgentDescriptions(agentAdapter, associated_agents))
        promptTemplate = promptTemplate.replace("{{AVAILABLE_TOOLS}}", buildToolDescriptions(toolAdapter, associated_tools))
        print("Planning prompt: ", promptTemplate)
        return promptTemplate

    def parsePlanStepsAndGetPlanAdapter(self, steps):
        planAdapter = PlanAdapter()
        for step in steps:
            step_order = step['step_order']
            step_type = step['step_type']
            name = step['name']
            inputs = None
            method_name = None
            class_name = None
            if step_type == 'tool':
                inputs = step['input']
                method_name = step['method']
            else:
                class_name = step['agent_class']
            plan = Plan(step_order, step_type, name, inputs, method_name, class_name)
            planAdapter.addPlanStep(plan)
        return planAdapter


