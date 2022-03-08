from rocksdict import Rdict, Options, AccessType
from python_pb import blockchain_block_v1_pb2
from python_pb import blockchain_txn_pb2
from python_pb import blockchain_block_pb2
from google.protobuf.json_format import MessageToDict
from python_pb import entry_v1_pb2
import base58
import json

path = str("C:/Users/evand/node_data/transactions.db")

opt = Options(raw_mode=True)
opt.set_error_if_exists(False)
# create a Rdict with default options at `path`
db = Rdict(path, options=opt, access_type=AccessType.secondary("C:/Users/evand/node_data/secondary"), column_families={"heights": Options(raw_mode=True),
                                                                  "transactions": Options(raw_mode=True),
                                                                  "json": Options(raw_mode=True)})

heights_cf = db.get_column_family("heights")
transactions_cf = db.get_column_family("transactions")
json_cf = db.get_column_family("json")
json_keys = [k for k in json_cf.keys()]

transactions = []
txn_keys = [key for key in transactions_cf.keys()]
for i, txn_key in enumerate(txn_keys[:1000]):
    txn_bytes = transactions_cf[txn_key]
    txn = blockchain_txn_pb2.blockchain_txn()
    txn.ParseFromString(txn_bytes)
    # have to change addresses to b58 strings with
    # append \x00 leading byte then base58.b58encode_check
    transactions.append(txn)

db.close()


path = str("C:/Users/evand/node_data/blockchain.db")

# create a Rdict with default options at `path`
db = Rdict(path, options=Options(raw_mode=True), access_type=AccessType.secondary("C:/Users/evand/node_data/secondary"),
           column_families={"temp_blocks": Options(raw_mode=True),
                                                                  "heights": Options(raw_mode=True),
                                                                  "blocks": Options(raw_mode=True),
                                                                  "plausible_blocks": Options(raw_mode=True),
                                                                  "snapshots": Options(raw_mode=True),
                                                                  "implicit_burns": Options(raw_mode=True),
                                                                  "info": Options(raw_mode=True),
                                                                  "htlc_receipts": Options(raw_mode=True)})

blocks_cf = db.get_column_family("blocks")

blocks = []
block_keys = [key for key in blocks_cf.keys()]
for i, block_key in enumerate(block_keys[:1000]):
    block_bytes = blocks_cf[block_key]
    # block = blockchain_block_v1_pb2.blockchain_block_v1()
    block = blockchain_block_pb2.blockchain_block()
    block.ParseFromString(block_bytes)
    # have to change addresses to b58 strings with
    # append \x00 leading byte then base58.b58encode_check
    blocks.append(block)

heights_cf = db.get_column_family("heights")

heights = []
height_keys = [key for key in heights_cf.keys()]
# for i, height_key in enumerate(height_keys[:1000]):
#     height_bytes = heights_cf[height_key]
#     # block = blockchain_block_v1_pb2.blockchain_block_v1()
#     height = blockchain_block_pb2.blockchain_block()
#     height.ParseFromString(height_bytes)
#     # have to change addresses to b58 strings with
#     # append \x00 leading byte then base58.b58encode_check
#     heights.append(height)
#
# db.close()

path = str("C:/Users/evand/node_data/balances.db")

# create a Rdict with default options at `path`
db = Rdict(path, options=Options(raw_mode=True), column_families={"entries": Options(raw_mode=True)})
entries_cf = db.get_column_family("entries")
entries_keys = [key for key in entries_cf.keys()]

entry_v1 = entry_v1_pb2.entry_v1()
entry_bytes = entries_cf[entries_keys[0]]
entry_v1.ParseFromString(entry_bytes)


path = str("C:/Users/evand/node_data/ledger.db")

cf_dict = {cf: Options(raw_mode=True) for cf in Rdict.list_cf(path)}
# create a Rdict with default options at `path`
db = Rdict(path, options=Options(raw_mode=True), access_type=AccessType.secondary("C:/Users/evand/node_data/secondary"), column_families=cf_dict)
