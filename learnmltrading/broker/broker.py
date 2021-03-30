import os
from abc import ABC
import pandas as pd
import requests
from typing import Dict, Any, Optional

JSONType = Dict[str, Any]


class Broker(ABC):
    """
    Abstract class for a broker.
    """

    def __init__(self, host: str, port: Optional[str]) -> None:
        self.host = host
        self.port = port


class OandaBroker(Broker):
    """
    Concrete implementation of Broker, using the OANDA brokerage for FX trading.
    """

    def __init__(
        self, host: str, port: Optional[str], account_number: str, api_token: str
    ) -> None:
        super().__init__(host, port)
        self.account_number = account_number
        self.api_token = api_token

    def get_historic_prices(
        self, instrument: str, granularity: str, start: int, end: int
    ) -> pd.DataFrame:
        """
        Get the a dataframe of historic prices from the API.

        granularity (str): E.g. 'H1' or 'D'.

        start (int): start of price data, in UNIX seconds.

        end (int): end of price data, in UNIX seconds.
        """
        json_candles = self._get_json_candles(instrument, granularity, start, end)
        print(json_candles)
        return pd.DataFrame()

    def _get_json_candles(
        self, instrument: str, granularity: str, start: int, end: int
    ) -> JSONType:
        """
        granularity (str): E.g. 'H1' or 'D'.

        start (int): start of price data, in UNIX seconds.

        end (int): end of price data, in UNIX seconds.
        """
        start, end = str(start), str(end)

        header = {"Authorization": "Bearer " + self.api_token}
        query = {"from": start, "to": end, "granularity": granularity}
        candles_path = (
            f"/v3/accounts/{self.account_number}/instruments/{instrument}/candles"
        )

        response = requests.get(
            "https://" + self.host + candles_path, headers=header, params=query
        )
        try:
            json_candles = response.json()["candles"]
            return json_candles
        except Exception:
            print(response.status_code)
            print(response.reason)


if __name__ == "__main__":
    HOST = "api-fxtrade.oanda.com"
    ACCOUNT_NUMBER = os.environ.get("OANDA_ACCOUNT_NUMBER")
    API_TOKEN = os.environ.get("OANDA_API_TOKEN")

    oanda_broker = OandaBroker(
        HOST,
        None,
    )
