import os
import pickle
from argparse import Namespace
from models.cliente import Cliente
from models.dipendente import Dipendente


def popola_database_utenti():
    utenti_da_salvare = []

    # ==========================================
    # 1. CREAZIONE CLIENTI
    # ==========================================
    cliente_1 = Cliente(1, "Tommaso", "Ciancarelli", "tommy@mail.com", "password123", "3331234567")

    metodi_tommaso = [
        "Carta di Credito (Visa) - **** 1234",
        "PayPal - tommy@mail.com"
    ]
    if hasattr(cliente_1, 'aggiungi_metodo_pagamento'):
        for m in metodi_tommaso:
            cliente_1.aggiungi_metodo_pagamento(m)
    else:
        cliente_1._metodi_pagamento = metodi_tommaso

    # --- INSERIMENTO PRODOTTI (TRUCCO SICURO PER PICKLE) ---
    # Usiamo Namespace: crea oggetti con attributi che non fanno mai crashare pickle!
    nuovi_prodotti = [
        Namespace(nome="Skipass Giornaliero Adulti", prezzo=45.00, quantita=2),
        Namespace(nome="Assicurazione Infortuni Neve", prezzo=5.00, quantita=2),
        Namespace(nome="Noleggio Sci e Scarponi (Avanzato)", prezzo=35.50, quantita=1)
    ]

    if hasattr(cliente_1, '_prodotti_carrello'):
        cliente_1._prodotti_carrello = nuovi_prodotti
    else:
        cliente_1.prodotti_carrello.clear()
        cliente_1.prodotti_carrello.extend(nuovi_prodotti)
    # ---------------------------------------------------------

    utenti_da_salvare.append(cliente_1)

    cliente_2 = Cliente(2, "Giulia", "Rossi", "giulia@mail.com", "neve2024", "3339876543")
    if hasattr(cliente_2, 'aggiungi_metodo_pagamento'):
        cliente_2.aggiungi_metodo_pagamento("Mastercard - **** 9876")
    else:
        if hasattr(cliente_2, '_metodi_pagamento'):
            cliente_2._metodi_pagamento = ["Mastercard - **** 9876"]

    utenti_da_salvare.append(cliente_2)

    # ==========================================
    # 2. CREAZIONE DIPENDENTI
    # ==========================================
    dipendente_1 = Dipendente(3, 1, "Marco", "Verdi", "marco.admin@passodellorso.it", "admin123", "3330001111")
    utenti_da_salvare.append(dipendente_1)

    dipendente_2 = Dipendente(4, 2, "Anna", "Bianchi", "anna.staff@passodellorso.it", "staff123", "3330002222")
    utenti_da_salvare.append(dipendente_2)

    # ==========================================
    # 3. SALVATAGGIO NEL FILE PICKLE
    # ==========================================
    percorso_file = "data/utenti.pickle"
    os.makedirs(os.path.dirname(percorso_file), exist_ok=True)

    with open(percorso_file, "wb") as f:
        pickle.dump(utenti_da_salvare, f)

    print(f"✅ Popolamento completato! Inseriti {len(utenti_da_salvare)} utenti.")
    print("Prodotti aggiunti al carrello di Tommaso con Namespace sicuri.")


if __name__ == "__main__":
    popola_database_utenti()