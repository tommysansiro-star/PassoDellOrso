from datetime import date
from models.enums import Difficolta, StatoApertura, FormulaTemporale, Livello, TipologiaAttrezzatura, StatoOrdine
from models.metodo_pagamento import MetodoPagamento
from models.cliente import Cliente
from models.dipendente import Dipendente
from models.skipass import Skipass
from models.attrezzatura import Attrezzatura
from models.lezione import Lezione
from models.assicurazione import Assicurazione
from models.prodotto_ordine import ProdottoOrdine
from models.ordine import Ordine
from models.pista import Pista


def main():
    print("=" * 60)
    print("      TEST DEL SISTEMA - PROGETTO PASSO DELL'ORSO")
    print("=" * 60 + "\n")

    # 1. Test Metodi di Pagamento e Utenti (Cliente e Dipendente)
    pagamento_1 = MetodoPagamento(1, "4000-1234-5678-9010", "123", "12/28")

    cliente = Cliente(
        id_utente=1,
        nome="Mario",
        cognome="Rossi",
        email="mario.rossi@email.com",
        password="password123",
        numero_telefono="3331234567",
        metodi_pagamento=[pagamento_1]
    )

    dipendente = Dipendente(
        id_utente=2,
        id_dipendente=101,
        nome="Anna",
        cognome="Verdi",
        email="anna.verdi@passodellorso.it",
        password="admin456",
        numero_telefono="3339876543"
    )

    print(f"👤 CLILENTE CREATO: {cliente.nome} {cliente.cognome}")
    print(f"   - Ruolo: {cliente.get_ruolo()}")
    print(f"   - Email: {cliente.email}")
    print(f"   - Data Registrazione: {cliente.data_creazione}")
    print(f"   - Metodi di pagamento salvati: {len(cliente.metodi_pagamento)}")

    print(f"\n👩‍💼 DIPENDENTE CREATO: {dipendente.nome} {dipendente.cognome}")
    print(f"   - Ruolo: {dipendente.get_ruolo()}")
    print(f"   - ID Dipendente: {dipendente.id_dipendente}")
    print("-" * 60)

    # 2. Test dei Prodotti (Ereditarietà da Prodotto e calcolo prezzi)
    skipass = Skipass(
        id_prodotto=1,
        nome="Skipass Settimanale",
        descrizione="Accesso impianti per 7 giorni",
        prezzo=40.0,
        formula_temporale=FormulaTemporale.SETTIMANALE,
        data_inizio=date(2026, 3, 1),
        data_fine=date(2026, 3, 8)
    )

    attrezzatura = Attrezzatura(
        id_prodotto=2,
        nome="Set Sci Alpino",
        descrizione="Sci, scarponi e bastoncini",
        prezzo=25.0,
        tipologia=TipologiaAttrezzatura.SCI,
        brand="Salomon",
        taglia="175",
        livello=Livello.INTERMEDIO,
        formula_temporale=FormulaTemporale.GIORNALIERO
    )

    lezione = Lezione(
        id_prodotto=3,
        nome="Lezione Privata Sci",
        descrizione="Lezione individuale con maestro esperto",
        prezzo=50.0,
        nome_maestro="Marco Maestri",
        livello=Livello.PRINCIPIANTE,
        numero_partecipanti=1
    )

    assicurazione = Assicurazione(
        id_prodotto=4,
        nome="Assicurazione Base",
        descrizione="Copertura infortuni e responsabilità civile",
        prezzo_giornaliero=5.0,
        copre_terzi=True
    )

    print("🎿 PRODOTTI DISPONIBILI:")
    print(f" - {skipass.nome} | Prezzo calcolato: {skipass.calcola_prezzo()}€")
    print(f" - {attrezzatura.nome} ({attrezzatura.brand}) | Prezzo calcolato: {attrezzatura.calcola_prezzo()}€")
    print(f" - {lezione.nome} (Maestro: {lezione.nome_maestro}) | Prezzo calcolato: {lezione.calcola_prezzo()}€")
    print(f" - {assicurazione.nome} | Prezzo calcolato: {assicurazione.calcola_prezzo()}€")
    print("-" * 60)

    # 3. Test Ordini e Righe Ordine (ProdottoOrdine)
    riga_1 = ProdottoOrdine(id_prodotto_ordine=1, prodotto=skipass, quantita=1)
    riga_2 = ProdottoOrdine(id_prodotto_ordine=2, prodotto=attrezzatura, quantita=2)
    riga_3 = ProdottoOrdine(id_prodotto_ordine=3, prodotto=assicurazione, quantita=1)

    # Creazione dell'ordine associato al cliente e al metodo di pagamento
    ordine = Ordine(
        id_ordine=501,
        prodotti=[riga_1, riga_2, riga_3],
        metodo_pagamento=pagamento_1,
        stato=StatoOrdine.COMPLETATO
    )

    # Aggiungiamo l'ordine allo storico del cliente
    cliente.aggiungi_ordine(ordine)

    print(f"📦 ORDINE CREATO #{ordine.id_ordine}")
    print(f"   - Cliente: {ordine.metodo_pagamento.codice_carta}")
    print(f"   - Stato Attuale: {ordine.stato.value.upper()}")
    print(f"   - Prezzo Totale: {ordine.prezzo_totale}€")
    print("   - Dettaglio Articoli:")
    for item in ordine.prodotti:
        print(f"     * {item.prodotto.nome} (Q.tà: {item.quantita}) - Subtotale: {item.get_subtotale()}€")
    print("-" * 60)

    # 4. Test del flusso di Rimborso sull'ordine
    print("🔄 TEST FLUSSO RIMBORSO:")
    print(f"   Stato iniziale: {ordine.stato.value}")

    ordine.richiedi_rimborso()
    print(f"   -> Dopo richiesta: {ordine.stato.value}")

    ordine.avvia_elaborazione_rimborso()
    print(f"   -> In elaborazione: {ordine.stato.value}")

    ordine.completa_rimborso()
    print(f"   -> Stato finale: {ordine.stato.value}")
    print("-" * 60)

    # 5. Test Piste dell'Impianto
    pista_1 = Pista(1, "Direttissima", Difficolta.NERA, StatoApertura.APERTA)
    pista_2 = Pista(2, "Panorama", Difficolta.AZZURRA, StatoApertura.CHIUSA)

    print("⛷️ STATO PISTE:")
    print(
        f" - Pista: {pista_1.nome} | Difficoltà: {pista_1.difficolta.value.upper()} | Stato: {pista_1.stato_apertura.value.upper()}")
    print(
        f" - Pista: {pista_2.nome} | Difficoltà: {pista_2.difficolta.value.upper()} | Stato: {pista_2.stato_apertura.value.upper()}")

    # Test del setter sulla pista
    pista_2.stato_apertura = StatoApertura.APERTA
    print(f"   [Aggiornamento] La pista '{pista_2.nome}' adesso è: {pista_2.stato_apertura.value.upper()}")

    print("\n" + "=" * 60)
    print("      TUTTI I TEST ESEGUITI CON SUCCESSO!")
    print("=" * 60)


if __name__ == "__main__":
    main()