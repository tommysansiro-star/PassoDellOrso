import os
import pickle


from models.pista import Pista
from models.enums import StatoApertura, Difficolta

class GestorePiste:
    def __init__(self):
        self._piste = []

        # Persistenza dati
        self._file_path = "data/piste.pickle"
        self._carica_dati()

    def visualizzaPiste(self) -> list:
        """Restituisce l'elenco completo di tutte le piste dell'impianto."""
        return self._piste

    def getPistaById(self, id_pista: int):
        """Restituisce un oggetto Pista specifico ricercato per ID."""
        for pista in self._piste:
            if getattr(pista, 'id', None) == id_pista:
                return pista
        return None

    def filtraPistePerDifficolta(self, difficolta) -> list:
        """
        Filtra le piste in base al livello (es. PRINCIPIANTE, AVANZATO).
        Il parametro 'difficolta' dovrebbe essere un valore dell'Enum Difficoltà.
        """
        return [p for p in self._piste if getattr(p, 'difficolta', None) == difficolta]

    def modificaStatoPista(self, id_pista: int, nuovo_stato) -> bool:
        """
        Modifica lo stato di apertura di una pista (es. da APERTA a MANUTENZIONE).
        'nuovo_stato' dovrebbe essere un valore dell'Enum StatoApertura.
        """
        pista = self.getPistaById(id_pista)
        if pista:
            pista.stato = nuovo_stato
            self._salva_dati()
            return True
        return False

    def inserisciNuovaPista(self, pista) -> None:
        """Aggiunge una nuova pista all'impianto (lato Dipendente)."""
        if getattr(pista, 'id', None) is None:
            nuovo_id = 1 if not self._piste else max(p.id for p in self._piste) + 1
            pista.id = nuovo_id

        self._piste.append(pista)
        self._salva_dati()

    def _salva_dati(self):
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, 'wb') as f:
            pickle.dump(self._piste, f)

    def _carica_dati(self):
        if os.path.exists(self._file_path):
            with open(self._file_path, 'rb') as f:
                self._piste = pickle.load(f)