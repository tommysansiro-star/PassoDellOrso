from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QRadioButton, QButtonGroup, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from models.enums import StatoApertura


class VistaDashboardDipendente(QWidget):
    def __init__(self, controller_utenti, controller_ordini, controller_piste):
        super().__init__()
        # Salvataggio dei controller passati dal main
        self.controller_utenti = controller_utenti
        self.controller_ordini = controller_ordini
        self.controller_piste = controller_piste

        # Recupero l'utente loggato
        self.utente_loggato = self.controller_utenti.get_utente_loggato()

        self.init_ui()

    def init_ui(self):
        nome_utente = f"{self.utente_loggato.nome}" if self.utente_loggato else "Admin"
        id_utente = f"{self.utente_loggato.id_dipendente}" if hasattr(self.utente_loggato, 'id_dipendente') else "101"
        self.setWindowTitle(f"Passo Dell'Orso - Ciao, {nome_utente} (Dipendente #{id_utente})")
        self.resize(800, 600)
        self.setStyleSheet("background-color: white;")

        layout_principale = QHBoxLayout()

        # ==========================================
        # COLONNA SINISTRA: MENU
        # ==========================================
        layout_sinistra = QVBoxLayout()
        layout_sinistra.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        layout_sinistra.setSpacing(15)

        lbl_logo = QLabel("⛰️ PASSO DELL'ORSO\nSKI RESORT")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a365d; margin-bottom: 20px;")
        layout_sinistra.addWidget(lbl_logo)

        lbl_menu = QLabel("MENÙ ADMIN")
        lbl_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_menu.setStyleSheet(
            "background-color: #a3d8f4; color: #1a365d; font-weight: bold; font-size: 16px; padding: 15px; border-radius: 10px;")
        layout_sinistra.addWidget(lbl_menu)

        stile_btn = """
            QPushButton { background-color: #1a365d; color: white; font-weight: bold; font-size: 14px; padding: 10px; border-radius: 5px; }
            QPushButton:hover { background-color: #2c5282; }
        """

        # Creazione e collegamento bottoni Menu
        self.btn_dashboard = QPushButton("Dashboard")
        self.btn_piste = QPushButton("Gestione Piste")
        self.btn_inventario = QPushButton("Inventario")
        self.btn_utenti = QPushButton("Utenti")
        self.btn_logout = QPushButton("Logout")

        for btn in [self.btn_dashboard, self.btn_piste, self.btn_inventario, self.btn_utenti, self.btn_logout]:
            btn.setFixedSize(180, 40)
            btn.setStyleSheet(stile_btn)
            layout_sinistra.addWidget(btn)

        # CABLAGGIO: Colleghiamo il tasto Logout
        self.btn_logout.clicked.connect(self.esegui_logout)

        # Gli altri bottoni per ora mostrano un popup (li collegheremo alle altre finestre poi)
        self.btn_piste.clicked.connect(lambda: QMessageBox.information(self, "Info", "Apertura Gestione Piste..."))
        self.btn_inventario.clicked.connect(lambda: QMessageBox.information(self, "Info", "Apertura Inventario..."))
        self.btn_utenti.clicked.connect(lambda: QMessageBox.information(self, "Info", "Apertura Gestione Utenti..."))

        # Separatore
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.VLine)
        linea.setStyleSheet("color: #1a365d;")

        # ==========================================
        # COLONNA DESTRA: CONTENUTI
        # ==========================================
        layout_destra = QVBoxLayout()
        layout_destra.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout_destra.setSpacing(20)

        stile_titolo = "background-color: #a3d8f4; color: #1a365d; font-weight: bold; font-size: 16px; padding: 15px; border-radius: 10px;"

        # --- SEZIONE 1: ULTIMI ORDINI ---
        lbl_ordini = QLabel("ULTIMI ORDINI")
        lbl_ordini.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_ordini.setStyleSheet(stile_titolo)
        layout_destra.addWidget(lbl_ordini)

        # Generazione DINAMICA degli ordini dal Controller
        testo_ordini = ""
        # Usiamo un try-except nel caso il controller non sia ancora completo
        try:
            ultimi_ordini = self.controller_ordini.get_tutti_ordini()[-2:]  # Prende gli ultimi 2
            if not ultimi_ordini:
                testo_ordini = "Nessun ordine presente nel sistema."
            for ord in ultimi_ordini:
                testo_ordini += f"- Ordine #{ord.id_ordine} | Totale: {ord.prezzo_totale}€ | Stato: {ord.stato.value}\n\n"
        except AttributeError:
            testo_ordini = "(Implementare get_tutti_ordini() nel ControllerOrdini per visualizzare i dati reali)"

        self.lbl_lista_ordini = QLabel(testo_ordini)
        self.lbl_lista_ordini.setStyleSheet("font-size: 14px; color: #333333; margin-left: 10px;")
        layout_destra.addWidget(self.lbl_lista_ordini)

        btn_vedi_ordini = QPushButton("Vedi tutti")
        btn_vedi_ordini.setFixedSize(150, 40)
        btn_vedi_ordini.setStyleSheet(stile_btn)
        layout_destra.addWidget(btn_vedi_ordini, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_destra.addSpacing(20)

        # --- SEZIONE 2: GESTIONE RAPIDA PISTE ---
        lbl_piste = QLabel("GESTIONE RAPIDA PISTE")
        lbl_piste.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_piste.setStyleSheet(stile_titolo)
        layout_destra.addWidget(lbl_piste)

        layout_griglia_piste = QGridLayout()

        # Generazione DINAMICA delle piste dal Controller
        try:
            tutte_piste = self.controller_piste.get_tutte_piste()
            self.gruppi_piste = []  # Manteniamo i riferimenti ai button group

            for riga, pista in enumerate(tutte_piste):
                lbl_nome = QLabel(f"- {pista.nome}:")
                lbl_nome.setStyleSheet("font-size: 14px; color: #333;")
                layout_griglia_piste.addWidget(lbl_nome, riga, 0)

                gruppo = QButtonGroup(self)
                rb_aperta = QRadioButton("Aperta")
                rb_chiusa = QRadioButton("Chiusa")
                rb_manut = QRadioButton("Manut.")

                # Imposta il check in base allo stato reale
                if pista.stato_apertura == StatoApertura.APERTA:
                    rb_aperta.setChecked(True)
                elif pista.stato_apertura == StatoApertura.CHIUSA:
                    rb_chiusa.setChecked(True)
                else:
                    rb_manut.setChecked(True)

                gruppo.addButton(rb_aperta)
                gruppo.addButton(rb_chiusa)
                gruppo.addButton(rb_manut)

                layout_griglia_piste.addWidget(rb_aperta, riga, 1)
                layout_griglia_piste.addWidget(rb_chiusa, riga, 2)
                layout_griglia_piste.addWidget(rb_manut, riga, 3)

                # CABLAGGIO: Quando clicchi, aggiorna lo stato della pista nel sistema!
                rb_aperta.clicked.connect(lambda checked, p=pista: self.aggiorna_stato_pista(p, StatoApertura.APERTA))
                rb_chiusa.clicked.connect(lambda checked, p=pista: self.aggiorna_stato_pista(p, StatoApertura.CHIUSA))
                rb_manut.clicked.connect(
                    lambda checked, p=pista: self.aggiorna_stato_pista(p, StatoApertura.MANUTENZIONE))

                self.gruppi_piste.append(gruppo)

        except AttributeError:
            lbl_errore = QLabel("(Implementare get_tutte_piste() nel ControllerPiste)")
            layout_griglia_piste.addWidget(lbl_errore, 0, 0)

        layout_destra.addLayout(layout_griglia_piste)

        btn_vedi_piste = QPushButton("Vedi tutte")
        btn_vedi_piste.setFixedSize(150, 40)
        btn_vedi_piste.setStyleSheet(stile_btn)
        layout_destra.addWidget(btn_vedi_piste, alignment=Qt.AlignmentFlag.AlignCenter)

        # ==========================================
        # ASSEMBLAGGIO FINALE
        # ==========================================
        layout_principale.addLayout(layout_sinistra, 1)
        layout_principale.addWidget(linea)
        layout_principale.addLayout(layout_destra, 2)
        self.setLayout(layout_principale)

    # --- METODI LOGICI (SLOTS) ---

    def aggiorna_stato_pista(self, pista, nuovo_stato):
        # Chiama il controller per aggiornare e salvare il dato
        pista.stato_apertura = nuovo_stato
        self.controller_piste.salva_dati()
        print(f"Stato pista '{pista.nome}' aggiornato a: {nuovo_stato.name}")

    def esegui_logout(self):
        # Esegue il logout nel controller
        self.controller_utenti.logout()

        # Qui potremmo importare e riaprire VistaLogin
        from views.vista_login import VistaLogin
        self.vista_login = VistaLogin(self.controller_utenti)
        self.vista_login.show()

        # Chiude la dashboard
        self.close()