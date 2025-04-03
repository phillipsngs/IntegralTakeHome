import uuid

from models.Account import Account
from clients.EtherScanClient import EtherScanClient
import datetime

from models.Transaction import Transaction

API_KEY = "3Q1P7BPPI2NZ8B62GX2I3ZZ2MADS2CIHN2"
URL = "https://api.etherscan.io/api?"


class TransactionService:
    def __init__(self, offset):
        self.client = EtherScanClient(
            base_url=URL,
            api_key=API_KEY,
            offset=offset
        )

    def get_transactions(self, account: Account):
        txns = []
        account_address = account.get_address()
        account_id = account.get_id()

        internal_txns_payload = self.client.get_internal_transactions(address=account_address)
        normal_txns_payload = self.client.get_normal_transactions(address=account_address)
        erc20_txns_payload = self.client.get_erc20_transactions(address=account_address)

        if internal_txns_payload["status"] == "1":
            txns += [self.process_internal_txn(account_id, account_address, x) for x in internal_txns_payload["result"]]

        if normal_txns_payload["status"] == "1":
            txns += [self.process_normal_txn(account_id, account_address, x) for x in normal_txns_payload["result"]]

        if erc20_txns_payload["status"] == "1":
            txns += [self.process_erc20_txn(account_id, account_address, x) for x in erc20_txns_payload["result"]]

        return txns

    def determine_txn_type(self, account_address, txn: dict):
        if txn.get("to", "") == account_address:
            return "deposit"
        elif txn.get("from", "") == account_address:
            return "withdraw"
        else:
            return "invalid"

    def process_normal_txn(self, account_id, account_address, txn: dict):
        txn_type = self.determine_txn_type(account_address, txn)
        formatted_timestamp = datetime.datetime.fromtimestamp(int(txn['timeStamp'])).strftime(
            '%Y-%m-%dT%H:%M:%SZ')

        return Transaction(
            id_=uuid.uuid4(),
            accountId=account_id,
            toAddress=txn['to'],
            fromAddress=txn['from'],
            type_=txn_type,
            amount=int(txn['value']) / 10**18,
            symbol="ETH",
            decimal=18,
            timestamp=formatted_timestamp,
            txnHash=txn['hash']
        )

    def process_internal_txn(self, account_id, account_address, txn: dict):
        txn_type = self.determine_txn_type(account_address, txn)
        formatted_timestamp = datetime.datetime.fromtimestamp(int(txn['timeStamp'])).strftime(
            '%Y-%m-%dT%H:%M:%SZ')

        return Transaction(
            id_=uuid.uuid4(),
            accountId=account_id,
            toAddress=txn['to'],
            fromAddress=txn['from'],
            type_=txn_type,
            amount=int(txn['value']) / 10**18,
            symbol="ETH",
            decimal=18,
            timestamp=formatted_timestamp,
            txnHash=txn['hash']
        )

    def process_erc20_txn(self, account_id, account_address, txn: dict):
        txn_type = self.determine_txn_type(account_address, txn)
        formatted_timestamp = datetime.datetime.fromtimestamp(int(txn['timeStamp'])).strftime(
            '%Y-%m-%dT%H:%M:%SZ')

        return Transaction(
            id_=uuid.uuid4(),
            accountId=account_id,
            toAddress=txn['to'],
            fromAddress=txn['from'],
            type_=txn_type,
            amount=int(txn['value']) / 10**int(txn['tokenDecimal']),
            symbol=txn['tokenSymbol'],
            decimal=txn['tokenDecimal'],
            timestamp=formatted_timestamp,
            txnHash=txn['hash']
        )
