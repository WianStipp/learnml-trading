"""Contains the base Broker class"""

import abc
from pydantic import BaseModel


class Broker(abc.ABC):
    """Abstracted represenation of a broker."""

    def __init__(self, host: str) -> None:
        super().__init__()
        self.host = host
    

class MarketOrder(BaseModel):
    """An order to buy or sell an instrument at the market
    price with a given quantity."""
    instrument: str
    quantity: int
    buy: bool

class Position(BaseModel):
    position_id: str
    ...