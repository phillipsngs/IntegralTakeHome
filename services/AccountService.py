from models.Account import Account


class AccountService:
    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):
        accounts = [
            Account(id_=str(1), address="0x2c1ba59d6f58433fb1eaee7d20b26ed83bda51a3"),
            Account(id_=str(2), address="0x20d42f2e99a421147acf198d775395cac2e8b03d"),
            Account(id_=str(3), address="0x881b0a4e9c55d08e31d8d3c022144d75a454211c"),
            Account(id_=str(4), address="0x642ae78fafbb8032da552d619ad43f1d81e4dd7c"),
            Account(id_=str(5), address="0x4e83362442b8d1bec281594cea3050c8eb01311c"),
        ]
        return accounts

    def get_account(self, account_id):
        for account in self.accounts:
            if account.get_id() == account_id:
                return account
        return None
