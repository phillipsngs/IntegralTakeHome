class Account:
    id: str
    address: str

    def __init__(self, id_: str, address: str):
        self.id = id_
        self.address = address

    def get_id(self):
        return self.id

    def get_address(self):
        return self.address
