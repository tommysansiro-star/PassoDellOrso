from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from views.login_view import LoginView
from views.registrazione_view import RegistrazioneView
from views.dashboard_cliente_view import DashboardClienteView
from views.catalogo_view import CatalogoView
from views.profilo_view import ProfiloView


class MainWindow(QMainWindow):
    def __init__(self, gestore_utenti, gestore_ordini, gestore_prodotti, gestore_piste):
        super().__init__()

        # Salviamo i controller per poterli passare alle future schermate
        self.gestore_utenti = gestore_utenti
        self.gestore_ordini = gestore_ordini
        self.gestore_prodotti = gestore_prodotti
        self.gestore_piste = gestore_piste

        # Configurazione base della finestra
        self.setWindowTitle("Passo dell'Orso - Ski Resort")
        self.setMinimumSize(900, 600)

        # Inizializziamo il contenitore a strati
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.inizializza_viste()

    def inizializza_viste(self):
        """Istanzia tutte le schermate e le aggiunge allo stack con i nomi corretti."""
        self.login_view = LoginView(self.gestore_utenti, main_window=self)
        self.registrazione_view = RegistrazioneView(self.gestore_utenti, main_window=self)

        # Nome dell'attributo corretto e allineato
        self.dashboard_cliente_view = DashboardClienteView(self.gestore_utenti, self.gestore_piste, main_window=self)
        self.catalogo_view = CatalogoView(self.gestore_prodotti, main_window=self)

        self.profilo_view = ProfiloView(self.gestore_utenti, main_window=self)
        self.stacked_widget.addWidget(self.profilo_view)

        # Aggiungiamo le view al QStackedWidget
        self.stacked_widget.addWidget(self.login_view)  # Indice 0
        self.stacked_widget.addWidget(self.registrazione_view)  # Indice 1
        self.stacked_widget.addWidget(self.dashboard_cliente_view)  # Indice 2
        self.stacked_widget.addWidget(self.catalogo_view)  # Indice 3

        self.mostra_login()

    def mostra_login(self):
        """Passa alla pagina di Login."""
        self.stacked_widget.setCurrentWidget(self.login_view)

    def mostra_registrazione(self):
        """Passa alla pagina di Registrazione."""
        self.stacked_widget.setCurrentWidget(self.registrazione_view)

    def mostra_prodotti(self):
        """Passa al catalogo prodotti aggiornando i dati."""
        self.catalogo_view.aggiorna_dati()
        self.stacked_widget.setCurrentWidget(self.catalogo_view)

    def mostra_area_cliente(self):
        """Passa alla dashboard del cliente aggiornando prima i dati e il nome utente."""
        self.dashboard_cliente_view.aggiorna_dati()
        self.stacked_widget.setCurrentWidget(self.dashboard_cliente_view)

    def mostra_profilo(self):
            """Aggiorna i dati e passa alla pagina profilo."""
            self.profilo_view.aggiorna_dati()
            self.stacked_widget.setCurrentWidget(self.profilo_view)

    def mostra_miei_ordini(self):
            """Passa alla pagina ordini (Da creare in futuro)."""
            print("WIP: Pagina ordini non ancora creata")
            # self.stacked_widget.setCurrentWidget(self.ordini_view)

    def mostra_modifica_credenziali(self):
            """Passa alla pagina modifica credenziali (Da creare in futuro)."""
            print("WIP: Pagina modifica credenziali non ancora creata")
            # self.stacked_widget.setCurrentWidget(self.modifica_credenziali_view)

    def mostra_dashboard_cliente(self):
        """Alias di compatibilità per il tasto indietro del catalogo."""
        self.mostra_area_cliente()

    def mostra_area_dipendente(self):
        """Passa alla dashboard del dipendente."""
        pass