from datetime import date, datetime, timedelta
from models.enums import Difficolta, StatoApertura, FormulaTemporale, Livello, TipologiaAttrezzatura, StatoOrdine
from models.pista import Pista
from models.skipass import SkiPass
from models.attrezzatura import Attrezzatura
from models.lezione import Lezione
from models.assicurazione import Assicurazione
from models.metodo_pagamento import MetodoPagamento
from models.prodotto_carrello import ProdottoCarrello
from models.prodotto_ordine import ProdottoOrdine
from models.ordine import Ordine


def main():
    print("=" * 60)
    print("TEST DEL SISTEMA - PASSO DELL'ORSO (AGGIORNATO)")
    print("=" * 60 + "\n")

    # 1. TEST PISTE
    pista1 = Pista(id_pista=1, nome="Direttissima", difficolta=Difficolta.NERA, stato_apertura=StatoApertura.APERTA)
    pista2 = Pista(id_pista=2, nome="Raccordo", difficolta=Difficolta.AZZURRA, stato_apertura=StatoApertura.CHIUSA)

    print("⛷️ GESTIONE PISTE:")
    print(f" - {pista1.nome} | Difficoltà: {pista1.difficolta.name} | Stato: {pista1.stato_apertura.name}")
    pista2.stato_apertura = StatoApertura.MANUTENZIONE
    print(f" - {pista2.nome} | Difficoltà: {pista2.difficolta.name} | Stato aggiornato: {pista2.stato_apertura.name}\n")

    # 2. TEST PRODOTTI
    oggi = date.today()
    settimana_prossima = oggi + timedelta(days=7)

    # SkiPass
    skipass = SkiPass(
        id_prodotto=101, nome="SkiPass Settimanale", descrizione="Accesso 7 giorni",
        prezzo=250.0, immagine="skipass.png", is_disponibile=True,
        formula_temporale=FormulaTemporale.SETTIMANALE
    )
    skipass.set_periodo_validita(oggi, settimana_prossima)

    # Attrezzatura
    sci = Attrezzatura(
        id_prodotto=102, nome="Sci Salomon", descrizione="Sci carving",
        prezzo=35.0, immagine="sci.png", is_disponibile=True,
        brand="Salomon", data=oggi, livello=Livello.INTERMEDIO,
        quantita=10, taglia="170", tipologia=TipologiaAttrezzatura.SCI
    )
    sci.decrementa_quantita(2)  # Simuliamo il noleggio di 2 paia

    # Lezione
    lezione = Lezione(
        id_prodotto=103, nome="Lezione Privata", descrizione="Maestro Andrea",
        prezzo=50.0, immagine="lezione.png", is_disponibile=True,
        data=datetime.now(), livello=Livello.PRINCIPIANTE, quantita=5
    )
    lezione.incrementa_quantita(1)  # Aggiungiamo un posto

    # Assicurazione
    assicurazione = Assicurazione(
        id_prodotto=104, nome="Assicurazione Base", descrizione="Copertura infortuni",
        prezzo=15.0, immagine="ass.png", is_disponibile=True
    )
    assicurazione.set_periodo_copertura(oggi, settimana_prossima)

    print("📦 PRODOTTI CREATI E METODI TESTATI:")
    print(f" - {skipass.nome}: Validità impostata da {skipass._data_inizio} a {skipass._data_fine}")
    print(f" - {sci.nome}: Quantità in magazzino aggiornata a {sci.quantita}")
    print(f" - {lezione.nome}: Posti disponibili aggiornati a {lezione.quantita}")
    print(f" - {assicurazione.nome}: Copertura impostata da {assicurazione._data_inizio} a {assicurazione._data_fine}\n")

    # 3. TEST METODO DI PAGAMENTO
    carta_scaduta = oggi - timedelta(days=365)
    pagamento = MetodoPagamento(
        codice_carta="1234-5678-9012-3456", cvv="123",
        data_scadenza=oggi + timedelta(days=700), nome="Mario Rossi"
    )
    print("💳 METODO DI PAGAMENTO:")
    print(f" - Carta {pagamento.codice_carta} intestata a {pagamento._nome}")
    print(f" - La carta è scaduta? {'Sì' if pagamento.is_scaduta() else 'No'}\n")

    # 4. TEST CARRELLO
    item_carrello1 = ProdottoCarrello(prodotto=skipass, quantita=2)
    item_carrello2 = ProdottoCarrello(prodotto=sci, quantita=2)

    print("🛒 TEST CARRELLO:")
    print(
        f" - {item_carrello1.quantita}x {item_carrello1.prodotto.nome} | Subtotale: {item_carrello1.calcola_subtotale()}€")
    print(
        f" - {item_carrello2.quantita}x {item_carrello2.prodotto.nome} | Subtotale: {item_carrello2.calcola_subtotale()}€\n")

    # 5. TEST ORDINE
    # Convertiamo gli elementi del carrello in righe d'ordine definitive
    riga_ordine1 = ProdottoOrdine(prodotto=skipass, quantita=2)
    riga_ordine2 = ProdottoOrdine(prodotto=sci, quantita=2)
    riga_ordine3 = ProdottoOrdine(prodotto=assicurazione, quantita=2)

    ordine = Ordine(
        id_ordine=999,
        metodo_pagamento=pagamento,
        prezzo_totale=0.0,
        prodotti=[riga_ordine1, riga_ordine2]
    )

    # Test aggiunta prodotto all'ordine e ricalcolo totale
    ordine.aggiungi_prodotto_ordine(riga_ordine3)
    ordine.calcola_prezzo_totale()
    ordine.stato = StatoOrdine.COMPLETATO

    print("🧾 RIEPILOGO ORDINE FINALE:")
    print(f" - {ordine.get_dettagli()}")
    for po in ordine._prodotti:
        print(f"   * {po.quantita}x {po.prodotto.nome}")
    print(f" - Totale Calcolato: {ordine.calcola_prezzo_totale()}€")
    print("=" * 60)


if __name__ == "__main__":
    main()