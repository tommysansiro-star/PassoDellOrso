from datetime import date
from models.prodotto import Prodotto
from models.enums import FormulaTemporale, Livello, TipologiaAttrezzatura

class Attrezzatura(Prodotto):
    def __init__(self, id_prodotto: int, nome: str, descrizione: str, prezzo: float,
                 tipologia: TipologiaAttrezzatura, brand: str, taglia: str, livello: Livello,
                 formula_temporale: FormulaTemporale = FormulaTemporale.GIORNALIERO,
                 data_inizio: date = None, data_fine: date = None,
                 immagine: str = "", is_disponibile: bool = True):
        super().__init__(id_prodotto, nome, descrizione, prezzo, immagine, is_disponibile)
        self._tipologia = tipologia
        self._brand = brand
        self._taglia = taglia
        self._livello = livello
        self._formula_temporale = formula_temporale
        self._data_inizio = data_inizio or date.today()
        self._data_fine = data_fine or date.today()

    @property
    def tipologia(self) -> TipologiaAttrezzatura:
        return self._tipologia

    @tipologia.setter
    def tipologia(self, valore: TipologiaAttrezzatura):
        self._tipologia = valore

    @property
    def brand(self) -> str:
        return self._brand

    @brand.setter
    def brand(self, valore: str):
        self._brand = valore

    @property
    def taglia(self) -> str:
        return self._taglia

    @taglia.setter
    def taglia(self, valore: str):
        self._taglia = valore

    @property
    def livello(self) -> Livello:
        return self._livello

    @livello.setter
    def livello(self, valore: Livello):
        self._livello = valore

    @property
    def formula_temporale(self) -> FormulaTemporale:
        return self._formula_temporale

    @formula_temporale.setter
    def formula_temporale(self, valore: FormulaTemporale):
        self._formula_temporale = valore

    @property
    def data_inizio(self) -> date:
        return self._data_inizio

    @data_inizio.setter
    def data_inizio(self, data: date):
        self._data_inizio = data

    @property
    def data_fine(self) -> date:
        return self._data_fine

    @data_fine.setter
    def data_fine(self, data: date):
        self._data_fine = data

    def calcola_prezzo(self) -> float:
        moltiplicatori = {
            FormulaTemporale.GIORNALIERO: 1.0,
            FormulaTemporale.SETTIMANALE: 5.0,
            FormulaTemporale.MENSILE: 15.0,
            FormulaTemporale.STAGIONALE: 30.0
        }
        return self._prezzo * moltiplicatori.get(self._formula_temporale, 1.0)