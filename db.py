from rocksdict import Rdict, Options, AccessType
# from python_pb import blockchain_block_pb2
from pathlib import Path
from typing import List, Union, Tuple, Mapping, Optional
from serialization_utils import *


# class BlockchainBlockV1:
#     def __init__(self, block_pb: blockchain_block_pb2.blockchain_block):
#         self.height = block_pb.v1.height
#         self.election_epoch = block_pb.v1.election_epoch
#         self.epoch_start = block_pb.v1.epoch_start
#         self.prev_hash = deserialize_hash(block_pb.v1.prev_hash)
#         self.block_hash = "" # SHA256 + B64 encode?
#         self.time = block_pb.v1.time
#         self.transaction_count = len(block_pb.v1.transactions)
#         self.block_pb = block_pb
#
#     def to_dict(self):
#         return vars(self)


class RocksDB:
    def __init__(self, rocks_path: Path, db_name: str, options: Options, secondary: bool = True):
        self.path = rocks_path / db_name
        self.column_families = Rdict.list_cf(str(self.path))
        cf_dict = {cf: Options(raw_mode=True) for cf in self.column_families}
        if secondary:
            secondary_path = rocks_path / "secondary"
            self.db: Rdict = Rdict(str(self.path), options=options, column_families=cf_dict, access_type=AccessType.secondary(str(secondary_path)))
        else:
            self.db: Rdict = Rdict(str(self.path), options=options, column_families=cf_dict)

    def close(self):
        try:
            self.db.close()
        except Exception: # db is already closed
            pass


# class BlockchainDBReader(RocksDB):
#     """Read directly from blockchain.db files and deserialize protobufs. No longer used in favor of direct transaction JSON."""
#     def __init__(self, rocks_path: Path, db_name="blockchain.db", options=Options(raw_mode=True)):
#         super().__init__(rocks_path, db_name, options)
#
#     def heights_cf(self) -> Rdict:
#         return self.db.get_column_family("heights")
#
#     def available_blocks(self) -> List[int]:
#         return [bytes_to_bigint(key) for key in self.heights_cf().keys()]
#
#     def first_block(self) -> int:
#         """Gets first non-genesis block"""
#         cf_iter = self.heights_cf().iter()
#         cf_iter.seek_to_first()
#         cf_iter.next()
#         return bytes_to_bigint(cf_iter.key())
#
#     def current_height(self) -> int:
#         cf_iter = self.heights_cf().iter()
#         cf_iter.seek_to_last()
#         return bytes_to_bigint(cf_iter.key(), "little")
#
#     def get_block(self, height: int) -> blockchain_block_pb2.blockchain_block:
#         block_bytes = self.heights_cf()[int_to_bytes(height)]
#         block = blockchain_block_pb2.blockchain_block()
#         return BlockchainBlockV1(block.ParseFromString(block_bytes))


class TransactionsDBReader(RocksDB):
    def __init__(self, rocks_path: Path, db_name="transactions.db", options=Options(raw_mode=True)):
        super().__init__(rocks_path, db_name, options)

    def json_cf(self) -> Rdict:
        return self.db.get_column_family("json")

    def transaction_keys(self) -> List[bytes]:
        return [key for key in self.json_cf().keys()]

    def get_transaction(self, key: bytes):
        return self.json_cf()[key]

    def heights_cf(self) -> Rdict:
        return self.db.get_column_family("heights")

    def heights_keys(self) -> List[bytes]:
        return [k for k in self.heights_cf().keys()]

    def heights_values_as_bigint(self) -> List[int]:
        return [bytes_to_bigint(v, "little") for v in self.heights_cf().values()]

    def first_block(self) -> int:
        try:
            return sorted(set(self.heights_values_as_bigint()))[1]
        except IndexError:
            raise Exception("No blocks found. Is the node running and syncing?")

    def current_height(self) -> int:
        return max(self.heights_values_as_bigint())

    def transaction_keys_by_block(self, txns_by_block, start_height=Optional[int], end_height=Optional[int]):
        """We have to reverse-index the heights column family in order to get transaction keys by block."""
        heights_keys, heights_values = self.heights_keys(), self.heights_values_as_bigint()
        if (start_height is int) and (end_height is int) and txns_by_block:
            update_blocks = range(start_height, end_height)
        else:
            txns_by_block = {}
            update_blocks = set(heights_values)
        for block in update_blocks:
            txns_by_block[block] = [heights_keys[i] for i in range(len(heights_values)) if heights_values[i] == block]
        return txns_by_block

