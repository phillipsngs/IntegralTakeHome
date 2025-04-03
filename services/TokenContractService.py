from models.Account import Account
from clients.EtherScanClient import EtherScanClient
import uuid

API_KEY = "3Q1P7BPPI2NZ8B62GX2I3ZZ2MADS2CIHN2"
URL = "https://api.etherscan.io/api?"


class TokenContractService:
    STETH_CONTRACT_ADDRESS = "0xae7ab96520de3a18e5e111b5eaab095312d7fe84"
    TOTAL_SHARES_DATA = "0xd5002f2e"
    TOTAL_POOLED_DATA = "0x37cfdaca"

    def __init__(self):
        self.client = EtherScanClient(URL, API_KEY, 5)

    def get_total_shares(self):
        total_shares_payload = self.client.get_total_shares(contract_address=self.STETH_CONTRACT_ADDRESS,
                                                            data=self.TOTAL_SHARES_DATA)
        return total_shares_payload["result"]

    def get_total_pooled_eth(self):
        total_supply_payload = self.client.get_total_pooled_eth(contract_address=self.STETH_CONTRACT_ADDRESS,
                                                                data=self.TOTAL_POOLED_DATA)
        return total_supply_payload["result"]
