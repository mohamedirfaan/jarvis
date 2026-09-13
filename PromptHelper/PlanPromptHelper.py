from adapters.PlanAdapter import PlanAdapter
from adapters.Plan import Plan
def buildToolDescriptions(toolAdapter):
    toolDescription = ""
    for tool in toolAdapter.getTools():
        toolDescription += "- Name : " + tool.getName() + " Description : " + tool.getDescription() + "\n"
    return toolDescription

def buildAgentDescriptions(agentAdapter, associated_agents):
    agentDescriptions = ""
    for agent in agentAdapter.getAgents():
        if agent.getAgentId() in associated_agents:
            agentDescriptions += "- Name : "+ agent.getName() + " Description : " + agent.getDescription() + "\n"
    return agentDescriptions

def parseSessionHistory(sessionHistory):
    history = []
    for session in sessionHistory:
        currHistory = {"message": session[3], "context_type": session[2]}
        history.append(currHistory)
    return history

class PlanPromptHelper:
    def __init__(self):
        self.planPromptPath = "C:\\Code\\Jarvis\\prompts\\planning_prompt.txt"

    def generatePlanningPrompt(self, sessionId, context, toolAdapter, agentAdapter, associated_agents):
        promptTemplate = ""
        with open(self.planPromptPath, "r") as f:
            promptTemplate += str(f.readlines())


        promptTemplate = promptTemplate.replace("{{AVAILABLE_AGENTS}}", buildAgentDescriptions(agentAdapter, associated_agents))
        promptTemplate = promptTemplate.replace("{{AVAILABLE_TOOLS}}", buildToolDescriptions(toolAdapter))
        promptTemplate = promptTemplate.replace("{{CONTEXT_HISTORY}}", str(parseSessionHistory(context.getSessionHistory(sessionId))))
        print("Prompt Template:", promptTemplate)
        return promptTemplate

    def parsePlanStepsAndGetPlanAdapter(self, steps):
        planAdapter = PlanAdapter()
        for step in steps:
            step_order = step['step_order']
            step_type = step['step_type']
            name = step['name']
            inputs = None
            if step_type == 'tool':
                inputs = step['input']
            plan = Plan(step_order, step_type, name, inputs)
            planAdapter.addPlanStep(plan)
        return planAdapter


