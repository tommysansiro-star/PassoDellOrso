from controllers.gestore_piste import GestorePiste
from models.pista import Pista
from models.enums import Difficolta, StatoApertura


def popola_database():
    gestore = GestorePiste()

    # Svuotiamo la lista per evitare duplicati
    if hasattr(gestore, 'piste'):
        gestore.piste = []
    elif hasattr(gestore, '_piste'):
        gestore._piste = []

    # Creazione delle piste mescolando le difficoltà e gli stati di apertura
    piste_da_inserire = [
        Pista(id_pista=1, nome="Azzurra Neve", difficolta=Difficolta.AZZURRA, stato_apertura=StatoApertura.APERTA),
        Pista(id_pista=2, nome="Rossa Tramonto", difficolta=Difficolta.ROSSA,
              stato_apertura=StatoApertura.MANUTENZIONE),
        Pista(id_pista=3, nome="Nera Abisso", difficolta=Difficolta.NERA, stato_apertura=StatoApertura.CHIUSA),
        Pista(id_pista=4, nome="Baby Park", difficolta=Difficolta.AZZURRA,
              stato_apertura=StatoApertura.MANUTENZIONE),
        Pista(id_pista=5, nome="Direttissima", difficolta=Difficolta.NERA, stato_apertura=StatoApertura.APERTA)
    ]

    # Inserimento
    for pista in piste_da_inserire:
        if hasattr(gestore, 'inserisciPista'):
            gestore.inserisciPista(pista)
        elif hasattr(gestore, 'aggiungi_pista'):
            gestore.aggiungi_pista(pista)
        else:
            # Fallback
            if hasattr(gestore, 'piste'):
                gestore.piste.append(pista)
            elif hasattr(gestore, '_piste'):
                gestore._piste.append(pista)
            gestore._salva_dati()

    print(f"✅ {len(piste_da_inserire)} piste create e salvate correttamente in data/piste.pickle!")


if __name__ == "__main__":
    popola_database()