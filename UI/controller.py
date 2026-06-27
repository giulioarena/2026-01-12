import flet as ft
import networkx as nx


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDAnni(self):
        anni = self._model.getAllYears()
        anniDD = [ft.dropdown.Option(a) for a in anni]
        self._view._ddAnno1.options = anniDD
        self._view._ddAnno2.options = anniDD

    def handleCreaGrafo(self,e):
        self._view.txt_result.controls.clear()
        if self._view._ddAnno1.value is None or self._view._ddAnno2.value is None or int(self._view._ddAnno1.value)>int(self._view._ddAnno2.value):
            self._view.txt_result.controls.append(ft.Text(f"Inserire un range corretto", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(int(self._view._ddAnno1.value), int(self._view._ddAnno2.value))
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente.\nNumero nodi: {len(self._model.graph.nodes)}, numero archi: {len(self._model.graph.edges)}"))
        self._view.update_page()

    def handleDettagli(self, e):

        self._view.txt_result.controls.append(ft.Text(f"\nI 3 archi di peso maggiore sono:", color="blue"))
        for e in self._model.get3Heaviest():
            self._view.txt_result.controls.append(ft.Text(f"{e[0]} --> {e[1]} | {e[2]["weight"]}"))

        self._view.txt_result.controls.append(ft.Text(f"\nIl numero di componenti connesse è {len(list(nx.connected_components(self._model.graph)))}", color="blue"))

        nodesBiggestCC = self._model.getBiggestCC()
        self._view.txt_result.controls.append(ft.Text(f"\n La componente connessa più grande ha {len(nodesBiggestCC)} nodi.", color="blue"))
        for n in nodesBiggestCC:
            self._view.txt_result.controls.append(ft.Text(f"{n[0]}, grado: {n[1]}"))

        self._view.update_page()


    def handleCerca(self, e):
        self._view.txt_result.controls.clear()
        try:
            K = int(self._view._txtInK)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text(f"Inserire un numero intero", color="red"))
            return
        if K is None or K>len(list(nx.connected_components(self._model.graph))):
            self._view.txt_result.controls.append(ft.Text(f"Inserire un numero intero <= del numero di componenti connesse del grafo", color="red"))
            return



