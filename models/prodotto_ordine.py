from models.prodotto import Prodotto

class ProdottoOrdine:
    def __init__(self, id_prodotto_ordine: int, prodotto: Prodotto, quantita: int = 1):
        self._id_prodotto_ordine = id_prodotto_ordine
        self._prodotto = prodotto
        self._quantita = quantita

    @property
    def id_prodotto_ordine(self) -> int:
        return self._id_prodotto_ordine

    @property
    def prodotto(self) -> Prodotto:
        return self._prodotto

    @prodotto.setter
    def prodotto(self, prod: Prodotto):
        self._prodotto = prod

    @property
    def quantita(self) -> int:
        return self._quantita

    @quantita.setter
    def quantita(self, valore: int):
        if valore <= 0:
            raise ValueError("La quantità deve essere maggiore di zero.")
        self._quantita = valore

    def get_subtotale(self) -> float:
        return self._prodotto.calcola_prezzo() * self._quantita