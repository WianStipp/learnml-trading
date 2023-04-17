"""Contains the OANDA Broker class"""

import enum
import httpx

from learnmltrading import time_helpers
from learnmltrading.broker import base_broker, broker_account

OANDA_LIVE_HOST = "https://api-fxtrade.oanda.com"
OANDA_DEMO_HOST = "https://api-fxpractice.oanda.com"


class OANDACandleGranularities(enum.Enum):
    """Allowed timeframes for the OANDA APIs."""

    S5 = "S5"
    S10 = "S10"
    S15 = "S15"
    S30 = "S30"
    M1 = "M1"
    M2 = "M2"
    M4 = "M4"
    M5 = "M5"
    M10 = "M10"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H2 = "H2"
    H3 = "H3"
    H4 = "H4"
    H6 = "H6"
    H8 = "H8"
    H12 = "H12"
    D = "D"
    W = "W"
    M = "M"


class OANDABroker(base_broker.Broker):
    """Global FX broker: https://www.oanda.com/"""

    def __init__(self, host: str, account: broker_account.OANDAAccount) -> None:
        super().__init__(host=host)
        self.account = account

    def get_candles(
        self,
        instrument: str,
        candle_timeframe: OANDACandleGranularities,
        timeframe: time_helpers.Timeframe,
    ):
        """Get candle data given an instrument and a timeframe."""
        candles_path = f"v3/accounts/{self.account.account_number}/instruments/{instrument}/candles"
        params = {
            "from": timeframe.start_unix,
            "to": timeframe.end_unix,
            "granularity": candle_timeframe.value,
            "price": "BA",
        }
        with httpx.Client(
            headers={"Authorization": f"Bearer {self.account.api_token}"}
        ) as client:
            response = client.get(os.path.join(self.host, candles_path), params=params)
        response.raise_for_status()
        response.text
        return response.json()


if __name__ == "__main__":
    import os

    account = broker_account.OANDAAccount(
        account_number=os.environ.get("OANDA_ACCOUNT_NUMBER"),
        api_token=os.environ.get("OANDA_API_TOKEN"),
    )
    broker = OANDABroker(OANDA_LIVE_HOST, account)
    candles = broker.get_candles(
        "EUR_USD",
        OANDACandleGranularities.H1,
        time_helpers.Timeframe.from_isoformat(
            "2023-03-29T00:00:00", "2023-03-31T00:00:00"
        ),
    )
    print(candles)
