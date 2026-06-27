import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.idMapConstructors = {}
        self.graph = nx.Graph()

    def getAllYears(self):
        return DAO.getAllYears()

    def buildGraph(self, minY: int, maxY: int):
        self.graph.clear()
        constructors = DAO.getConstructors(minY, maxY)
        self.graph.add_nodes_from(constructors)
        self.idMapConstructors = {}
        for constructor in constructors:
            self.idMapConstructors[constructor.constructorId] = constructor

        edges = DAO.getEdges(minY, maxY, self.idMapConstructors)
        self.graph.add_weighted_edges_from(edges)

    def get3Heaviest(self):
        edges = list(self.graph.edges(data=True))
        edges.sort(key=lambda x: x[2]["weight"], reverse=True)
        return edges[:3]

    def getBiggestCC(self):
        largestCC = max(nx.connected_components(self.graph), key=len)
        result = []
        for n in largestCC:
            result.append((n, self.graph.degree[n]))

        result.sort(key=lambda x: x[1], reverse=True)
        return result





