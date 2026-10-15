from dao.DBUtil import DBUtil


class ExecutionDAO:
    def __init__(self):
        self.db = DBUtil()

    def createAgentExecution(self, agent_name, execution_status = "running", parent_agent_id = None):
        if parent_agent_id is not None:
            query = "insert into execution(name, execution_status, parent_agent_id) values (%s, %s, %s) returning id"
            return self.db.execute_query(query, (agent_name, execution_status, parent_agent_id))
        else:
            query = "insert into execution(name, execution_status) values (%s, %s) returning id"
            return self.db.execute_query(query, (agent_name, execution_status))

    def updateAgentExecutionStatus(self, agent_id, execution_status):
        try:
            query = "update execution set execution_status = %s where id = %s"
            return self.db.execute_query(query, (execution_status, agent_id))
        except Exception as e:
            print(e)

    def getExecutionStatus(self, agent_id):
        try:
            query = "select execution_status from execution where id = %s"
            return self.db.execute_query(query, (agent_id,))
        except Exception as e:
            print(e)

    def deleteAgentExecution(self, agentId):
        query = "delete from execution where id = %s"
        return self.db.execute_query(query, (agentId, ))