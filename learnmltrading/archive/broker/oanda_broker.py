from typing import Optional, Dict, Any
import os
import time
import pandas as pd
import requests
import matplotlib.pyplot as plt

from learnmltrading.utils import time_conversion
from learnmltrading.broker import broker

JSONType = Dict[str, Any]
PRICE_COMPONENTS = "BA"  # get bid and ask candles
MAX_REQUEST_SIZE = 2500
REQUEST_SLEEP = 1.0


class OandaBroker(broker.Broker):
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
        start_dt, end_dt = (
            pd.to_datetime(ts, unit="s", origin="unix") for ts in (start, end)
        )
        time_series = pd.date_range(
            start_dt, end_dt, freq=time_conversion.oanda_to_pandas_freq(granularity)
        )

        query_timestamps = time_series[::MAX_REQUEST_SIZE].to_list()
        query_timestamps = (
            query_timestamps + [time_series[-1]]
            if query_timestamps[-1] != time_series[-1]
            else query_timestamps
        )

        dfs = []
        for i in range(len(query_timestamps) - 1):
            sub_start = time_conversion.pd_datetime_to_unix(query_timestamps[i])
            sub_end = time_conversion.pd_datetime_to_unix(query_timestamps[i + 1])
            dfs.append(
                self._get_sub_historic_price(
                    instrument, granularity, sub_start, sub_end
                )
            )
            time.sleep(REQUEST_SLEEP)
        df = pd.concat(dfs, axis=0)
        return df

    def _get_sub_historic_price(
        self, instrument: str, granularity: str, start: int, end: int
    ) -> pd.DataFrame:
        """
        Assuming that the request is valid (and the number of candles
        > MAX_REQUEST_SIZE), return the dataframe of prices.
        """
        json_candles = self._get_json_candles(instrument, granularity, start, end)
        flattened_json_candles = pd.json_normalize(json_candles)
        df = pd.DataFrame(flattened_json_candles)
        df.index = pd.to_datetime(df.time)
        df.drop(["complete", "volume", "time"], axis=1, inplace=True)
        return df.astype(float)

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


if __name__ == "__main__":
    HOST = "api-fxtrade.oanda.com"
    ACCOUNT_NUMBER = os.environ.get("OANDA_ACCOUNT_NUMBER")
    API_TOKEN = os.environ.get("OANDA_API_TOKEN")
    INSTRUMENT = "GBP_USD"
    GRANULARITY = "H4"
    START = time_conversion.pd_datetime_to_unix(pd.to_datetime("2015-12-10"))
    END = time_conversion.pd_datetime_to_unix(pd.to_datetime("2021-03-01"))

    oanda_broker = OandaBroker(HOST, None, ACCOUNT_NUMBER, API_TOKEN)
    df = oanda_broker.get_historic_prices(INSTRUMENT, GRANULARITY, START, END)

    plt.plot(df["bid.c"])
    plt.show()
    print(df.head())
    print(df.shape)
