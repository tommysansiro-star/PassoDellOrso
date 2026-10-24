from models.prodotto import Prodotto

class Assicurazione(Prodotto):
    def __init__(self, id_prodotto: int, nome: str, descrizione: str,
                 prezzo_giornaliero: float, copre_terzi: bool = True,
                 immagine: str = "", is_disponibile: bool = True):
        super().__init__(id_prodotto, nome, descrizione, prezzo_giornaliero, immagine, is_disponibile)
        self._copre_terzi = copre_terzi

    @property
    def copre_terzi(self) -> bool:
        return self._copre_terzi

    @copre_terzi.setter
    def copre_terzi(self, valore: bool):
        self._copre_terzi = bool(valore)

    def calcola_prezzo(self) -> float:
        # Prezzo base giornaliero dell'assicurazione
        base = self._prezzo
        if self._copre_terzi:
            base *= 1.25  # Maggiorazione se copre anche i danni a terzi
        return base