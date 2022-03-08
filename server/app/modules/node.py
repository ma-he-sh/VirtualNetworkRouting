import yaml
ipStart = "172.16.238."


class Node:
    def __init__(self, start, end, cost=0):
        self.start = start
        self.end   = end
        self.cost  = cost

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getCost(self):
        return self.cost

    

# class Node:
#     def __init__(self, index, node_name, cost=0):
#         self.index = index
#         self.node_name = node_name
#         self.cost = cost

#     def create(self):
#         """
#         Create Node
#         :return:
#         """
#         pass

#     def destroy(self):
#         """
#         destory Node
#         :return:
#         """
#         pass

#     def getNodeName(self):
#         return "node_" + str(self.index)

#     def getIP(self):
#         return ipStart + str( 10 + self.index )

#     def getCost(self):
#         return self.cost

#     def getNodeID(self):
#         return self.node_id

#     def writeToContainer(self):
#         pass
