
class Node:
    def __init__(self, node_id, ip, cost=0):
        self.node_id = node_id
        self.ip = ip
        self.cost = cost

    def create(self):
        """
        Create Node
        :return:
        """
        pass

    def destroy(self):
        """
        destory Node
        :return:
        """
        pass

    def getIP(self):
        return self.ip

    def getCost(self):
        return self.cost

    def getNodeID(self):
        return self.node_id

