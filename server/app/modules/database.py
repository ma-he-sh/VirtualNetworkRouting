import sqlite3
import uuid
from datetime import datetime

class DB:
    def __init__(self):
        self.conn = self.get_conn()

    def get_conn(self):
        self.conn = sqlite3.connect("database.db")
        self.row_factory = sqlite3.Row
        return self.conn

    def set(self, query):
        self.conn.execute(query)
        self.commit()
        self.conn.close()

    def get(self, query):
        data = self.conn.execute(query)
        self.conn.close()
        if data is None:
            return False
        return data

    def close(self):
        self.conn.close()

    def create_tables(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS sess(
        sessID text primary key,
        session_name text
        )''')
        self.conn.commit()

        self.conn.execute('''CREATE TABLE IF NOT EXISTS nodes(
        ID integer primary key,
        sessID int,
        nodeID int,
        nodeCost int,
        nodeIP text
        )''')
        self.conn.commit()

class NetworkDB(DB):
    def __init__(self):
        super().__init__()

    def create_node(self, sessID, nodeID, nodeCost, nodeIP ):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute("INSERT INTO nodes (sessID, nodeID, nodeCost, nodeIP) VALUES (?, ?)", (sessID, nodeID, nodeCost, nodeIP))
        conn.commit()
        conn.close()

    def create_session(self, sessID, sessName ):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO sess(sessID, session_name) VALUES (?, ?)", (sessID, sessName))
        conn.commit()
        conn.close()

    def delete_node(self, sessID, nodeID ):
        conn = self.get_conn()
        c = conn.cursor()
        c.execute("DELETE FROM nodes WHERE sessID=? AND nodeID=?;", (sessID, nodeID))
        conn.execute()
        conn.close()

    def delete_session(self, sessID ):
        conn = self.get_conn()
        c = conn.cursor()
        sql = "DELETE FROM sess WHERE sessID='{sessID}'".format(sessID=sessID)
        c.execute(sql)
        conn.commit()

        sql = "DELETE FROM nodes WHERE sessID='{sessID}'".format(sessID=sessID)
        c.execute(sql)
        conn.commit()

        conn.close()