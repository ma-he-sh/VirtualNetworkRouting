import pickle
from modules.node import Node
import os.path

from modules.dockerize import Dockerize
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
    def sessionExists():
        return os.path.exists( PIK )

    def generateContainers(self):
        if len(self.nodeArr) > 0:
            routers = {}
            for node in self.nodeArr:
                entry, router = node.create() 
                routers[router] = entry

            # deploy containers
            docker = Dockerize( "session", routers )
            docker.generate()
            docker.exec()