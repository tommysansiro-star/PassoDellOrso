from datetime import datetime
from models.ordine import Ordine
from models.enums import StatoOrdine

class GestoreMail:
    def __init__(self):
        self._indirizzoMittente: str = "noreply@impiantosciistico.it"

    def formattaCorpoMessaggio(self, oggetto: str, testo: str) -> str:
        """Formatta il messaggio standard per tutte le comunicazioni."""
        bordo = "=" * 50
        messaggio = (
            f"\n{bordo}\n"
            f"DA: {self._indirizzoMittente}\n"
            f"OGGETTO: {oggetto}\n"
            f"{bordo}\n\n"
            f"{testo}\n\n"
            f"{bordo}\n"
        )
        return messaggio

    def _simula_invio(self, email_destinatario: str, oggetto: str, testo: str) -> bool:
        """Metodo privato di utilità per stampare la finta email in console."""
        corpo = self.formattaCorpoMessaggio(oggetto, testo)
        print(f"-> Simulazione invio email a [{email_destinatario}]: {corpo}")
        return True

    def inviaEmailBenvenuto(self, email_destinatario: str, nome: str) -> None:
        """Inviata dopo la registrazione di un Cliente o Dipendente."""
        oggetto = "Benvenuto nel nostro Impianto Sciistico!"
        testo = f"Ciao {nome},\nGrazie per esserti registrato sul nostro portale."
        self._simula_invio(email_destinatario, oggetto, testo)

    def inviaEmailRecupero(self, email_destinatario: str) -> bool:
        """Inviata quando l'utente dimentica la password."""
        oggetto = "Recupero Credenziali"
        testo = "Abbiamo ricevuto una richiesta di ripristino per la tua password.\nUsa il codice 123456 per reimpostarla."
        return self._simula_invio(email_destinatario, oggetto, testo)

    def inviaEmailModificaCredenziali(self, email_destinatario: str) -> None:
        """Inviata come notifica di sicurezza dopo un cambio password."""
        oggetto = "Avviso di Sicurezza: Password Modificata"
        testo = f"Ti informiamo che la password del tuo account ({email_destinatario}) è stata cambiata in data {datetime.now().strftime('%d/%m/%Y %H:%M')}."
        self._simula_invio(email_destinatario, oggetto, testo)

    def inviaEmailConferma(self, email_destinatario: str, ordine) -> bool:
        """Inviata dopo il checkout completato."""
        oggetto = f"Conferma Ordine #{ordine.id}"
        testo = f"Il tuo acquisto è andato a buon fine!\nHai acquistato {len(ordine.prodotti)} articoli.\nData ordine: {ordine.dataAcquisto.strftime('%d/%m/%Y')}"
        return self._simula_invio(email_destinatario, oggetto, testo)

    def inviaEmailModificaOrdine(self, email_destinatario: str, ordine) -> None:
        """Inviata se il dipendente apporta variazioni ai prodotti dell'ordine."""
        oggetto = f"Modifica apportata all'Ordine #{ordine.id}"
        testo = "Ti comunichiamo che il tuo ordine è stato aggiornato dal nostro staff. Controlla la tua area riservata per i dettagli."
        self._simula_invio(email_destinatario, oggetto, testo)

    def inviaEmailStatoRimborso(self, email_destinatario: str, ordine, stato_rimborso) -> None:
        """Inviata quando il dipendente accetta o rifiuta il rimborso."""
        oggetto = f"Aggiornamento richiesta rimborso (Ordine #{ordine.id})"
        testo = f"La tua richiesta di rimborso per l'ordine #{ordine.id} è passata allo stato: {stato_rimborso.name}."
        self._simula_invio(email_destinatario, oggetto, testo)