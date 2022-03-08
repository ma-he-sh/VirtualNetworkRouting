from platform import node
from modules.node import Node
import networkx as net

class NegativeCycles(Exception):
    pass

class Graphs:
    def __init__(self, nodes, nodeComb ):
        self.nodes = nodes
        self.nodeComb = nodeComb
        self.graph = net.Graph()
        self.num_vertex = len(self.nodes)
        self.solution = {}

    def _prepareNodes(self):
        for key in self.nodeComb:
            if key['cost'] is not None:
                self.graph.add_edge( key['node1'], key['node2'], weight=key['cost'] )

    def getNodes(self):
        return self.nodes

    def getCosts(self):
        return self.costs

    def get_solution(self, start, end ):
        self._prepareNodes()
        path = net.shortest_path(self.graph, start, end, weight='weight')

        nodeArr = []
        index = 20 # padding for ip
        i = 0

        if len(path) > 1:
            # add observation node
            path.append("OBSERVER")
            while ( i < len(path) - 1 ):
                nodeObj = Node( index, path[i], path[i+1] )
                nodeArr.append(nodeObj)
                i+=1

        return path, nodeArr