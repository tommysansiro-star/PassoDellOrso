import os
import pickle
from models.cliente import Cliente
from models.metodo_pagamento import MetodoPagamento
from controllers.gestore_mail import GestoreMail

class GestoreClienti:
    def __init__(self, gestore_mail: GestoreMail):
        self.clienti = []
        self.gestore_mail = gestore_mail
        self._file_path = "data/clienti.pickle"
        self._carica_dati()

    def registraCliente(self, nome:str, cognome: str, email: str, password: str, telefono: str):
        """Registra un nuovo cliente, lo salva su file e invia la mail di benvenuto"""
        if self.getClienteByMail(email) is not None:
            raise ValueError("Email già in uso da un altro cliente")
        if not self.validaPassword(password):
            raise ValueError("La password non rispetta i requisiti di sicurezza.")

        nuovo_id = 1 if not self._clienti else max(c.id for c in self._clienti) + 1

        nuovo_cliente = Cliente(nuovo_id, nome, cognome, email, password, telefono)
        self._clienti.append(nuovo_cliente)

        self._salva_dati()

        self._gestore_mail.inviaEmailBenvenuto(email,nome)

        return nuovo_cliente

    def getClienteByMail(self, email: str):
        """Cerca e restituisce un Cliente dalla lista in base alla mail"""
        for cliente in self._clienti:
            if cliente.email == email:
                return cliente
            return None

    def eliminaAccountCliente(self, id_cliente: int) -> bool:
        """Elimina il cliente identificato dall'ID"""
        for cliente in self._clienti:
            if cliente.id == id_cliente:
                self._clienti.remove(cliente)
                self._salva_dati()
                return True
        return False

    def validaPassword(self, password: str) -> bool:
        """Verifica la robustezza della password"""
        return len(password)>=8
        #aggiungere eventualmente altri vincoli sulla struttura della password

    def aggiungiNuovoMetodoPagamento(self, cliente, metodo_pagamento) -> None:
        """Aggiunge una carta al profilo del cliente."""
        cliente.aggiungi_metodo_pagamento(metodo_pagamento)
        self._salva_dati()

    def rimuoviMetodoPagamento(self, cliente, codice_carta: str) -> bool:
        """Rimuove una carta dal profilo del cliente verificandone l'esito"""
        esito = cliente.rimuovi_metodo_pagamento(codice_carta)
        if esito:
            self._salva_dati()
        return esito

    def inserisciMail(self, email: str) -> None:
        """Verifica se la mail inserita nel form esiste nel sistema."""
        if self.getClienteByMail(email) is None:
            raise ValueError("Nessun cliente trovato con questa email.")

    def inserisciPassword(self, password: str) -> None:
        """Verifica l'inserimento di una password"""
        pass

    def modificaCredenziali(self, email: str, nuova_password: str) -> None:
        """Aggiorna le credenziali del cliente."""
        cliente = self.getClienteByMail(email)
        if cliente and self.validaPassword(nuova_password):
            cliente.password = nuova_password
            self._salva_dati()
            self._gestore_mail.inviaEmailModificaCredenziali(email, cliente)

    def _salva_dati(self):
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, "wb") as f:
            pickle.dump(self._clienti, f)

    def _carica_dati(self):
        if os.path.exists(self._file_path):
            with open(self._file_path, "rb") as f:
                self._clienti = pickle.load(f)
