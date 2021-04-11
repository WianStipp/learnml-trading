"""
This file contains common functions for converting between different
time formats.
"""
import pandas as pd


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
