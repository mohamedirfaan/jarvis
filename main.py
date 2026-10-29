from agent_blueprints.registry.agent_factory import *


print("main started")
orchestrator = createOrchestratorAgent(1, "jarvis")
sessionDAO = SessionDAO()
sessionDAO.updateStatus(1, "planning")
orchestrator.run()
orchestrator.shutDown()


print("main finished")