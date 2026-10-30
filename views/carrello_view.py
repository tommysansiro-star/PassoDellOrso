import datetime
from argparse import Namespace
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QScrollArea, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt


class CarrelloView(QWidget):
    def __init__(self, gestore_utenti, gestore_ordini, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.gestore_ordini = gestore_ordini
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)

        # Titolo
        self.lbl_titolo = QLabel("IL TUO CARRELLO")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setObjectName("Titolo")
        self.main_layout.addWidget(self.lbl_titolo)

        # Area di scorrimento per i prodotti
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("ScrollArea")

        self.scroll_content = QWidget()
        self.layout_prodotti = QVBoxLayout(self.scroll_content)
        self.layout_prodotti.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_prodotti.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        # Riquadro inferiore: Totale e Pagamento
        self.footer_frame = QFrame()
        self.footer_frame.setObjectName("FooterFrame")
        self.footer_layout = QHBoxLayout(self.footer_frame)

        self.lbl_totale = QLabel("Totale: € 0.00")
        self.lbl_totale.setObjectName("Totale")
        self.footer_layout.addWidget(self.lbl_totale)

        self.layout_pagamento = QVBoxLayout()
        self.combo_pagamenti = QComboBox()
        self.combo_pagamenti.setMinimumWidth(250)

        self.btn_acquista = QPushButton("Completa Acquisto")
        self.btn_acquista.setCursor(Qt.CursorShape.PointingHandCursor)

        self.layout_pagamento.addWidget(QLabel("Seleziona metodo di pagamento:"))
        self.layout_pagamento.addWidget(self.combo_pagamenti)
        self.layout_pagamento.addWidget(self.btn_acquista)

        self.footer_layout.addLayout(self.layout_pagamento)
        self.main_layout.addWidget(self.footer_frame)

        self.btn_indietro = QPushButton("Torna alla Dashboard")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_indietro.setFixedSize(250, 40)
        self.main_layout.addWidget(self.btn_indietro, alignment=Qt.AlignmentFlag.AlignCenter)

    def applica_stili(self):
        self.setStyleSheet("""
            CarrelloView { background-color: white; font-family: Arial, sans-serif; }
            #Titolo { font-size: 26px; font-weight: bold; color: #1a365d; }
            #ScrollArea { border: 1px solid #ccc; border-radius: 8px; background-color: #f8f9fa; }
            #FooterFrame { border: 2px solid #1a365d; border-radius: 8px; background-color: #f0f4f8; padding: 10px; }
            #Totale { font-size: 22px; font-weight: bold; color: #1a365d; }
            .ProdottoFrame { background-color: white; border: 1px solid #ddd; border-radius: 5px; padding: 10px; }
            QPushButton { background-color: #132a4a; color: white; font-weight: bold; font-size: 15px; border-radius: 8px; padding: 10px;}
            QPushButton:hover { background-color: #2a528a; }
            QComboBox { padding: 5px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; }
        """)

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_indietro)
        self.btn_acquista.clicked.connect(self.completa_acquisto)

    def aggiorna_dati(self):
        while self.layout_prodotti.count():
            child = self.layout_prodotti.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.combo_pagamenti.clear()

        utente = getattr(self.gestore_utenti, 'utente_corrente', None) if self.gestore_utenti else None
        if not utente:
            return

        carrello = getattr(utente, 'prodotti_carrello', getattr(utente, '_prodotti_carrello', []))

        if not carrello:
            lbl_vuoto = QLabel("Il tuo carrello è vuoto.")
            lbl_vuoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_vuoto.setStyleSheet("font-size: 16px; color: #666; margin-top: 20px;")
            self.layout_prodotti.addWidget(lbl_vuoto)
            self.lbl_totale.setText("Totale: € 0.00")
            self.btn_acquista.setEnabled(False)
            self.combo_pagamenti.setEnabled(False)
            return

        self.btn_acquista.setEnabled(True)
        self.combo_pagamenti.setEnabled(True)

        totale = 0.0

        for item in carrello:
            nome = getattr(item, 'nome', getattr(item.prodotto, 'nome', 'Prodotto')) if hasattr(item,
                                                                                                'prodotto') else getattr(
                item, 'nome', 'Prodotto')
            prezzo = getattr(item, 'prezzo', getattr(item.prodotto, 'prezzo', 0.0)) if hasattr(item,
                                                                                               'prodotto') else getattr(
                item, 'prezzo', 0.0)
            quantita = getattr(item, 'quantita', 1)

            subtotale = prezzo * quantita
            totale += subtotale

            frame = QFrame()
            frame.setProperty("class", "ProdottoFrame")
            lay = QHBoxLayout(frame)

            lbl_info = QLabel(f"<b>{nome}</b> (x{quantita})")
            lbl_info.setStyleSheet("font-size: 15px;")
            lbl_prezzo = QLabel(f"€ {subtotale:.2f}")
            lbl_prezzo.setStyleSheet("font-size: 15px; font-weight: bold; color: #132a4a;")

            btn_rimuovi = QPushButton("Rimuovi")
            btn_rimuovi.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_rimuovi.setStyleSheet("""
                QPushButton { background-color: #d9534f; padding: 5px; font-size: 13px; border-radius: 4px; }
                QPushButton:hover { background-color: #c9302c; }
            """)
            btn_rimuovi.setFixedSize(80, 30)
            btn_rimuovi.clicked.connect(lambda checked, i=item: self.rimuovi_prodotto(i))

            lay.addWidget(lbl_info, stretch=1)
            lay.addWidget(lbl_prezzo)
            lay.addSpacing(15)
            lay.addWidget(btn_rimuovi)

            self.layout_prodotti.addWidget(frame)

        self.lbl_totale.setText(f"Totale: € {totale:.2f}")

        metodi = getattr(utente, 'metodi_pagamento', getattr(utente, '_metodi_pagamento', []))
        if metodi:
            for metodo in metodi:
                nome_met = metodo if isinstance(metodo, str) else getattr(metodo, 'nome', str(metodo))
                self.combo_pagamenti.addItem(nome_met)
        else:
            self.combo_pagamenti.addItem("Nessun metodo registrato")
            self.combo_pagamenti.setEnabled(False)
            self.btn_acquista.setEnabled(False)

    def rimuovi_prodotto(self, item):
        utente = self.gestore_utenti.utente_corrente
        if not utente:
            return

        carrello = getattr(utente, 'prodotti_carrello', getattr(utente, '_prodotti_carrello', []))

        if item in carrello:
            carrello.remove(item)
            if hasattr(self.gestore_utenti, '_salva_dati'):
                self.gestore_utenti._salva_dati()
            self.aggiorna_dati()

    def completa_acquisto(self):
        # IMPORTA QUI IL TUO ENUM se necessario (es: from models.ordine import StatoOrdine)

        utente = self.gestore_utenti.utente_corrente
        metodo_scelto = self.combo_pagamenti.currentText()

        if not utente or metodo_scelto == "Nessun metodo registrato":
            QMessageBox.warning(self, "Errore", "Aggiungi un metodo di pagamento nel profilo per acquistare.")
            return

        carrello = getattr(utente, 'prodotti_carrello', getattr(utente, '_prodotti_carrello', []))
        if not carrello:
            return

        totale_ordine = sum((getattr(item, 'prezzo', 0.0) * getattr(item, 'quantita', 1)) for item in carrello)
        id_ordine_generato = int(datetime.datetime.now().timestamp())
        stato_ordine_enum = "COMPLETATO"

        nuovo_ordine = Namespace(
            id_ordine=id_ordine_generato,
            data=datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            totale=totale_ordine,
            stato=stato_ordine_enum,
            prodotti=list(carrello)
        )

        # =======================================================
        # STAMPA EMAIL DI RICEVUTA
        # =======================================================
        email_cliente = getattr(utente, 'email', 'cliente@mail.com')
        nome_cliente = getattr(utente, 'nome', 'Cliente')

        print(f"\n-> Simulazione invio email a [{email_cliente}]: ")
        print("==================================================")
        print("DA: noreply@impiantosciistico.it")
        print(f"OGGETTO: Conferma Ordine #{id_ordine_generato}")
        print("==================================================")
        print(f"\nCiao {nome_cliente},")
        print("Grazie per il tuo acquisto su Passo dell'Orso!\n")
        print("Riepilogo dei prodotti:")

        for item in carrello:
            nome_p = getattr(item, 'nome', 'Prodotto')
            prezzo_p = getattr(item, 'prezzo', 0.0)
            q_p = getattr(item, 'quantita', 1)
            print(f"- {q_p}x {nome_p} (€ {prezzo_p:.2f} cad.)")

        print(f"\nTotale pagato: € {totale_ordine:.2f}")
        print(f"Metodo di pagamento: {metodo_scelto}")
        print("\n==================================================\n")

        # =======================================================
        # SCALA LE QUANTITÀ DAL CATALOGO (SOLO PER ATTREZZATURE/LEZIONI)
        # =======================================================
        if self.main_window and hasattr(self.main_window, 'gestore_prodotti'):
            gestore_prodotti = self.main_window.gestore_prodotti
            contenitore_prodotti = getattr(gestore_prodotti, '_prodotti', getattr(gestore_prodotti, 'prodotti', []))
            lista_prodotti_reali = list(contenitore_prodotti.values()) if isinstance(contenitore_prodotti,
                                                                                     dict) else contenitore_prodotti

            for item in carrello:
                nome_acquistato = getattr(item, 'nome', getattr(item.prodotto, 'nome', '')) if hasattr(item,
                                                                                                       'prodotto') else getattr(
                    item, 'nome', '')
                qta_acquistata = getattr(item, 'quantita', 1)

                for prod_db in lista_prodotti_reali:
                    nome_db = getattr(prod_db, 'nome', getattr(prod_db, '_nome', ''))

                    if nome_db == nome_acquistato:
                        # Se il prodotto ha l'attributo quantita, vuol dire che NON è infinito
                        if hasattr(prod_db, 'quantita') or hasattr(prod_db, '_quantita'):
                            qta_attuale = getattr(prod_db, 'quantita', getattr(prod_db, '_quantita', 0))
                            nuova_qta = max(0, int(qta_attuale) - int(qta_acquistata))

                            # Scala la quantità
                            try:
                                prod_db.quantita = nuova_qta
                            except AttributeError:
                                prod_db._quantita = nuova_qta

                            # Se esaurito, impostiamo a Non Disponibile
                            if nuova_qta == 0:
                                try:
                                    prod_db.is_disponibile = False
                                except AttributeError:
                                    prod_db._is_disponibile = False

                        # Se non ha l'attributo (es. Skipass), lo ignoriamo (rimane sempre disponibile)
                        break

            # Salva il catalogo prodotti aggiornato
            try:
                if hasattr(gestore_prodotti, '_salva_dati'):
                    gestore_prodotti._salva_dati()
                elif hasattr(gestore_prodotti, 'salva_dati'):
                    gestore_prodotti.salva_dati()
            except Exception as e:
                print(f"Errore nel salvataggio catalogo: {e}")
        # =======================================================

        # Aggiorna utente
        if not hasattr(utente, 'storico_ordini'):
            utente.storico_ordini = []
        utente.storico_ordini.append(nuovo_ordine)

        if hasattr(utente, 'svuota_carrello'):
            utente.svuota_carrello()
        else:
            carrello.clear()

        # Salva utente
        if hasattr(self.gestore_utenti, '_salva_dati'):
            self.gestore_utenti._salva_dati()
        elif hasattr(self.gestore_utenti, 'salva_dati'):
            self.gestore_utenti.salva_dati()

        QMessageBox.information(self, "Successo",
                                "Acquisto completato con successo!\nIl tuo ordine è stato registrato.")

        if self.main_window and hasattr(self.main_window, 'mostra_miei_ordini'):
            self.main_window.mostra_miei_ordini()

    def torna_indietro(self):
        if self.main_window and hasattr(self.main_window, 'mostra_dashboard_cliente'):
            self.main_window.mostra_dashboard_cliente()