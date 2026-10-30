from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QScrollArea)
from PyQt6.QtCore import Qt


class OrdiniView(QWidget):
    def __init__(self, gestore_utenti, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)

        self.lbl_titolo = QLabel("I MIEI ORDINI")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setObjectName("Titolo")
        self.main_layout.addWidget(self.lbl_titolo)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("ScrollArea")

        self.scroll_content = QWidget()
        self.layout_ordini = QVBoxLayout(self.scroll_content)
        self.layout_ordini.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_ordini.setSpacing(15)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        self.btn_indietro = QPushButton("Torna al Profilo")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_indietro.setFixedSize(250, 45)
        self.main_layout.addWidget(self.btn_indietro, alignment=Qt.AlignmentFlag.AlignCenter)

    def applica_stili(self):
        self.setStyleSheet("""
            OrdiniView { background-color: white; font-family: Arial, sans-serif; }
            #Titolo { font-size: 26px; font-weight: bold; color: #1a365d; }
            #ScrollArea { border: 1px solid #ccc; border-radius: 8px; background-color: #f8f9fa; }
            .OrdineFrame { background-color: white; border: 2px solid #1a365d; border-radius: 8px; padding: 15px; }
            QPushButton { background-color: #132a4a; color: white; font-weight: bold; font-size: 15px; border-radius: 8px; }
            QPushButton:hover { background-color: #2a528a; }
        """)

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_indietro)

    def aggiorna_dati(self):
        while self.layout_ordini.count():
            child = self.layout_ordini.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        utente = None
        if self.gestore_utenti and hasattr(self.gestore_utenti, 'utente_corrente'):
            utente = self.gestore_utenti.utente_corrente

        if not utente:
            return

        ordini = getattr(utente, 'storico_ordini', getattr(utente, '_storico_ordini', []))

        if not ordini:
            lbl_vuoto = QLabel("Non hai ancora effettuato nessun ordine.")
            lbl_vuoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_vuoto.setStyleSheet("font-size: 16px; color: #666; margin-top: 20px;")
            self.layout_ordini.addWidget(lbl_vuoto)
            return

        # Mostriamo gli ordini dal più recente al più vecchio
        for ordine in reversed(ordini):
            frame = QFrame()
            frame.setProperty("class", "OrdineFrame")
            lay = QVBoxLayout(frame)

            id_ordine = getattr(ordine, 'id_ordine', 'N/A')
            data = getattr(ordine, 'data', 'Data sconosciuta')
            totale = getattr(ordine, 'totale', 0.0)
            stato = getattr(ordine, 'stato', 'Completato')

            lbl_header = QLabel(f"<b>Ordine #{id_ordine}</b> - {data}")
            lbl_header.setStyleSheet("font-size: 16px; color: #1a365d;")

            lbl_dettagli = QLabel(f"Totale: € {totale:.2f} &nbsp;|&nbsp; Stato: <b>{stato}</b>")
            lbl_dettagli.setStyleSheet("font-size: 15px; color: #333; margin-top: 5px;")

            lay.addWidget(lbl_header)
            lay.addWidget(lbl_dettagli)

            self.layout_ordini.addWidget(frame)

    def torna_indietro(self):
        if self.main_window and hasattr(self.main_window, 'mostra_profilo'):
            self.main_window.mostra_profilo()