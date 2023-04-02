"""
This script tests out using the Backtesting.py package with our own data from OANDA.
Most of this script is taken from the Backtesting.py docs.
"""
import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from learnmltrading.broker.oanda_broker import OandaBroker
from learnmltrading.utils.config import Config
from learnmltrading.utils.time_conversion import pd_datetime_to_unix

OANDA_HOST = "api-fxtrade.oanda.com"
START = pd_datetime_to_unix(pd.to_datetime("2019-12-10"))
END = pd_datetime_to_unix(pd.to_datetime("2021-03-01"))
INSTRUMENT = "EUR_USD"
GRANULARITY = "H8"
REQUIRED_COLS = ("Open", "High", "Low", "Close")
OANDA_CORRESPONDING_COLS = ("ask.o", "ask.h", "ask.l", "ask.c")


def SMA(values, n):
    """
    Return simple moving average of `values`, at
    each step taking into account `n` previous values.
    """
    return pd.Series(values).rolling(n).mean()


class SmaCross(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20

    def init(self):
        # Precompute the two moving averages
        self.sma1 = self.I(SMA, self.data.Close, self.n1)
        self.sma2 = self.I(SMA, self.data.Close, self.n2)

    def next(self):
        # If sma1 crosses above sma2, close any existing
        # short trades, and buy the asset
        if crossover(self.sma1, self.sma2):
            self.position.close()
            self.buy()

        # Else, if sma1 crosses below sma2, close any existing
        # long trades, and sell the asset
        elif crossover(self.sma2, self.sma1):
            self.position.close()
            self.sell()


def format_prices_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Format prices dataframe from OANDA for Backtesting.py
    """
    df = df[list(OANDA_CORRESPONDING_COLS)]
    df.columns = REQUIRED_COLS
    return df


def main() -> None:
    config = Config(
        {
            "OANDA_ACCOUNT_NUMBER": "account number for OANDA",
            "OANDA_API_TOKEN": "api token for OANDA account",
        }
    )
    broker = OandaBroker(
        OANDA_HOST, None, config.OANDA_ACCOUNT_NUMBER, config.OANDA_API_TOKEN
    )
    eur_usd = broker.get_historic_prices(INSTRUMENT, GRANULARITY, START, END)
    eur_usd = format_prices_df(eur_usd)

    backtest = Backtest(eur_usd, SmaCross, cash=10_000, commission=0.02)
    stats = backtest.run()
    print(stats)

    backtest.plot()


if __name__ == "__main__":
    main()
