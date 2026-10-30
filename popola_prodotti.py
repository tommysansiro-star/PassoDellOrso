import os
import pickle
from datetime import date, datetime, timedelta

from models.skipass import SkiPass
from models.assicurazione import Assicurazione
from models.attrezzatura import Attrezzatura
from models.lezione import Lezione

# Importa i tuoi Enum reali
from models.enums import FormulaTemporale

# Presumo che tu abbia anche questi Enum, scommentali o cambiali in base al tuo codice:
# from models.enums import Livello, TipologiaAttrezzatura

# Se non hai gli Enum per Livello e Tipologia, usiamo delle stringhe come fallback nello script,
# ma ti consiglio di importarli dal tuo file enums.py come fatto per FormulaTemporale.
LIVELLI = ["PRINCIPIANTE", "INTERMEDIO", "AVANZATO", "ESPERTO"]
TIPOLOGIE_ATTREZZATURA = ["SCI", "SNOWBOARD", "CASCO", "SCARPONI", "TUTA"]


def popola_database_prodotti():
    prodotti_da_salvare = []
    id_counter = 1  # Contatore per generare ID univoci per ogni prodotto

    # Definiamo la stagione sciistica
    inizio_stagione = date(2025, 12, 1)
    fine_stagione = date(2026, 4, 30)

    print("Generazione dei prodotti in corso. Potrebbe richiedere qualche secondo...")

    # ==========================================
    # 1. SKIPASS STAGIONALE (Unico per tutta la stagione)
    # ==========================================
    prodotti_da_salvare.append(SkiPass(
        id_prodotto=id_counter,
        nome="Skipass Stagionale 2025-2026",
        descrizione="Accesso illimitato per tutta la stagione invernale.",
        prezzo=450.00,
        immagine="nessuna_immagine.png",
        is_disponibile=True,
        formula_temporale=FormulaTemporale.STAGIONALE,
        data_inizio=inizio_stagione,
        data_fine=fine_stagione
    ))
    id_counter += 1

    # ==========================================
    # CICLO GIORNALIERO (Genera prodotti per OGNI giorno)
    # ==========================================
    giorno_corrente = inizio_stagione

    # Dati per le combinazioni
    maestri = ["Marco", "Anna", "Luca"]
    orari_lezioni = [9, 11, 14]  # Ore 9:00, 11:00 e 14:00
    brand_map = {
        "SCI": "Salomon",
        "SNOWBOARD": "Burton",
        "CASCO": "Giro",
        "SCARPONI": "Nordica",
        "TUTA": "Colmar"
    }

    while giorno_corrente <= fine_stagione:

        # --- SKIPASS MENSILE (Generato solo il 1° di ogni mese) ---
        if giorno_corrente.day == 1:
            # Calcola l'ultimo giorno del mese
            mese_successivo = giorno_corrente.replace(day=28) + timedelta(days=4)
            fine_mese = mese_successivo - timedelta(days=mese_successivo.day)

            prodotti_da_salvare.append(SkiPass(
                id_prodotto=id_counter,
                nome=f"Skipass Mensile ({giorno_corrente.strftime('%B %Y')})",
                descrizione="Accesso valido per tutto il mese.",
                prezzo=150.00,
                immagine="nessuna_immagine.png",
                is_disponibile=True,
                formula_temporale=FormulaTemporale.MENSILE,
                data_inizio=giorno_corrente,
                data_fine=fine_mese
            ))
            id_counter += 1

        # --- SKIPASS SETTIMANALE (Generato ogni Lunedì) ---
        if giorno_corrente.weekday() == 0:  # 0 = Lunedì
            prodotti_da_salvare.append(SkiPass(
                id_prodotto=id_counter,
                nome=f"Skipass Settimanale (dal {giorno_corrente.strftime('%d/%m')})",
                descrizione="Accesso valido per 7 giorni.",
                prezzo=180.00,
                immagine="nessuna_immagine.png",
                is_disponibile=True,
                formula_temporale=FormulaTemporale.SETTIMANALE,
                data_inizio=giorno_corrente,
                data_fine=giorno_corrente + timedelta(days=6)
            ))
            id_counter += 1

        # --- SKIPASS GIORNALIERO ---
        prodotti_da_salvare.append(SkiPass(
            id_prodotto=id_counter,
            nome=f"Skipass Giornaliero ({giorno_corrente.strftime('%d/%m/%Y')})",
            descrizione="Accesso completo agli impianti per la giornata.",
            prezzo=45.00,
            immagine="nessuna_immagine.png",
            is_disponibile=True,
            formula_temporale=FormulaTemporale.GIORNALIERO,
            data_inizio=giorno_corrente,
            data_fine=giorno_corrente
        ))
        id_counter += 1

        # --- ASSICURAZIONE GIORNALIERA ---
        prodotti_da_salvare.append(Assicurazione(
            id_prodotto=id_counter,
            nome=f"Assicurazione Giornaliera ({giorno_corrente.strftime('%d/%m/%Y')})",
            descrizione="Copertura completa sulle piste.",
            prezzo=5.00,
            immagine="nessuna_immagine.png",
            is_disponibile=True,
            data_inizio=giorno_corrente,
            data_fine=giorno_corrente
        ))
        id_counter += 1

        # --- ATTREZZATURA (Tutte le combinazioni per questo giorno) ---
        for tipologia in TIPOLOGIE_ATTREZZATURA:
            for livello in LIVELLI:
                prodotti_da_salvare.append(Attrezzatura(
                    id_prodotto=id_counter,
                    nome=f"Noleggio {tipologia.capitalize()} {livello.capitalize()}",
                    descrizione=f"Attrezzatura revisionata per livello {livello.lower()}.",
                    prezzo=25.00,
                    immagine="nessuna_immagine.png",
                    is_disponibile=True,
                    brand=brand_map[tipologia],
                    data=giorno_corrente,
                    livello=livello,  # Sostituisci con Livello.NOME se usi l'Enum
                    quantita=5,
                    taglia="M",
                    tipologia=tipologia  # Sostituisci con TipologiaAttrezzatura.NOME se usi l'Enum
                ))
                id_counter += 1

        # --- LEZIONI (Tutte le combinazioni per questo giorno) ---
        for ora in orari_lezioni:
            for maestro in maestri:
                for livello in ["PRINCIPIANTE", "AVANZATO"]:  # Limitato a 2 livelli per non moltiplicare troppo
                    data_ora_lezione = datetime(giorno_corrente.year, giorno_corrente.month, giorno_corrente.day, ora,
                                                0)
                    prodotti_da_salvare.append(Lezione(
                        id_prodotto=id_counter,
                        nome=f"Lezione {livello.capitalize()} con {maestro}",
                        descrizione=f"Lezione di 1 ora alle {ora}:00.",
                        prezzo=40.00,
                        immagine="nessuna_immagine.png",
                        is_disponibile=True,
                        data=data_ora_lezione,
                        livello=livello,
                        quantita=3
                    ))
                    id_counter += 1

        # Passa al giorno successivo
        giorno_corrente += timedelta(days=1)

    # Salvataggio nel file pickle
    percorso_file = "data/prodotti.pickle"
    os.makedirs(os.path.dirname(percorso_file), exist_ok=True)

    with open(percorso_file, "wb") as f:
        pickle.dump(prodotti_da_salvare, f)

    print(f"✅ Popolamento completato! Inseriti {len(prodotti_da_salvare)} prodotti REALI nel catalogo.")
    print("Database pronto per la stagione 2025-2026.")


if __name__ == "__main__":
    popola_database_prodotti()