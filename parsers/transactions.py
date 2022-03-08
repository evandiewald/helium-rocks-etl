from parsers.models.schema_definitions import Transactions
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


class TransactionParser:
    def __init__(self, transaction: dict):
        self.transaction = transaction

    def insert(self, session: Session, with_fields: bool = True):
        try:
            session.add(Transactions(
                block=self.transaction["block"],
                hash=self.transaction["hash"],
                type=self.transaction["type"],
                fields=self.transaction if with_fields else None
            ))
            session.commit()
        except IntegrityError:
            session.rollback()
            pass

