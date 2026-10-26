import unittest
import os

from controllers.gestore_piste import GestorePiste

class MockPista:
    def __init__(self, id_pista, nome, difficolta, stato_apertura="APERTA"):
        self.id_pista = id_pista
        self.nome = nome
        self.difficolta = difficolta
        self.stato_apertura = stato_apertura

class TestGestorePiste(unittest.TestCase):

    def setUp(self):
        """Inizializza l'ambiente prima di ogni test."""
        self.gestore = GestorePiste()
        self.gestore._file_path = "data/test_piste.pickle"
        self.gestore._piste = []

    def tearDown(self):
        """Pulisce i file dopo ogni test."""
        if os.path.exists(self.gestore._file_path):
            os.remove(self.gestore._file_path)

    def test_inserisci_e_ricerca_pista(self):
        pista_nuova = MockPista(id_pista=0, nome="Rossa 1", difficolta="AVANZATO")
        self.gestore.inserisciNuovaPista(pista_nuova)

        self.assertEqual(pista_nuova.id_pista, 1)
        self.assertEqual(len(self.gestore._piste), 1)

        trovata = self.gestore.getPistaById(1)
        self.assertIsNotNone(trovata)
        self.assertEqual(trovata.nome, "Rossa 1")

    def test_filtra_piste_per_difficolta(self):
        self.gestore.inserisciNuovaPista(MockPista(1, "Facile 1", "PRINCIPIANTE"))
        self.gestore.inserisciNuovaPista(MockPista(2, "Facile 2", "PRINCIPIANTE"))
        self.gestore.inserisciNuovaPista(MockPista(3, "Difficile 1", "ESPERTO"))

        risultato_facili = self.gestore.filtraPistePerDifficolta("PRINCIPIANTE")
        self.assertEqual(len(risultato_facili), 2)

        risultato_difficili = self.gestore.filtraPistePerDifficolta("ESPERTO")
        self.assertEqual(len(risultato_difficili), 1)
        self.assertEqual(risultato_difficili[0].nome, "Difficile 1")

    def test_modifica_stato_pista_successo(self):
        pista = MockPista(1, "Azzurra", "PRINCIPIANTE", stato_apertura="APERTA")
        self.gestore.inserisciNuovaPista(pista)

        esito = self.gestore.modificaStatoPista(id_pista=1, nuovo_stato="MANUTENZIONE")

        self.assertTrue(esito)

        pista_modificata = self.gestore.getPistaById(1)
        self.assertEqual(pista_modificata.stato_apertura, "MANUTENZIONE")

    def test_modifica_stato_pista_inesistente(self):
        """Verifica che la modifica su una pista che non esiste restituisca False senza bloccarsi."""
        esito = self.gestore.modificaStatoPista(id_pista=999, nuovo_stato="CHIUSA")
        self.assertFalse(esito)

if __name__ == '__main__':
    unittest.main()
