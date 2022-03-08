from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from parsers.models.schema_definitions import ChallengeReceiptParsed


class ChallengeReceiptParser:
    def __init__(self, transaction: dict):
        self.transaction = transaction

    def insert(self, session: Session):
        parsed_receipts = []
        for witness in self.transaction["path"][0]["witnesses"]:
            parsed_receipts.append(ChallengeReceiptParsed(
                block=self.transaction["block"],
                hash=self.transaction["hash"],
                tx_power=self.transaction["path"][0]["receipt"]["tx_power"] if self.transaction["path"][0]["receipt"] else None,
                challenger_address=self.transaction["challenger"],
                transmitter_address=self.transaction["path"][0]["receipt"]["gateway"] if self.transaction["path"][0]["receipt"] else None,
                origin=self.transaction["path"][0]["receipt"]["origin"] if self.transaction["path"][0]["receipt"] else None,
                witness_address=witness["gateway"],
                witness_is_valid=witness["is_valid"],
                witness_invalid_reason=witness["invalid_reason"] if "invalid_reason" in witness.keys() else None,
                witness_signal=witness["signal"],
                witness_snr=witness["snr"],
                witness_channel=witness["channel"],
                witness_datarate=witness["datarate"],
                witness_frequency=witness["frequency"],
                witness_timestamp=witness["timestamp"]
            ))
        try:
            session.add_all(parsed_receipts)
            session.commit()
        except IntegrityError:
            session.rollback()
            pass