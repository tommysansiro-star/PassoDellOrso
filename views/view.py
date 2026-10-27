import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from controllers.gestore_utenti import GestoreUtenti

class LoginView(QWidget):
    def __init__(self, gestore_utenti):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.setupUi()
        self.connectSignals()

    def setupUi(self):
        self.layout = QVBoxLayout()
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.btnLogin = QPushButton("Accedi")

        self.layout.addWidget(self.input_email)
        self.layout.addWidget(self.input_password)
        self.layout.addWidget(self.btnLogin)
        self.setLayout(self.layout)

    def connectSignals(self):
        self.btnLogin.clicked.connect(self.eseguiLogin)

    def eseguiLogin(self):
        email = self.input_email.text()
        password = self.input_password.text()

        utente = self.gestore_utenti.richiestaAccesso(email, password)

        if utente:
            QMessageBox.information(self, "Successo", f"Benvenuto ,{utente.nome} {utente.cognome}.")
        else:
            QMessageBox.information(self, "Errore", "Credenziali non valide")


