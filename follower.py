import json
from serialization_utils import serialize_hash, deserialize_hash
import sqlalchemy.exc
from sqlalchemy.engine import Engine
from db import TransactionsDBReader
from typing import Literal
import os
from pathlib import Path
from parsers.models.schema_definitions import FollowerInfo
from parsers.challenge_receipts import ChallengeReceiptParser
from parsers.payments import PaymentParser
from parsers.transactions import TransactionParser
from sqlalchemy.orm import sessionmaker
import time
from config import Config


class Follower:
    def __init__(self, engine: Engine, config: Config):
        self.rocks_path = Path(os.getenv("ROCKS_PATH"))
        self.engine = engine
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.transactions = TransactionsDBReader(rocks_path=self.rocks_path)
        self.current_height = self.transactions.current_height()
        self.first_block = self.transactions.first_block()
        self.sync_height = self.load_sync_height()
        self.transactions_by_block = self.transactions.transaction_keys_by_block()
        self.config = config

    def load_sync_height(self):
        try:
            sync_height = self.session.query(FollowerInfo.value).filter(FollowerInfo.name == "sync_height").one()[0]
        except sqlalchemy.exc.NoResultFound:
            sync_height = self.first_block
            self.session.add(FollowerInfo(name="sync_height", value=self.first_block))
            self.session.commit()
        return sync_height

    def update_sync_height(self, new_sync_height: int):
        self.session.query(FollowerInfo).filter(FollowerInfo.name == "sync_height")\
            .update({"value": new_sync_height}, synchronize_session="fetch")
        self.sync_height = new_sync_height

    def process_transaction(self, transaction: dict):
        if (self.config.transactions_config.mode == "full") or (transaction["type"] in self.config.transactions_config.include_types):
            TransactionParser(transaction).insert(self.session, self.config.transactions_config.with_fields)
        if transaction["type"] == "poc_receipts_v1":
            if "challenge_receipts" in self.config.parsers:
                ChallengeReceiptParser(transaction).insert(self.session)
        elif transaction["type"] in ["payment_v1", "payment_v2"]:
            if "payments" in self.config.parsers:
                PaymentParser(transaction).insert(self.session)
        elif transaction["type"] == "add_gateway_v1":
            print(transaction)
        elif transaction["type"] in ["assert_location_v1", "assert_location_v2"]:
            print(transaction)

    def load_block(self, height: int):
        for txn_key in self.transactions_by_block[height]:
            transaction = json.loads(self.transactions.json_cf()[txn_key].decode())
            self.process_transaction(transaction)

    def update_databases(self):
        self.transactions.db.try_catch_up_with_primary()
        new_height = self.transactions.current_height()
        self.transactions_by_block = self.transactions.transaction_keys_by_block(self.transactions_by_block, self.current_height, new_height+1)
        self.current_height = new_height

    def run(self):
        print(f"Starting sync from blocks {self.sync_height} to {self.current_height}")
        while True:
            try:
                if self.sync_height <= self.current_height:
                    print(f"Loading transactions in block: {self.sync_height}")
                    self.load_block(self.sync_height)
                    self.update_sync_height(self.sync_height + 1)
                else:
                    print(f"Fully synced. Searching for new blocks...")
                    time.sleep(10)
                    self.update_databases()
            except KeyboardInterrupt:
                # close somewhat gracefully
                print("Closing database connection.")
                try:
                    self.transactions.db.close()
                except Exception:
                    # not implemented for secondary
                    pass







