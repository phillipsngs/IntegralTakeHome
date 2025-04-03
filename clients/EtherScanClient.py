import requests


class EtherScanClient:
    def __init__(self, base_url, api_key):
        self.url = base_url
        self.api_key = api_key

    def get(self, module, **kwargs):
        transactions = requests.get(
            url=f"{self.url}module={module}",
            params=kwargs)
        return transactions.json()

    def get_recent_deposit_addresses(self, contract_address):
        pass
