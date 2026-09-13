from DBUtil import DBUtil
class SessionHistoryDAO:
    def __init__(self):
        self.db = DBUtil()

    def addChatToHistory(self, chat):