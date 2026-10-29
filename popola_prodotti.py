from controllers.gestore_prodotti import GestoreProdotti
from models.prodotto import Prodotto


def popola_database():
    gestore = GestoreProdotti()

    # Svuotiamo la lista per evitare duplicati
    gestore._prodotti = []

    # Creazione dei prodotti con tutti i parametri richiesti
    prodotti_da_inserire = [
        Prodotto(id_prodotto=1, nome="Skipass Giornaliero", prezzo=45.00, descrizione="Accesso valido per 1 giorno",
                 immagine="", is_disponibile=True),
        Prodotto(id_prodotto=2, nome="Skipass Settimanale", prezzo=250.00, descrizione="Accesso valido per 7 giorni",
                 immagine="", is_disponibile=True),
        Prodotto(id_prodotto=3, nome="Noleggio Sci Completo", prezzo=35.00,
                 descrizione="Sci, scarponi e racchette per 1 giorno", immagine="", is_disponibile=True),
        Prodotto(id_prodotto=4, nome="Noleggio Snowboard", prezzo=35.00, descrizione="Tavola e scarponi per 1 giorno",
                 immagine="", is_disponibile=True),
        Prodotto(id_prodotto=5, nome="Lezione Privata 1h", prezzo=50.00, descrizione="Lezione singola con maestro FISI",
                 immagine="", is_disponibile=True),
        Prodotto(id_prodotto=6, nome="Assicurazione Infortuni", prezzo=5.00,
                 descrizione="Copertura medica giornaliera sulle piste", immagine="", is_disponibile=True)
    ]

    # Inserimento tramite il metodo del controller
    for p in prodotti_da_inserire:
        gestore.inserisciNuovoProdotto(p)

    print(f"✅ {len(gestore.get_tutti_prodotti())} prodotti creati e salvati correttamente in data/prodotti.pickle!")


if __name__ == "__main__":
    popola_database()