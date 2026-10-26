import os
import pickle
from models.utente import Utente
from models.cliente import Cliente
from models.dipendente import Dipendente
from controllers.gestore_mail import GestoreMail

class GestoreUtenti:
    def __init__(self, gestore_mail: GestoreMail):
        self._utenti = []
        self._gestore_mail = gestore_mail
        self._file_path = "data/utenti.pickle"

        self.utente_corrente = None

        self._carica-dati()

    def getUtenteByMail(self, email:str ):
        for utente in self._utenti:
            if utente.email == email:
                return utente
            return None

    def validaPassword(self, password: str) -> bool:
        return len(password) >= 8

    def validaCredenziali(self, email: str, password: str) -> bool:
        utente = self.getUtenteByMail(email)
        if utente is not None and utente.password == password:
            return True
        return False

    def richiestaAccesso(self, email: str, password: str):
        if self.validaCredenziali(email, password):
            self.utente_corrente = self.getUtenteByMail(email)
            return self.utente_corrente
        return None

    def effettuaLogout(self) -> None:
        """Chiude la sessione corrente dell'utente loggato."""
        if self.utente_corrente is not None:
            # Opzionale: self.utente_corrente.ultimoAccesso = datetime.now()
            # self._salva_dati()
            self.utente_corrente = None

    def registraCliente(self, nome: str, cognome: str, email: str, password: str, telefono: str):
        """Registra un nuovo Cliente."""
        if self.getUtenteByMail(email) is not None:
            raise ValueError("Email già in uso nel sistema.")
        if not self.validaPassword(password):
            raise ValueError("La password non rispetta i requisiti di sicurezza.")

        nuovo_id = 1 if not self._utenti else max(u.id for u in self._utenti) + 1

        nuovo_cliente = Cliente(nuovo_id, nome, cognome, email, password, telefono)
        self._utenti.append(nuovo_cliente)
        self._salva_dati()
        self._gestore_mail.inviaEmailBenvenuto(email, nome)
        return nuovo_cliente

    def registraDipendente(self, nome: str, cognome: str, email: str, password: str, telefono: str):
        """Registra un nuovo Dipendente (solo admin)."""
        if self.getUtenteByMail(email) is not None:
            raise ValueError("Email già in uso nel sistema.")
        if not self.validaPassword(password):
            raise ValueError("La password non rispetta i requisiti di sicurezza.")

        nuovo_id = 1 if not self._utenti else max(u.id for u in self._utenti) + 1

        nuovo_dipendente = Dipendente(nuovo_id, nome, cognome, email, password, telefono)
        self._utenti.append(nuovo_dipendente)
        self._salva_dati()
        self._gestore_mail.inviaEmailBenvenuto(email, nome)
        return nuovo_dipendente


    def rimuoviUtente(self, id_utente: int) -> bool:
        """Elimina un Utente (Cliente o Dipendente) tramite ID."""
        for utente in self._utenti:
            if utente.id == id_utente:
                self._utenti.remove(utente)
                self._salva_dati()
                return True
        return False

    def aggiungiNuovoMetodoPagamento(self, utente, metodo_pagamento) -> None:
        """Aggiunge una carta al profilo, verificando che l'utente sia abilitato."""
        if hasattr(utente, 'aggiungi_metodo_pagamento'):
            utente.aggiungi_metodo_pagamento(metodo_pagamento)
            self._salva_dati()
        else:
            raise TypeError("Operazione non consentita per questo tipo di utente.")

    def rimuoviMetodoPagamento(self, utente, codice_carta: str) -> bool:
        """Rimuove una carta dal profilo del cliente."""
        if hasattr(utente, 'rimuovi_metodo_pagamento'):
            esito = utente.rimuovi_metodo_pagamento(codice_carta)
            if esito:
                self._salva_dati()
            return esito
        return False

    def inserisciMail(self, email: str) -> None:
        """Verifica se la mail inserita per il recupero esiste a sistema."""
        if self.getUtenteByMail(email) is None:
            raise ValueError("Nessun utente trovato con questa email.")

    def recuperoCredenziali(self, email: str) -> None:
        """Avvia la procedura di recupero password tramite email."""
        if self.getUtenteByMail(email):
            self._gestore_mail.inviaEmailRecupero(email)

    def inserisciNuovaPassword(self, email: str, nuova_password: str) -> None:
        """Aggiorna le credenziali dell'utente e invia notifica."""
        utente = self.getUtenteByMail(email)
        if utente and self.validaPassword(nuova_password):
            utente.password = nuova_password
            self._salva_dati()
            # Assicurati che GestoreMail riceva i parametri attesi
            self._gestore_mail.inviaEmailModificaCredenziali(email)

    def _salva_dati(self):
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, "wb") as f:
            pickle.dump(self._utenti, f)

    def _carica_dati(self):
        if os.path.exists(self._file_path):
            with open(self._file_path, "rb") as f:
                self._utenti = pickle.load(f)
