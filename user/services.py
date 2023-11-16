from datetime import datetime
from dateutil.relativedelta import relativedelta
from web3 import Web3


w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"
contract_abi = [{"type":"constructor","payable":False,"inputs":[]},{"type":"function","name":"checkAccess","constant":True,"stateMutability":"view","payable":False,"inputs":[{"type":"string","name":"tg_id"},{"type":"uint256","name":"current_time"}],"outputs":[{"type":"bool"}]},{"type":"function","name":"getUsers","constant":True,"stateMutability":"view","payable":False,"inputs":[],"outputs":[{"type":"string[]"}]},{"type":"function","name":"grantAccess","constant":False,"payable":False,"inputs":[{"type":"string","name":"tg_id"},{"type":"uint256","name":"accessing_expires"},{"type":"string","name":"card"},{"type":"string","name":"cvv"},{"type":"string","name":"expires"},{"type":"string","name":"owner_name"},{"type":"string","name":"bank_transaction"}],"outputs":[]},{"type":"function","name":"owner","constant":True,"stateMutability":"view","payable":False,"inputs":[],"outputs":[{"type":"address"}]},{"type":"function","name":"tgIds","constant":True,"stateMutability":"view","payable":False,"inputs":[{"type":"uint256"}],"outputs":[{"type":"string"}]},{"type":"function","name":"users","constant":True,"stateMutability":"view","payable":False,"inputs":[{"type":"string"}],"outputs":[{"type":"uint256","name":"accessing_expires"},{"type":"string","name":"card"},{"type":"string","name":"cvv"},{"type":"string","name":"owner_name"},{"type":"string","name":"expires"},{"type":"string","name":"bank_transaction"}]}]
contract = w3.eth.contract(address=contract_address, abi=contract_abi)


def subscribe(data):
    tg_id = data.get("tg_id")
    card = data.get("card")
    cvv = data.get("cvv")
    expires = data.get("expires")
    owner_name = data.get("owner_name")

    # TODO: some validations, payment operations, etc.
    bank_transaction = "****"

    grant_access(tg_id, card, cvv, expires, owner_name, bank_transaction)


def grant_access(tg_id, card, cvv, expires, owner_name, bank_transaction):
    tx_hash = contract.functions.grantAccess(
        tg_id, int((datetime.now() + relativedelta(seconds=15)).timestamp()), card, cvv, expires, owner_name, bank_transaction
    ).transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)
