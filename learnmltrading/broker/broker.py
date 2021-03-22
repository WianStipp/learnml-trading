#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import pandas as pd


class Broker(ABC):
    def __init__(self, host: str, port: str) -> None:
        self.host = host
        self.port = port

    def get_historic_prices(
        self, instrument: str, granularity: str, start: int, end: int
    ) -> pd.DataFrame:
        return pd.DataFrame()