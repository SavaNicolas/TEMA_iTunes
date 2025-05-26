import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._albumsAll = DAO.getAllAlbums() # lista con tutti i retailer
        # creo grafo
        self._grafo = nx.Graph()  # semplice, non orientato e pesato
        # mappa di oggetti
        self.idAlbums = {}
        for p in self._albumsAll:
            self.idAlbums[p.AlbumId] = p

        self._nodi= None

    def buildGraph(self,durataMin,anno):
        self._grafo.clear()
        self._nodi = self.getNodes(durataMin)  # retailer presi in base alla nazionalità
        # aggiungiamo i nodi(li ho nelle fermate)
        self._grafo.add_nodes_from(self._nodi)
        # aggiungo archi
        self.addEdges(anno,self.idAlbums)

    def addEdges(self,anno,idMap):
        """
        Due album a1 e a2 sono collegati tra loro se
almeno una canzone di a1 e una canzone di a2
sono state inserite da un utente all’interno di
una stessa playlist (tabella PlaylistTrack).
        """
        edges= DAO.getAllEdges(idMap)
        self._grafo.add_edges_from(edges)

#metodi che devono esserci sempre
    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())

    def getNodi(self):
        return self._nodi
        #return list(self._grafo.nodes())

    def getGraph(self):
        return self._grafo