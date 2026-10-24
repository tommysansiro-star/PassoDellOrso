from datetime import datetime
from typing import List
from models.prodotto_ordine import ProdottoOrdine
from models.metodo_pagamento import MetodoPagamento
from models.enums import StatoOrdine

class Ordine:
    def __init__(self, id_ordine: int, prodotti: List[ProdottoOrdine],
                 metodo_pagamento: MetodoPagamento, stato: StatoOrdine = StatoOrdine.IN_CORSO):
        self._id_ordine = id_ordine
        self._data_creazione = datetime.now()
        self._prodotti = prodotti
        self._metodo_pagamento = metodo_pagamento
        self._stato = stato
        self._prezzo_totale = self.calcola_totale()

    @property
    def id_ordine(self) -> int:
        return self._id_ordine

    @property
    def data_creazione(self) -> datetime:
        return self._data_creazione

    @property
    def prodotti(self) -> List[ProdottoOrdine]:
        return self._prodotti

    @prodotti.setter
    def prodotti(self, lista_prodotti: List[ProdottoOrdine]):
        self._prodotti = lista_prodotti
        self._prezzo_totale = self.calcola_totale()

    @property
    def metodo_pagamento(self) -> MetodoPagamento:
        return self._metodo_pagamento

    @metodo_pagamento.setter
    def metodo_pagamento(self, metodo: MetodoPagamento):
        self._metodo_pagamento = metodo

    @property
    def stato(self) -> StatoOrdine:
        return self._stato

    @stato.setter
    def stato(self, nuovo_stato: StatoOrdine):
        self._stato = nuovo_stato

    @property
    def prezzo_totale(self) -> float:
        return self._prezzo_totale

    def calcola_totale(self) -> float:
        self._prezzo_totale = sum(item.get_subtotale() for item in self._prodotti)
        return self._prezzo_totale

    def aggiungi_prodotto_ordine(self, prodotto_ordine: ProdottoOrdine):
        self._prodotti.append(prodotto_ordine)
        self.calcola_totale()

    def rimuovi_prodotto_ordine(self, prodotto_ordine: ProdottoOrdine):
        if prodotto_ordine in self._prodotti:
            self._prodotti.remove(prodotto_ordine)
            self.calcola_totale()

    def richiedi_rimborso(self):
        if self._stato == StatoOrdine.COMPLETATO:
            self._stato = StatoOrdine.RIMBORSO_RICHIESTO

    def avvia_elaborazione_rimborso(self):
        if self._stato == StatoOrdine.RIMBORSO_RICHIESTO:
            self._stato = StatoOrdine.RIMBORSO_IN_ELABORAZIONE

    def completa_rimborso(self):
        if self._stato == StatoOrdine.RIMBORSO_IN_ELABORAZIONE:
            self._stato = StatoOrdine.RIMBORSO_COMPLETATO