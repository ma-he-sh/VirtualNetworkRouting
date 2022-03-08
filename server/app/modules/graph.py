from modules.node import Node
import networkx

class NegativeCycles(Exception):
    pass

class Graphs:
    def __init__(self, nodes, nodeComb ):
        self.nodes = nodes
        self.nodeComb = self._prepareNodes( nodeComb )
        self.num_vertex = len(self.nodes)
        self.solution = {}

    def _prepareNodes(self, nodeComb):
        nodeArr = []
        for key in nodeComb:
            if key['cost'] is not None:
                nodeObj = Node( key['node1'], key['node2'], key['cost'] )
                nodeArr.append( nodeObj )
        return nodeArr

    def getNodes(self):
        return self.nodes

    def getCosts(self):
        return self.costs

    def get_solution(self, start_node):
        # bellman ford distance calculation
        # 1 assign infinity as the default distance
        #self.solution = {} # stores the distance
        #if self.num_vertex <= 0: return False

        # for node in self.nodes:
        #     self.solution[node] = float("Inf")

        # self.solution[start_node] = 0

        # for vertex in range(self.num_vertex - 1):
        #     for node in self.nodeComb:
        #         start = node.getStart()
        #         end   = node.getEnd()
        #         cost  = node.getCost()

        #         if self.solution[ start ] != float("Inf") and self.solution[ start ] + cost < self.solution[ end ]:
        #             self.solution[ end ] = self.solution[ start ] + cost

        # print(self.solution)

        # # determine if graph contains negative edges
        # for node in self.nodeComb:
        #     start = node.getStart()
        #     end   = node.getEnd()
        #     cost  = node.getCost()

        #     if self.solution[ start ] != float("Inf") and self.solution[ start ] + cost < self.solution[ end ]:
        #         raise NegativeCycles('Contain negative cycles')



        return self.solution
    
    def getSolution(self):
        return self.solution