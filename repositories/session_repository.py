import time
from repositories.database_util import DBUtil


class SessionDAO:
    def __init__(self):
        self.db = DBUtil()

    def getSessionHistory(self, sessionId):
        query = "select * from session_history WHERE session_id=%s order by created_at"
        return self.db.execute_query(query, (sessionId, ))

    def addSessionHistoryEntry(self, sessionId, role, content):
        query = "INSERT INTO session_history(session_id, role, content) values(%s, %s, %s) returning id"
        return self.db.execute_query(query, (sessionId, role, content, ))

    def createSession(self, session_name):
        query = "INSERT INTO sessions(session_name) values(%s) RETURNING id"
        return self.db.execute_query(query, (session_name, ))

    def updateSession(self, session_id, session_name):
        query = "UPDATE sessions SET session_name=%s, updated_at=%s WHERE id=%s"
        return self.db.execute_query(query, (session_name, int(time.time()), session_id))

    def getStatus(self, session_id):
        query = "SELECT status FROM sessions WHERE id=%s"
        return self.db.execute_query(query, (session_id, ))

    def updateStatus(self, session_id, status):
        query = "UPDATE sessions SET status=%s WHERE id=%s RETURNING status"
        return self.db.execute_query(query, (status, session_id))