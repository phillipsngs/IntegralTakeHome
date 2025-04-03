from fastapi import FastAPI
import requests

from services.TransactionService import TransactionService
from services.AccountService import AccountService
from services.TokenContractService import TokenContractService

app = FastAPI()


@app.get("/")
async def root():
    return {
        "data": "Hello World"
    }


@app.get("/accounts/{accountId}/transactions")
async def get_transactions(accountId: str):
    account_service = AccountService()
    transaction_service = TransactionService(5)

    account = account_service.get_account(accountId)
    transactions = []

    if account:
        transactions = transaction_service.get_transactions(account)

    return {
        "data": transactions,
        "count": len(transactions)
    }


@app.get("/contracts/steth/total_pooled_eth")
async def get_total_pooled_eth():
    total_pooled_eth = TokenContractService().get_total_pooled_eth()
    return {
        "data": total_pooled_eth
    }


@app.get("/contracts/steth/total_shares")
async def get_total_shares():
    total_shares = TokenContractService().get_total_shares()
    return {
        "data": total_shares
    }


@app.get("/contracts/steth/recent_depositors")
async def get_recent_steth_depositors():
    return {
        "temp": 1
    }
