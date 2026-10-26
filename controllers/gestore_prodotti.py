import os
import pickle

from models.prodotto import Prodotto
from models.prodotto_carrello import ProdottoCarrello

class GestoreProdotti:
    def __init__(self):
        self._prodotti = []
        self._file_path = "data/prodotti.pickle"
        self._carica_dati()

    def inserisciNuovoProdotto(self, prodotto) -> None:
        """Aggiunge un prodotto inedito al catalogo e salva su file."""
        self._prodotti.append(prodotto)
        self._salva_dati()

    def getProdottoById(self, id_prodotto: int):
        """Cerca e restituisce un prodotto dal catalogo tramite il suo ID."""
        for prodotto in self._prodotti:
            if prodotto.id == id_prodotto:
                return prodotto
        return None

    def eliminaProdotto(self, id_prodotto: int) -> bool:
        """Rimuove un prodotto dal catalogo in base all'ID."""
        prodotto = self.getProdottoById(id_prodotto)
        if prodotto is not None:
            self._prodotti.remove(prodotto)
            self._salva_dati()
            return True
        return False

    def filtraProdottiPerTipo(self, tipo: str) -> list:
        """Filtra i prodotti per categoria. Usa il nome della sottoclasse per filtrare"""
        return  [
            p for p in self._prodotti
            if p.__class__.__name__.lower() == tipo.lower()
        ]

    def modificaProdotto(self, id_prodotto: int, nuovo_prezzo: float, is_disponibile: bool) -> bool:
        """Modifica il prezzo e lo stato di disponibilità di un prodotto a catalogo."""
        prodotto = self.getProdottoById(id_prodotto)
        if prodotto is not None:
            prodotto.prezzo = nuovo_prezzo
            prodotto.is_disponibile = is_disponibile
            self._salva_dati()
            return True
        return False

    def aggiungiProdotto(self, cliente, prodotto, quantita_richiesta: int) -> None:
        """Aggiunge un prodotto con la relativa quantità al carrello del cliente."""
        if quantita <= 0:
            raise ValueError("La quantità defe essere maggiore di zero.")

        if not getattr(prodotto, 'is_disponibile', True):
            raise ValueError("Il prodotto selezionato non è attualmente disponibile.")

        if hasattr(prodotto, 'quantita') and prodotto.quantita < quantita_richiesta:
            raise ValueError("Quantità richiesta non disponibile. Scorta attuale: {prodotto.quantita}")

        for item in cliente.prodotti_carrello:
            if item.prodotto.id == prodotto.id:
                nuova_quantita = item.quantita + quantita_richiesta
                if hasattr(prodotto, 'quantita') and prodotto.quantita < nuova_quantita:
                    raise ValueError("Quantità totale nel carrello superiore alla disponibilità.")
                item.quantita = nuova_quantita
                return

        nuovo_item = ProdottoCarrello(prodotto = prodotto, quantita = quantita_richiesta)
        cliente.prodotti_carrello.append(nuovo_item)

    def visualizzaCarrello(self, cliente) -> list:
        """Restituisce la lista di ProdottoCarrello associata al cliente."""
        return cliente.prodotti_carrello

    def rimuoviProdottoDalCarrello(self, cliente, prodotto_carrello) -> None:
        """Rimuove un ProdottoCarrello dal carrello del cliente."""
        if prodotto_carrello in cliente.prodotti_carrello:
            cliente.prodotti_carrello.remove(prodotto_carrello)

    def modificaQuantitaCarrello(self, cliente, prodotto_carrello, nuova_quantita: int) -> bool:
        """Modifica la quantità di un elemento già presente nel carrello."""
        if prodotto_carrello not in cliente.prodotti_carrello:
            return False

        if nuova_quantita <= 0:
            self.rimuoviProdottoDalCarrello(cliente, prodotto_carrello)
            return True

        prodotto_catalogo = prodotto_carrello.prodotto
        if hasattr(prodotto_catalogo, 'quantita') and prodotto_catalogo.quantita < nuova_quantita:
            return False

        prodotto_carrello.quantita = nuova_quantita
        return True

    def _salva_dati(self):
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, "wb") as f:
            pickle.dump(self._prodotti, f)

    def _carica_dati(self):
        if os.path.exists(self._file_path):
            with open(self._file_path, "rb") as f:
                self._prodotti = pickle.load(f)