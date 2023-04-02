"""Models for the broker accounts"""

from pydantic import BaseModel

class OANDAAccount(BaseModel):
    """Data model for the OANDA account details."""
    account_number: str
    api_token: str
