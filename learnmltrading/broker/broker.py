"""
This file contains code to interact with the broker.

To-do:

- Get bid and ask candles (not mid)
- Allow larger data queries
"""

import os
import time
from abc import ABC
import pandas as pd
import requests
from typing import Dict, Any, Optional

JSONType = Dict[str, Any]
PRICE_COMPONENTS = "BA"  # get bid and ask candles
MAX_REQUEST_SIZE = 2500
REQUEST_SLEEP = 1.0


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
        start_dt = pd.to_datetime(start, unit="s", origin="unix")
        end_dt = pd.to_datetime(end, unit="s", origin="unix")
        series = pd.date_range(start_dt, end_dt, freq=oanda_to_pandas_freq(granularity))

        query_timestamps = series[::MAX_REQUEST_SIZE].to_list()
        query_timestamps = (
            query_timestamps + [series[-1]]
            if query_timestamps[-1] != series[-1]
            else query_timestamps
        )

        dfs = []
        for i in range(len(query_timestamps) - 1):
            sub_start = pd_datetime_to_unix(query_timestamps[i])
            sub_end = pd_datetime_to_unix(query_timestamps[i + 1])
            json_candles = self._get_json_candles(
                instrument, granularity, sub_start, sub_end
            )
            flattened_json_candles = pd.json_normalize(json_candles)
            df = pd.DataFrame(flattened_json_candles)
            df.index = pd.to_datetime(df.time)
            df.drop(["complete", "volume", "time"], axis=1, inplace=True)
            dfs.append(df.astype(float))
            time.sleep(REQUEST_SLEEP)

        df = pd.concat(dfs, axis=1)
        return df

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
        query = {
            "from": start,
            "to": end,
            "granularity": granularity,
            "price": PRICE_COMPONENTS,
        }
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


def pd_datetime_to_unix(pd_datetime: pd.Timestamp) -> int:
    """
    convert pandas datetime date to UNIX seconds.
    """
    return (pd_datetime - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")


def oanda_to_pandas_freq(granularity: str) -> str:
    """
    Format the OANA granularity to be comparible with Pandas.

    For example, 'H4' -> '4H'
    """
    if "H" in granularity:
        return granularity[::-1]
    elif "M" in granularity:
        return granularity[1:] + "min"


if __name__ == "__main__":
    HOST = "api-fxtrade.oanda.com"
    ACCOUNT_NUMBER = os.environ.get("OANDA_ACCOUNT_NUMBER")
    API_TOKEN = os.environ.get("OANDA_API_TOKEN")
    INSTRUMENT = "GBP_USD"
    GRANULARITY = "H4"
    START = pd_datetime_to_unix(pd.to_datetime("2010-12-10"))
    END = pd_datetime_to_unix(pd.to_datetime("2021-03-01"))

    oanda_broker = OandaBroker(HOST, None, ACCOUNT_NUMBER, API_TOKEN)
    df = oanda_broker.get_historic_prices(INSTRUMENT, GRANULARITY, START, END)

    print(df.head())
