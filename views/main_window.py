from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from views.login_view import LoginView
from views.registrazione_view import RegistrazioneView


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
        """Istanzia tutte le schermate e le aggiunge allo stack."""
        # Creiamo le view passando il controller necessario e 'self' come main_window
        self.login_view = LoginView(self.gestore_utenti, main_window=self)
        self.registrazione_view = RegistrazioneView(self.gestore_utenti, main_window=self)

        # Aggiungiamo le view al QStackedWidget
        self.stacked_widget.addWidget(self.login_view)  # Indice 0
        self.stacked_widget.addWidget(self.registrazione_view)  # Indice 1

        # Impostiamo la schermata iniziale da mostrare all'avvio
        self.mostra_login()

    def mostra_login(self):
        """Passa alla pagina di Login."""
        self.stacked_widget.setCurrentWidget(self.login_view)

    def mostra_registrazione(self):
        """Passa alla pagina di Registrazione."""
        self.stacked_widget.setCurrentWidget(self.registrazione_view)

    def mostra_area_cliente(self):
        """TODO: Passa alla dashboard del cliente."""
        pass

    def mostra_area_dipendente(self):
        """TODO: Passa alla dashboard del dipendente."""
        pass