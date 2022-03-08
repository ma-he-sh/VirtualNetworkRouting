import pickle
from modules.node import Node
import os.path
PIK = "session.dat"

class NodeHandler:
    def __init__(self, nodeArr, start ):
        self.nodeArr = nodeArr
        self.start   = start

    @staticmethod
    def saveNodes(nodeArr):
        with open( PIK, "wb" ) as f:
            pickle.dump( nodeArr, f )

    @staticmethod
    def getNodes():
        with open( PIK, "rb" ) as f:
            return pickle.load(f)

    @staticmethod
    def sessionExists(self):
        return os.path.exists( PIK )

    def generateContainers(self):
        if len(self.nodeArr) > 0:
            for node in self.nodeArr:
                node.create()