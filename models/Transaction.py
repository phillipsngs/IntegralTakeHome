class Transaction:
    id: str
    accountId: str
    toAddress: str
    fromAddress: str
    type: str
    amount: float
    symbol: str
    decimal: int
    timestamp: str
    txnHash: str

    def __init__(self, id_, accountId, toAddress, fromAddress, type_, amount, symbol, decimal, timestamp, txnHash):
        self.id = id_
        self.accountId = accountId
        self.toAddress = toAddress
        self.fromAddress = fromAddress
        self.type = type_
        self.amount = amount
        self.symbol = symbol
        self.decimal = decimal
        self.timestamp = timestamp
        self.txnHash = txnHash

