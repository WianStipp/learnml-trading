"""Contains the OANDA Broker class"""

from learnmltrading.broker import base_broker
from learnmltrading.broker import broker_account

OANDA_LIVE_HOST = "https://api-fxtrade.oanda.com"
OANDA_DEMO_HOST = "https://api-fxpractice.oanda.com"

class OANDABroker(base_broker.Broker):
    """Global FX broker: https://www.oanda.com/"""
    def __init__(self, host: str, account: broker_account.OANDAAccount) -> None:
        super().__init__(host=host)
        self.account = account

if __name__ == "__main__":
    import os
    account = broker_account.OANDAAccount(account_number=os.environ.get("OANDA_ACCOUNT_NUMBER"), \
                                        api_token=os.environ.get("OANDA_API_TOKEN"))
    broker = OANDABroker(OANDA_LIVE_HOST, account)
    print(broker)
