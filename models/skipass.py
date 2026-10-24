from datetime import date
from models.prodotto import Prodotto
from models.enums import FormulaTemporale

class Skipass(Prodotto):
    def __init__(self, id_prodotto: int, nome: str, descrizione: str, prezzo: float,
                 formula_temporale: FormulaTemporale, data_inizio: date, data_fine: date,
                 immagine: str = "", is_disponibile: bool = True):
        super().__init__(id_prodotto, nome, descrizione, prezzo, immagine, is_disponibile)
        self._formula_temporale = formula_temporale
        self._data_inizio = data_inizio
        self._data_fine = data_fine

    @property
    def formula_temporale(self) -> FormulaTemporale:
        return self._formula_temporale

    @formula_temporale.setter
    def formula_temporale(self, formula: FormulaTemporale):
        self._formula_temporale = formula

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

    def set_periodo_validita(self, data_inizio: date, data_fine: date) -> None:
        """Imposta contemporaneamente la data di inizio e di fine validità dello skipass."""
        if data_inizio > data_fine:
            raise ValueError("La data di inizio non può essere successiva alla data di fine.")
        self._data_inizio = data_inizio
        self._data_fine = data_fine

    def calcola_prezzo(self) -> float:
        moltiplicatori = {
            FormulaTemporale.GIORNALIERO: 1.0,
            FormulaTemporale.SETTIMANALE: 5.5,
            FormulaTemporale.MENSILE: 18.0,
            FormulaTemporale.STAGIONALE: 40.0
        }
        return self._prezzo * moltiplicatori.get(self._formula_temporale, 1.0)