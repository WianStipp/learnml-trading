from abc import ABC
import pandas as pd


class Broker(ABC):
    """
    Abstract class for a broker.
    """

    def __init__(self, host: str, port: str) -> None:
        self.host = host
        self.port = port


class OandaBroker(Broker):
    def __init__(
        self, host: str, port: str, account_number: str, api_token: str
    ) -> None:
        super().__init__(host, port)
        self.account_number = account_number
        self.api_token = api_token

    def get_historic_prices(
        self, instrument: str, granularity: str, start: int, end: int
    ) -> pd.DataFrame:
        return pd.DataFrame()
