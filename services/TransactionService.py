import uuid
from typing import List

from models.Account import Account
from clients.EtherScanClient import EtherScanClient
import datetime

from models.Transaction import Transaction

API_KEY = "3Q1P7BPPI2NZ8B62GX2I3ZZ2MADS2CIHN2"
URL = "https://api.etherscan.io/api?"


class TransactionService:
    def __init__(self, offset):
        self.offset = offset
        self.client = EtherScanClient(
            base_url=URL,
            api_key=API_KEY,
        )

    def _get_normal_transactions(self, account: Account, page=1) -> List[Transaction]:
        account_address = account.get_address()
        account_id = account.get_id()

        transactions = self.client.get(
            module="account",
            action="txlist",
            address=account_address,
            startblock=0,
            endblock=99999999,
            page=page,
            offset=self.offset,
            sort="asc",
            apikey=API_KEY
        )

        if transactions["status"] == "0":
            return []

        return [self.process_txn(account, x) for x in transactions["result"]]

    def _get_internal_transactions(self, account: Account, page=1) -> List[Transaction]:
        transactions = self.client.get(
            module="account",
            action="txlistinternal",
            address=account.get_address(),
            startblock=0,
            endblock=99999999,
            page=page,
            offset=self.offset,
            sort="asc",
            apikey=API_KEY
        )

        if transactions["status"] == "0":
            return []

        return [self.process_txn(account, x) for x in transactions["result"]]

    def _get_erc20_transactions_from_address(self, account: Account, page=1) -> List[Transaction]:
        transactions = self.client.get(
            module="account",
            action="tokentx",
            address=account.get_address(),
            startblock=0,
            endblock=99999999,
            page=page,
            offset=self.offset,
            sort="asc",
            apikey=API_KEY
        )
        if transactions["status"] == "0":
            return []

        return [self.process_erc20_txn(account, x) for x in transactions["result"]]

    def _get_erc20_transactions_to_address(self, account: Account, page=1) -> List[Transaction]:
        transactions = self.client.get(
            module="account",
            action="tokentx",
            contractaddress=account.get_address(),
            startblock=0,
            endblock=99999999,
            page=page,
            offset=self.offset,
            sort="asc",
            apikey=API_KEY
        )

        if transactions["status"] == "0":
            return []

        return [self.process_erc20_txn(account, x) for x in transactions["result"]]

    def determine_txn_type(self, account_address, txn: dict):
        if txn.get("to", "") == account_address:
            return "deposit"
        elif txn.get("from", "") == account_address:
            return "withdraw"
        else:
            return "invalid"

    def process_txn(self, account: Account, txn: dict):
        txn_type = self.determine_txn_type(account.get_address(), txn)
        formatted_timestamp = datetime.datetime.fromtimestamp(int(txn['timeStamp'])).strftime(
            '%Y-%m-%dT%H:%M:%SZ')

        return Transaction(
            id_=uuid.uuid4(),
            accountId=account.get_id(),
            toAddress=txn['to'],
            fromAddress=txn['from'],
            type_=txn_type,
            amount=int(txn['value']) / 10 ** 18,
            symbol="ETH",
            decimal=18,
            timestamp=formatted_timestamp,
            txnHash=txn['hash']
        )

    def process_erc20_txn(self, account: Account, txn: dict):
        txn_type = self.determine_txn_type(account.get_address(), txn)
        formatted_timestamp = datetime.datetime.fromtimestamp(int(txn['timeStamp'])).strftime(
            '%Y-%m-%dT%H:%M:%SZ')

        return Transaction(
            id_=uuid.uuid4(),
            accountId=account.get_id(),
            toAddress=txn['to'],
            fromAddress=txn['from'],
            type_=txn_type,
            amount=int(txn['value']) / 10 ** int(txn['tokenDecimal']),
            symbol=txn['tokenSymbol'],
            decimal=int(txn['tokenDecimal']),
            timestamp=formatted_timestamp,
            txnHash=txn['hash']
        )

    def get_transactions(self, account: Account):
        internal_txns_payload = self._get_internal_transactions(account)
        normal_txns_payload = self._get_normal_transactions(account)
        erc20_to_txns_payload = self._get_erc20_transactions_to_address(account)
        erc20_from_txns_payload = self._get_erc20_transactions_from_address(account)
        return internal_txns_payload + normal_txns_payload + erc20_to_txns_payload + erc20_from_txns_payload
