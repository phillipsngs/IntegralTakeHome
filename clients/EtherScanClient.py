import requests
import json


class EtherScanClient:
    def __init__(self, base_url, api_key, offset):
        self.url = base_url
        self.api_key = api_key
        self.offset = offset

    def get(self, module, **kwargs):
        transactions = requests.get(
            url=f"{self.url}module={module}",
            params=kwargs)
        return transactions.json()

    def get_normal_transactions(self, address):
        normal_transactions = self.get(
            module="account",
            action="txlist",
            address=address,
            startblock=0,
            endblock=99999999,
            page=1,
            offset=self.offset,
            sort="asc",
            apikey=self.api_key
        )
        return normal_transactions

    def get_internal_transactions(self, address):
        internal_transactions = self.get(
            module="account",
            action="txlistinternal",
            address=address,
            startblock=0,
            endblock=99999999,
            page=1,
            offset=self.offset,
            sort="asc",
            apikey=self.api_key
        )
        return internal_transactions

    def get_erc20_transactions(self, address):
        erc20_tokens_transactions = self.get(
            module="account",
            action="tokentx",
            address=address,
            contractaddress="0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2",
            startblock=0,
            endblock=99999999,
            page=1,
            offset=self.offset,
            sort="asc",
            apikey=self.api_key
        )
        return erc20_tokens_transactions

    def get_total_shares(self, contract_address, data):
        total_shares = self.get(
            module="proxy",
            action="eth_call",
            to=contract_address,
            data=data,
            tag="latest",
            apikey=self.api_key
        )
        return total_shares

    def get_total_pooled_eth(self, contract_address, data):
        total_pooled = self.get(
            module="proxy",
            action="eth_call",
            to=contract_address,
            data=data,
            tag="latest",
            apikey=self.api_key
        )
        return total_pooled

    def get_recent_deposit_addresses(self, contract_address):
        pass
