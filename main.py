import sys
from PyQt6.QtWidgets import QApplication
from views.view import LoginView
from controllers.gestore_utenti import GestoreUtenti
from controllers.gestore_mail import GestoreMail

def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    gestore_mail = GestoreMail()
    gestore_utenti = GestoreUtenti(gestore_mail)
    view = LoginView(gestore_utenti)
    view.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())