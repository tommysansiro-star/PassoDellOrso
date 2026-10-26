import os
import pickle
from datetime import datetime
from models.ordine import Ordine
from models.prodotto_ordine import ProdottoOrdine
from models.enums import StatoOrdine
from controllers.gestore_mail import GestoreMail
from controllers.gestore_prodotti import GestoreProdotti

class GestoreOrdini:
    def __init__(self, gestore_mail: GestoreMail, gestore_prodotti: GestoreProdotti):
        self._ordini = []

        self._gestore_mail = gestore_mail
        self._gestore_prodotti = gestore_prodotti

        self._file_path = "data/ordini.pickle"
        self._carica_dati()

    def MetodoPagamentoValido(self, metodo_pagamento) -> bool:
        """Verifica la validità della carta"""
        return True

    def selezionaMetodoPagamento(self, metodo_pagamento) -> None:
        """Imposta il metodo di pagamento per il checkout in corso."""
        pass

    def validaDati(self, prodotti_ordine: list) -> None:
        """Verifica la coerenza dei prodotti prima di confermare l'ordine."""
        if not prodotti_ordine:
            raise ValueError("L'ordine non contiene prodotti validi.")

    def richiestaOrdine(self, cliente, carrello: list, metodo_pagamento) -> None:
        """Trasforma il carrello in un ordine effettivo."""
        if not carrello:
            raise ValueError("Il carrello è vuoto.")

        if not self.MetodoPagamentoValido(metodo_pagamento):
            raise ValueError("Metodo di pagamento non valido o rifiutato.")

        nuovo_id = 1 if not self._ordini else max(o.id_ordine for o in self._ordini) + 1

        self.validaDati(carrello)

        prezzo_totale = sum(item.prodotto.prezzo * item.quantita for item in carrello)

        for item in carrello:
            prodotto_catalogo = self._gestore_prodotti.getProdottoById(item.prodotto.id_prodotto)
            if prodotto_catalogo:
                if hasattr(prodotto_catalogo, 'quantita'):
                    if prodotto_catalogo.quantita >= item.quantita:
                        prodotto_catalogo.quantita -= item.quantita
                        if prodotto_catalogo.quantita == 0:
                            prodotto_catalogo.is_disponibile = False
                    else:
                        raise ValueError(f"Prodotto {prodotto_catalogo.nome} esaurito prima del checkout.")

        self._gestore_prodotti._salva_dati()

        prodotti_ordine = [ProdottoOrdine(item.prodotto, item.quantita) for item in carrello]
        nuovo_ordine = Ordine(nuovo_id, metodo_pagamento, prezzo_totale, prodotti_ordine)
        self.aggiungiOrdine(nuovo_ordine)

        cliente.aggiungi_ordine(nuovo_ordine)

        self._gestore_mail.inviaMailConferma(cliente.email, nuovo_ordine)

        cliente.svuota_carrello()

    def aggiungiOrdine(self, ordine) -> None:
        """Aggiunge l'ordine finalizzato alla lista e lo salva."""
        self._ordini.append(ordine)
        self._salva_dati()

    def visualizzaOrdine(self, id_ordine: int):
        """Restituisce l'ordine specifico per i dettagli."""
        for ordine in self._ordini:
            if ordine.id_ordine == id_ordine:
                return ordine
        return None

    def getOrdiniCliente(self, cliente) -> list:
        """Restituisce lo storico degli ordini di un determinato cliente."""
        return cliente.ordini

    def richiediInformazioniOrdine(self, id_oridne: int) -> None:
        """Logica per richiedere info al supporto o tracciamento."""
        pass

    def richiediModifica(self, id_ordine: int) -> None:
        """Verifica se l'ordine è in uno stato modificabile."""
        ordine = self.visualizzaOrdine(id_ordine)
        if not ordine:
            raise ValueError("Ordine non trovato.")

    def inviaDatiModifica(self, id_ordine: int, prodotti_ordine: list) -> None:
        """Applica le modifiche ai prodotti dell'ordine e salva."""
        ordine = self.visualizzaOrdine(id_ordine)
        if ordine:
            ordine.set_prodotti(prodotti_ordine)
            ordine.calcola_prezzo_totale()
            self._salva_dati()

    def richiediRimborso(self, id_ordine: int, motivazione: str) -> bool:
        """Scatena la transizione di stato da Completato a Rimborso Richiesto."""
        ordine = self.visualizzaOrdine(id_ordine)
        if ordine:
            ordine.stato = StatoOrdine.RIMBORSO_RICHIESTO
            #ordine.note = motivazione
            self._salva_dati()
            return True
        return False

    def gestisciRimborso(self, id_ordine: int, approvato: bool) -> None:
        """Scatena la transizione finale del rimborso"""
        ordine = self.visualizzaOrdine(id_ordine)
        if ordine:
            if approvato:
                ordine.stato = StatoOrdine.RIMBORSO_COMPLETATO
            else:
                ordine.stato = StatoOrdine.COMPLETATO

            self._salva_dati()

    def _salva_dati(self):
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, "wb") as f:
            pickle.dump(self._ordini, f)

    def _carica_dati(self):
        if os.path.exists(self._file_path):
            with open(self._file_path, "rb") as f:
                self._ordini = pickle.load(f)
