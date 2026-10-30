from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QLineEdit, QMessageBox, QFormLayout)
from PyQt6.QtCore import Qt


class ModificaCredenzialiView(QWidget):
    def __init__(self, gestore_utenti, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.main_window = main_window
        self.modalita_recupero = False  # True se veniamo dal Login (Password Dimenticata)

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Titolo
        self.lbl_titolo = QLabel("MODIFICA CREDENZIALI")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setObjectName("Titolo")
        self.main_layout.addWidget(self.lbl_titolo)

        self.main_layout.addSpacing(20)

        # Riquadro del Form
        self.form_frame = QFrame()
        self.form_frame.setObjectName("FormFrame")
        self.form_layout = QFormLayout(self.form_frame)
        self.form_layout.setSpacing(15)
        self.form_layout.setContentsMargins(30, 30, 30, 30)

        # Campi di input
        self.input_nome = QLineEdit()
        self.input_cognome = QLineEdit()
        self.input_email = QLineEdit()
        self.input_telefono = QLineEdit()

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setPlaceholderText("Lascia vuoto per non modificare")

        # Aggiunta dei campi al FormLayout
        self.form_layout.addRow(QLabel("Nome:"), self.input_nome)
        self.form_layout.addRow(QLabel("Cognome:"), self.input_cognome)
        self.form_layout.addRow(QLabel("Email:"), self.input_email)
        self.form_layout.addRow(QLabel("Telefono:"), self.input_telefono)
        self.form_layout.addRow(QLabel("Nuova Password:"), self.input_password)

        self.main_layout.addWidget(self.form_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addSpacing(20)

        # Pulsanti
        self.layout_pulsanti = QHBoxLayout()
        self.layout_pulsanti.setSpacing(20)

        self.btn_salva = QPushButton("Salva Modifiche")
        self.btn_salva.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_annulla = QPushButton("Annulla / Indietro")
        self.btn_annulla.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_annulla.setObjectName("BtnAnnulla")

        self.layout_pulsanti.addWidget(self.btn_salva)
        self.layout_pulsanti.addWidget(self.btn_annulla)

        self.main_layout.addLayout(self.layout_pulsanti)

    def applica_stili(self):
        self.setStyleSheet("""
            ModificaCredenzialiView { background-color: white; font-family: Arial, sans-serif; }
            #Titolo { font-size: 26px; font-weight: bold; color: #1a365d; }
            #FormFrame { border: 2px solid #1a365d; border-radius: 12px; background-color: #f8f9fa; min-width: 450px; }
            QLabel { font-size: 15px; font-weight: bold; color: #333; }
            QLineEdit { padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px; background-color: white; }
            QLineEdit:focus { border: 1px solid #1a365d; }
            QPushButton { background-color: #132a4a; color: white; font-weight: bold; font-size: 15px; border-radius: 8px; padding: 12px; min-width: 200px; }
            QPushButton:hover { background-color: #2a528a; }
            #BtnAnnulla { background-color: #6c757d; }
            #BtnAnnulla:hover { background-color: #5a6268; }
        """)

    def connetti_segnali(self):
        self.btn_salva.clicked.connect(self.salva_dati)
        self.btn_annulla.clicked.connect(self.torna_indietro)

    def aggiorna_dati(self):
        """Pulisce e riempie i campi se l'utente è loggato. Se non lo è, va in modalità recupero."""
        self.input_nome.clear()
        self.input_cognome.clear()
        self.input_email.clear()
        self.input_telefono.clear()
        self.input_password.clear()

        utente = None
        if self.gestore_utenti and hasattr(self.gestore_utenti, 'utente_corrente'):
            utente = self.gestore_utenti.utente_corrente

        if utente:
            self.modalita_recupero = False
            self.lbl_titolo.setText("MODIFICA IL TUO PROFILO")
            self.input_nome.setText(str(getattr(utente, 'nome', getattr(utente, '_nome', ''))))
            self.input_cognome.setText(str(getattr(utente, 'cognome', getattr(utente, '_cognome', ''))))
            self.input_email.setText(str(getattr(utente, 'email', getattr(utente, '_email', ''))))
            self.input_email.setEnabled(False)  # L'email non si cambia se sei già loggato
            self.input_telefono.setText(str(getattr(utente, 'telefono', getattr(utente, '_telefono', ''))))
            self.input_password.setPlaceholderText("Lascia vuoto per mantenere l'attuale")
        else:
            self.modalita_recupero = True
            self.lbl_titolo.setText("RECUPERO CREDENZIALI")
            self.input_email.setEnabled(True)
            self.input_email.setPlaceholderText("Inserisci la tua email per trovarti")
            self.input_password.setPlaceholderText("Inserisci la nuova password")

    def salva_dati(self):
        email = self.input_email.text().strip()
        nome = self.input_nome.text().strip()
        cognome = self.input_cognome.text().strip()
        telefono = self.input_telefono.text().strip()
        nuova_password = self.input_password.text().strip()

        if not email:
            QMessageBox.warning(self, "Errore", "Il campo Email è obbligatorio.")
            return

        utente_da_modificare = None

        if not self.modalita_recupero:
            utente_da_modificare = self.gestore_utenti.utente_corrente
        else:
            # Ricerca l'utente tramite l'email inserita
            for u in self.gestore_utenti._utenti:
                if getattr(u, 'email', getattr(u, '_email', '')) == email:
                    utente_da_modificare = u
                    break

            if not utente_da_modificare:
                QMessageBox.warning(self, "Errore", "Nessun account trovato con questa email.")
                return
            if not nuova_password:
                QMessageBox.warning(self, "Errore", "Inserisci una nuova password.")
                return

        # Applica le modifiche all'oggetto utente
        if hasattr(utente_da_modificare, '_nome'):  # Se usi variabili private
            if nome: utente_da_modificare._nome = nome
            if cognome: utente_da_modificare._cognome = cognome
            if telefono: utente_da_modificare._telefono = telefono
            if nuova_password: utente_da_modificare._password = nuova_password
        else:  # Se usi variabili pubbliche
            if nome: utente_da_modificare.nome = nome
            if cognome: utente_da_modificare.cognome = cognome
            if telefono: utente_da_modificare.telefono = telefono
            if nuova_password: utente_da_modificare.password = nuova_password

        # Salva su file pickle
        if hasattr(self.gestore_utenti, '_salva_dati'):
            self.gestore_utenti._salva_dati()

        QMessageBox.information(self, "Successo", "I dati sono stati aggiornati correttamente!")
        self.torna_indietro()

    def torna_indietro(self):
        if self.modalita_recupero:
            if self.main_window and hasattr(self.main_window, 'mostra_login'):
                self.main_window.mostra_login()
        else:
            if self.main_window and hasattr(self.main_window, 'mostra_profilo'):
                self.main_window.mostra_profilo()