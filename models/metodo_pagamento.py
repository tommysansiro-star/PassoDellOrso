class MetodoPagamento:
    def __init__(self, codice_carta: str, cvv: str, data_scadenza: str, nome: str):
        self._codice_carta = codice_carta
        self._cvv = cvv
        self._data_scadenza = data_scadenza
        self._nome = nome


    @property
    def codice_carta(self) -> str:
        return self._codice_carta

    @codice_carta.setter
    def codice_carta(self, valore: str):
        self._codice_carta = valore

    @property
    def cvv(self) -> str:
        return self._cvv

    @cvv.setter
    def cvv(self, valore: str):
        self._cvv = valore

    @property
    def data_scadenza(self) -> str:
        return self._data_scadenza

    @data_scadenza.setter
    def data_scadenza(self, valore: str):
        self._data_scadenza = valore

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valore: str):
        self._nome = valore