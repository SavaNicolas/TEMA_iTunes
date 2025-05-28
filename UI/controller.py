import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._prodottoScelto = None

    def handleCreaGrafo(self, e):
        #leggi la durata minima
        dMinTxt= self._view._txtInDurata.value #str

        if dMinTxt is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("attenzione valore non inserito"))
            self._view.update_page()
            return

        try:
            dMin= int(dMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("valore inserito non è numerico"))
            self._view.update_page()
            return


        self._model.buildGraph(dMin)
        #posso riempire tendina
        self._fillDD(self._model.getAllNodes())
        self._view.update_page()

        # stampo txt result
        self._view.txt_result.controls.append(ft.Text("grafo correttamente creato"))
        self._view.txt_result.controls.append(
            ft.Text(f"il grafo ha {self._model.getNumNodi()} nodi e {self._model.getNumArchi()} archi"))
        self._view.update_page()



    def getSelectedAlbum(self, e):
        #trova prodotto scelto, la soglia e poi chiamo ricorsione
        sogliaTxt = self._view._txtInSoglia.value
        if sogliaTxt is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("valore soglia non inserito"))
            self._view.update_page()
            return
        try:
            soglia = int(sogliaTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("inserire un valore intero"))
            self._view.update_page()
            return

        if self._prodottoScelto is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("valore soglia non inserito"))
            self._view.update_page()
            return

        path,durata=  self.model.getSetOfNodes(self._prodottoScelto,soglia)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"dimensione: {len(path)}. durata: {durata}"))
        for n in path:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()

    def handleAnalisiComp(self, e):

        if self._prodottoScelto is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(value="Attenzione, album non selezionato.", color="red")
            )
            return

        size,dTotCC=self._model.getInfoConnessa(self._prodottoScelto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(
            f"La componente connessa che contiene {self._prodottoScelto} "
            f"ha {size} nodi e una durata totale di {dTotCC} minuti"))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        pass

    def _fillDD(self,nodi):
        for album in nodi:  # sto appendendo al dropdown l'oggetto reatiler
            self._view._ddAlbum.options.append(
                ft.dropdown.Option(key=album.AlbumId,  # 🔑 Chiave univoca dell'opzione
                                   text=album.Title,  # 🏷️ Testo visibile nel menu a tendina
                                   data=album,
                                   # 📦 Oggetto completo, utile per accedere a tutti gli attributi dopo la selezione
                                   on_click=self.read_album))  # salvati l'oggetto da qualche parte

    def read_album(self, e):
        if e.control.data is None:
            print("errore nella scelta")
        self._prodottoScelto = e.control.data  # l'abbiamo inizializzata a None
        # e.control.data è il risultato di onclick sopra
