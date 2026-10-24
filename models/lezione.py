from datetime import date, time
from models.prodotto import Prodotto
from models.enums import Livello

class Lezione(Prodotto):
    def __init__(self, id_prodotto: int, nome: str, descrizione: str, prezzo: float,
                 nome_maestro: str, livello: Livello, numero_partecipanti: int = 1,
                 data_lezione: date = None, orario_inizio: time = None,
                 immagine: str = "", is_disponibile: bool = True):
        super().__init__(id_prodotto, nome, descrizione, prezzo, immagine, is_disponibile)
        self._nome_maestro = nome_maestro
        self._livello = livello
        self._numero_partecipanti = numero_partecipanti
        self._data_lezione = data_lezione or date.today()
        self._orario_inizio = orario_inizio

    @property
    def nome_maestro(self) -> str:
        return self._nome_maestro

    @nome_maestro.setter
    def nome_maestro(self, valore: str):
        self._nome_maestro = valore

    @property
    def livello(self) -> Livello:
        return self._livello

    @livello.setter
    def livello(self, valore: Livello):
        self._livello = valore

    @property
    def numero_partecipanti(self) -> int:
        return self._numero_partecipanti

    @numero_partecipanti.setter
    def numero_partecipanti(self, valore: int):
        if valore < 1:
            raise ValueError("Il numero di partecipanti deve essere almeno 1.")
        self._numero_partecipanti = valore

    @property
    def data_lezione(self) -> date:
        return self._data_lezione

    @data_lezione.setter
    def data_lezione(self, data: date):
        self._data_lezione = data

    @property
    def orario_inizio(self) -> time:
        return self._orario_inizio

    @orario_inizio.setter
    def orario_inizio(self, ora: time):
        self._orario_inizio = ora

    def calcola_prezzo(self) -> float:
        # Sovrapprezzo leggero in base al numero di partecipanti (es. lezione privata vs gruppo)
        fattore_gruppo = 1.0 + (0.2 * (self._numero_partecipanti - 1))
        return self._prezzo * fattore_gruppo