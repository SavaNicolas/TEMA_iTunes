import copy

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

        ##parte 2
        self._bestSet = {}
        self._maxLen = 0

    def buildGraph(self,durataMin):
        self._grafo.clear()
        self._nodi = DAO.getNodes(durataMin)  # retailer presi in base alla nazionalità
        # aggiungiamo i nodi(li ho nelle fermate)
        self._grafo.add_nodes_from(self._nodi)
        # aggiungo archi
        self._idAlbumScelti = {n.AlbumId: n for n in self._nodi}
        self.addEdges(self._idAlbumScelti)

    def addEdges(self,nodi):
        """
        Due album a1 e a2 sono collegati tra loro se
almeno una canzone di a1 e una canzone di a2
sono state inserite da un utente all’interno di
una stessa playlist (tabella PlaylistTrack).
        """

        edges= DAO.getAllEdges(nodi) #[(u,v),(z,v)]
        self._grafo.add_edges_from(edges)

#metodi che devono esserci sempre
    def getNumNodi(self):
        return len(self._grafo.nodes())

    def getNumArchi(self):
        return len(self._grafo.edges())

    def getAllNodes(self):
        return self._nodi
        #return list(self._grafo.nodes())

    def getGraph(self):
        return self._grafo

    def getInfoConnessa(self,a1):
        """
• la dimensione della componente connessa a cui appartiene a1;
• la durata complessiva (in minuti) di tutti gli album appartenenti alla componente connessa di a1.
        """
        #componente connessa: l’insieme di tutti i nodi del grafo che sono raggiungibili da quel nodo tramite uno o più archi
        cc=nx.node_connected_component(self._grafo,a1) #dal nodo e il grafo, e ti restituisce la componente connessa che contiene a1
        return len(cc), self._getDurataTot(cc)


    ###parte 2#######

    def getSetOfNodes(self,a1,soglia):
        """
utilizzare un algoritmo ricorsivo per estrarre un set di album dal grafo che abbia le seguenti caratteristiche:
• includa a1;
• includa solo album appartenenti alla stessa componente connessa di a1;
• includa il maggior numero possibile di album;
• abbia una durata complessiva, definita come la somma della durata degli album in esso contenuti, non superiore dTOT.
        """
        self._bestSet = {}
        self._maxLen = 0

        parziale = [a1] #parziale deve per forza avere a1
        cc = nx.node_connected_component(self._grafo, a1) #includa solo album appartenenti alla stessa componente connessa di a1; #questo è un set
        cc.pop(a1) #perchè noi iteriamo su cc e non ci serve a1, che sta già in parziale
        for n in cc:
            #richiamo la mia ricorsione
            parziale.append(n) #appendo n
            cc.remove(n) #lo rimuovo dalla lista di componenti connesse
            self._ricorsione(parziale,cc,soglia)
            # backtraking
            parziale.pop(n)#rimuovo il nodo da parziale
            cc.add(n)#rimetto il nodo nei possibili

        return self._bestSet, self._getDurataTot(self._bestSet)

    def _ricorsione(self, parziale,rimanenti,soglia):
        #1)verifico che parziale sia ammissibili, ovvero viola i vincoli(terminazione)
        if self._getDurataTot(parziale) > soglia:#se ho già superato la soglia ho finito
            return
        #2)se è minore della soglia:verifico se è migliore di quella che ho trovato(non ho limite di quante cose aggiungere)
        if len(parziale)> self._maxLen:
            self._maxLen = len(parziale)
            self._bestSet = copy.deepcopy(parziale)
            #non deve interrompere quindi non metto return
        #ricorsione
        for n in rimanenti:
            if n not in parziale:
                # richiamo la mia ricorsione
                parziale.append(n)  # appendo n
                rimanenti.remove(n)  # lo rimuovo dalla lista di componenti connesse
                self._ricorsione(parziale, rimanenti, soglia)
                # backtraking
                parziale.pop(n)  # rimuovo il nodo da parziale
                rimanenti.add(n)  # rimetto il nodo nei possibili

    def _getDurataTot(self,listaDiNodi):
        sumDurata=0
        for n in listaDiNodi:
            sumDurata+=n.dTot
        return sumDurata

