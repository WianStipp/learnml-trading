"""Contains the base Broker class"""

import abc

class Broker(abc.ABC):
    """Abstracted represenation of a broker."""
    def __init__(self, host: str) -> None:
        super().__init__()
        self.host = host
    