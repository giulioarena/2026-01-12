import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.idMapConstructors = {}
        self.graph = nx.Graph()

        self._bestSol = []
        self._bestObj = 10000000

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

    def getSetConstructors(self, minY: int, maxY: int, K):
        self._bestSol = []
        self._bestObj = 10000000
        parziale = []
        l = 0
        componenti= list(nx.connected_components(self.graph))
        DAO.setOldestDOB(minY, maxY, self.idMapConstructors)
        self.ricorsione(parziale, K, componenti, l)

        return self._bestSol


    def ricorsione(self, parziale, K, componenti, l):
        if len(parziale) == K:
            if self.obj(parziale)<self._bestObj:
                self._bestObj = self.obj(parziale)
                self._bestSol = copy.deepcopy(parziale)
            return

        if len(parziale)>0:
            if self.obj(parziale) > self._bestObj:
                return
        if l>=len(componenti):
            return

        for n in componenti[l]:
            parziale.append(n)
            self.ricorsione(parziale, K, componenti, l+1)
            parziale.pop()

        self.ricorsione(parziale, K, componenti, l)



    def obj(self, sol):
        sol1 = sorted(sol, key=lambda x: x.oldest_driver_dob)
        return sol1[-1].oldest_driver_dob - sol1[0].oldest_driver_dob







