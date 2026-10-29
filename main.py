import sys
from PyQt6.QtWidgets import QApplication

from controllers import gestore_prodotti
from views.login_view import LoginView
from views.registrazione_view import RegistrazioneView
from controllers.gestore_utenti import GestoreUtenti
from controllers.gestore_mail import GestoreMail
from controllers.gestore_prodotti import GestoreProdotti
from controllers.gestore_ordini import GestoreOrdini
from controllers.gestore_piste import GestorePiste
from views.main_window import MainWindow

def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
                font-family: Arial, sans-serif;
            }
        """)
    gestore_mail = GestoreMail()
    gestore_utenti = GestoreUtenti(gestore_mail)
    gestore_prodotti = GestoreProdotti()
    gestore_ordini = GestoreOrdini(gestore_mail, gestore_prodotti)
    gestore_piste = GestorePiste()
    window = MainWindow(gestore_utenti, gestore_ordini, gestore_prodotti, gestore_piste)
    if gestore_utenti.getUtenteByMail("admin@passodellorso.it") is None:
        gestore_utenti.registraDipendente("Admin", "Principale", "admin@passodellorso.it", "admin12345", "0000000000")
    window.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())