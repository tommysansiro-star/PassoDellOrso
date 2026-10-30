
import sys
import traceback

import datetime


def risana_prodotti_scaduti(gestore_utenti, gestore_prodotti):
    """Controlla gli ordini passati e restituisce la quantità al catalogo se la data è superata."""
    oggi = datetime.datetime.now()
    dati_modificati_utenti = False
    dati_modificati_prodotti = False

    lista_utenti = getattr(gestore_utenti, '_utenti', getattr(gestore_utenti, 'utenti', []))
    lista_prodotti_db = getattr(gestore_prodotti, '_prodotti', getattr(gestore_prodotti, 'prodotti', []))

    for utente in lista_utenti:
        storico = getattr(utente, 'storico_ordini', getattr(utente, '_storico_ordini', []))
        for ordine in storico:
            stato = getattr(ordine, 'stato', '')

            # Se l'ordine è completato, controlliamo la data
            if stato == "COMPLETATO":  # Sostituisci con il valore del tuo Enum se usi un Enum
                data_ordine_str = getattr(ordine, 'data', '')
                try:
                    # Converte la stringa della data dell'ordine (formato dd/mm/yyyy HH:MM)
                    data_ordine = datetime.datetime.strptime(data_ordine_str, "%d/%m/%Y %H:%M")

                    # Se è passato un giorno (24 ore) dall'ordine, consideriamo il prodotto "restituito"
                    if (oggi - data_ordine).days >= 1:

                        # Ripristina le quantità nel catalogo
                        for item in getattr(ordine, 'prodotti',
                                            []):  # Presupponendo di aver salvato gli item, o si usa una logica simile
                            nome_item = getattr(item, 'nome', '')
                            qta_item = getattr(item, 'quantita', 1)

                            for prod_db in lista_prodotti_db:
                                nome_db = getattr(prod_db, 'nome', getattr(prod_db, '_nome', ''))
                                if nome_db == nome_item:
                                    if hasattr(prod_db, 'quantita'):
                                        prod_db.quantita += qta_item
                                    elif hasattr(prod_db, '_quantita'):
                                        prod_db._quantita += qta_item
                                    dati_modificati_prodotti = True
                                    break

                        # Aggiorna lo stato dell'ordine per non risanarlo due volte
                        ordine.stato = "RESTITUITO"  # Sostituisci con il tuo Enum
                        dati_modificati_utenti = True
                except ValueError:
                    pass  # Se la data non è formattata bene, salta

    # Salva i database se ci sono state modifiche
    if dati_modificati_prodotti:
        if hasattr(gestore_prodotti, '_salva_dati'):
            gestore_prodotti._salva_dati()
        elif hasattr(gestore_prodotti, 'salva_dati'):
            gestore_prodotti.salva_dati()

    if dati_modificati_utenti:
        if hasattr(gestore_utenti, '_salva_dati'):
            gestore_utenti._salva_dati()
        elif hasattr(gestore_utenti, 'salva_dati'):
            gestore_utenti.salva_dati()

# Aggiungi questa funzione per catturare i crash silenziosi di PyQt6
def cattura_errori(tipo_eccezione, valore_eccezione, traceback_eccezione):
    print("\n" + "!"*50)
    print("ERRORE FATALE TROVATO:")
    traceback.print_exception(tipo_eccezione, valore_eccezione, traceback_eccezione)
    print("!"*50 + "\n")
    sys.exit(1)

sys.excepthook = cattura_errori
from PyQt6.QtWidgets import QApplication

from controllers.gestore_utenti import GestoreUtenti
from controllers.gestore_mail import GestoreMail
from controllers.gestore_prodotti import GestoreProdotti
from controllers.gestore_ordini import GestoreOrdini
from controllers.gestore_piste import GestorePiste
from views.main_window import MainWindow

def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
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
    risana_prodotti_scaduti(gestore_utenti, gestore_prodotti)
    window = MainWindow(gestore_utenti, gestore_ordini, gestore_prodotti, gestore_piste)
    window.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())