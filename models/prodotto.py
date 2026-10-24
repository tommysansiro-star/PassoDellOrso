from abc import ABC, abstractmethod

class Prodotto(ABC):
    def __init__(self, id_prodotto: int, nome: str, descrizione: str,
                 prezzo: float, immagine: str = "", is_disponibile: bool = True):
        self._id_prodotto = id_prodotto
        self._nome = nome
        self._descrizione = descrizione
        self._prezzo = prezzo
        self._immagine = immagine
        self._is_disponibile = is_disponibile

    @property
    def id_prodotto(self) -> int:
        return self._id_prodotto

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valore: str):
        self._nome = valore

    @property
    def descrizione(self) -> str:
        return self._descrizione

    @descrizione.setter
    def descrizione(self, valore: str):
        self._descrizione = valore

    @property
    def prezzo(self) -> float:
        return self._prezzo

    @prezzo.setter
    def prezzo(self, valore: float):
        if valore < 0:
            raise ValueError("Il prezzo non può essere negativo.")
        self._prezzo = float(valore)

    @property
    def immagine(self) -> str:
        return self._immagine

    @immagine.setter
    def immagine(self, percorso: str):
        self._immagine = percorso

    @property
    def is_disponibile(self) -> bool:
        return self._is_disponibile

    @is_disponibile.setter
    def is_disponibile(self, stato: bool):
        self._is_disponibile = bool(stato)

    @abstractmethod
    def calcola_prezzo(self) -> float:
        pass