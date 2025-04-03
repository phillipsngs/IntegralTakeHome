from models.Transaction import Transaction


class Erc20Transaction(Transaction):
    def __init__(self, id_, accountId, toAddress, fromAddress, type_, amount, symbol, decimal, timestamp, txnHash):
        super().__init__(
            id_=id_,
            accountId=accountId,
            toAddress=toAddress,
            fromAddress=fromAddress,
            type_=type_,
            amount=amount,
            symbol=symbol,
            decimal=decimal,
            timestamp=timestamp,
            txnHash=txnHash
        )