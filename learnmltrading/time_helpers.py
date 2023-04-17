"""Helpers for dealing with price timing."""

import datetime
from pydantic import BaseModel


class Timeframe(BaseModel):
    """Represents a time window"""

    start_unix: int
    end_unix: int

    @classmethod
    def from_isoformat(cls, start_iso: str, end_iso: str) -> "Timeframe":
        """Initialize from ISO format dates."""
        return cls(
            start_unix=iso_to_unix(start_iso),
            end_unix=iso_to_unix(end_iso),
        )


def iso_to_unix(isoformat_date: str) -> int:
    """Convert isoformat_date <YYYY>-<MM>-<DD>T<HH>:<mm>:<ss> e.g. 2023-04-02T10:30:00
    into Unix format."""
    return int(datetime.datetime.fromisoformat(isoformat_date).timestamp())
