"""
This file contains code to interact with the broker.
"""

from typing import Optional
from abc import ABC


class Broker(ABC):
    """
    Abstract class for a broker.
    """

    def __init__(self, host: str, port: Optional[str]) -> None:
        self.host = host
        self.port = port
