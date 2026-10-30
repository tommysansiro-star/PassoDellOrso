from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QSpinBox, QMessageBox)
from PyQt6.QtCore import Qt
from argparse import Namespace


class ProdottoView(QWidget):
    def __init__(self, gestore_utenti, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.main_window = main_window
        self.prodotto_corrente = None

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Riquadro principale
        self.info_box = QFrame()
        self.info_box.setObjectName("InfoBox")
        self.info_layout = QVBoxLayout(self.info_box)
        self.info_layout.setSpacing(20)
        self.info_layout.setContentsMargins(40, 40, 40, 40)

        # Nome Prodotto
        self.lbl_nome = QLabel("Nome Prodotto")
        self.lbl_nome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_nome.setObjectName("TitoloProdotto")
        self.info_layout.addWidget(self.lbl_nome)

        # Prezzo e Descrizione
        self.lbl_prezzo = QLabel("Prezzo: € 0.00")
        self.lbl_prezzo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_prezzo.setStyleSheet("font-size: 20px; font-weight: bold; color: #d9534f;")
        self.info_layout.addWidget(self.lbl_prezzo)

        self.lbl_descrizione = QLabel("Descrizione del prodotto qui...")
        self.lbl_descrizione.setWordWrap(True)
        self.lbl_descrizione.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_descrizione.setStyleSheet("font-size: 16px; color: #555; margin-top: 10px; margin-bottom: 20px;")
        self.info_layout.addWidget(self.lbl_descrizione)

        # Selezione Quantità
        self.layout_quantita = QHBoxLayout()
        self.layout_quantita.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_qta = QLabel("Quantità:")
        lbl_qta.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")

        self.spin_quantita = QSpinBox()
        self.spin_quantita.setMinimum(1)
        self.spin_quantita.setMaximum(10)
        self.spin_quantita.setFixedSize(80, 35)

        self.layout_quantita.addWidget(lbl_qta)
        self.layout_quantita.addWidget(self.spin_quantita)

        self.info_layout.addLayout(self.layout_quantita)

        # Pulsante Aggiungi al Carrello
        self.btn_aggiungi = QPushButton("Aggiungi al Carrello")
        self.btn_aggiungi.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_aggiungi.setObjectName("BtnAggiungi")
        self.info_layout.addWidget(self.btn_aggiungi, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.info_box, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addSpacing(20)

        # Pulsante Indietro
        self.btn_indietro = QPushButton("Torna al Catalogo")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_indietro.setFixedSize(250, 45)
        self.main_layout.addWidget(self.btn_indietro, alignment=Qt.AlignmentFlag.AlignCenter)

    def applica_stili(self):
        self.setStyleSheet("""
            ProdottoView { background-color: white; font-family: Arial, sans-serif; }
            #InfoBox { border: 2px solid #1a365d; border-radius: 12px; background-color: #f8f9fa; min-width: 500px; max-width: 600px; }
            #TitoloProdotto { font-size: 28px; font-weight: bold; color: #1a365d; }
            QSpinBox { font-size: 16px; border: 1px solid #ccc; border-radius: 5px; padding: 5px; }
            QPushButton { background-color: #132a4a; color: white; font-weight: bold; font-size: 15px; border-radius: 8px; padding: 10px; }
            QPushButton:hover { background-color: #2a528a; }
            #BtnAggiungi { background-color: #5cb85c; min-width: 250px; margin-top: 15px; }
            #BtnAggiungi:hover { background-color: #4cae4c; }
        """)

    def connetti_segnali(self):
        self.btn_aggiungi.clicked.connect(self.aggiungi_al_carrello)
        self.btn_indietro.clicked.connect(self.torna_al_catalogo)

    def imposta_prodotto(self, prodotto):
        self.prodotto_corrente = prodotto

        nome = getattr(prodotto, 'nome', getattr(prodotto, '_nome', 'Prodotto Sconosciuto'))
        prezzo = getattr(prodotto, 'prezzo', getattr(prodotto, '_prezzo', 0.0))
        descrizione = getattr(prodotto, 'descrizione',
                              getattr(prodotto, '_descrizione', 'Nessuna descrizione disponibile.'))

        self.lbl_nome.setText(nome)
        self.lbl_prezzo.setText(f"Prezzo: € {prezzo:.2f}")
        self.lbl_descrizione.setText(descrizione)

        # 1. Controlla se il prodotto è stato disabilitato manualmente dal dipendente
        is_disponibile = getattr(prodotto, 'is_disponibile', getattr(prodotto, '_is_disponibile', True))

        # 2. Controlla se è un prodotto con quantità limitata (Attrezzatura/Lezione) o infinito (Skipass)
        ha_quantita = hasattr(prodotto, 'quantita') or hasattr(prodotto, '_quantita')
        qta_rimanente = getattr(prodotto, 'quantita', getattr(prodotto, '_quantita', 0)) if ha_quantita else 99

        # LOGICA DI BLOCCO
        if not is_disponibile or (ha_quantita and qta_rimanente <= 0):
            self.spin_quantita.setMaximum(0)
            self.spin_quantita.setValue(0)
            self.spin_quantita.setEnabled(False)
            self.btn_aggiungi.setEnabled(False)
            self.btn_aggiungi.setText("Non Disponibile / Esaurito")
            self.btn_aggiungi.setStyleSheet(
                "background-color: #d9534f; color: white; font-weight: bold; border-radius: 8px; padding: 10px; min-width: 250px; margin-top: 15px;")
        else:
            self.spin_quantita.setMinimum(1)
            # Se è limitato (es. Sci) metti il limite reale, se è Skipass metti un massimo arbitrario per acquisto (es. 10)
            limite_acquisto = int(qta_rimanente) if ha_quantita else 10
            self.spin_quantita.setMaximum(limite_acquisto)
            self.spin_quantita.setValue(1)
            self.spin_quantita.setEnabled(True)
            self.btn_aggiungi.setEnabled(True)
            self.btn_aggiungi.setText("Aggiungi al Carrello")
            self.btn_aggiungi.setStyleSheet(
                "background-color: #5cb85c; color: white; font-weight: bold; border-radius: 8px; padding: 10px; min-width: 250px; margin-top: 15px;")

    def aggiungi_al_carrello(self):
        if not self.prodotto_corrente:
            return

        utente = None
        if self.gestore_utenti and hasattr(self.gestore_utenti, 'utente_corrente'):
            utente = self.gestore_utenti.utente_corrente

        if not utente:
            QMessageBox.warning(self, "Attenzione", "Devi effettuare l'accesso per aggiungere prodotti al carrello.")
            return

        # Estrai dati dal prodotto corrente
        nome_prod = getattr(self.prodotto_corrente, 'nome', getattr(self.prodotto_corrente, '_nome', 'Prodotto'))
        prezzo_prod = getattr(self.prodotto_corrente, 'prezzo', getattr(self.prodotto_corrente, '_prezzo', 0.0))
        quantita = self.spin_quantita.value()

        # Usiamo Namespace per evitare crash con pickle (come fatto in precedenza)
        nuovo_item = Namespace(nome=nome_prod, prezzo=prezzo_prod, quantita=quantita)

        # Aggiungiamo al carrello dell'utente
        if hasattr(utente, 'aggiungi_al_carrello'):
            utente.aggiungi_al_carrello(nuovo_item)
        else:
            if not hasattr(utente, '_prodotti_carrello') and not hasattr(utente, 'prodotti_carrello'):
                utente._prodotti_carrello = []

            carrello = getattr(utente, 'prodotti_carrello', getattr(utente, '_prodotti_carrello', []))
            carrello.append(nuovo_item)

        # Salva su file pickle
        if hasattr(self.gestore_utenti, '_salva_dati'):
            self.gestore_utenti._salva_dati()

        # Messaggio di successo personalizzato
        QMessageBox.information(
            self,
            "Prodotto Aggiunto",
            f"Hai aggiunto {quantita}x '{nome_prod}' al tuo carrello con successo!\n\nContinua lo shopping o vai al carrello per completare l'acquisto."
        )

        # Torna al catalogo automaticamente
        self.torna_al_catalogo()

    def torna_al_catalogo(self):
        if self.main_window and hasattr(self.main_window, 'mostra_prodotti'):
            self.main_window.mostra_prodotti()
        else:
            print("WIP: Pagina catalogo prodotti non ancora gestita dalla MainWindow")