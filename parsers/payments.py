from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from parsers.models.schema_definitions import PaymentsParsed
from parsers.models.schema_definitions import transaction_type


class PaymentParser:
    def __init__(self, transaction: dict):
        self.transaction = transaction

    def insert(self, session: Session):
        if self.transaction["type"] == "payment_v1":
            parsed_payment = PaymentsParsed(
                block=self.transaction["block"],
                hash=self.transaction["hash"],
                fee=self.transaction["fee"],
                type=transaction_type.payment_v1,
                payer=self.transaction["payer"],
                payee=self.transaction["payee"],
                amount=self.transaction["amount"]
            )
            try:
                session.add(parsed_payment)
                session.commit()
            except IntegrityError:
                session.rollback()
                pass
        elif self.transaction["type"] == "payment_v2":
            parsed_payments = []
            for payment in self.transaction["payments"]:
                parsed_payments.append(PaymentsParsed(
                    block=self.transaction["block"],
                    hash=self.transaction["hash"],
                    fee=self.transaction["fee"],
                    type=transaction_type.payment_v2,
                    payer=self.transaction["payer"],
                    payee=payment["payee"],
                    amount=payment["amount"]
                ))
            try:
                session.add_all(parsed_payments)
                session.commit()
            except IntegrityError:
                session.rollback()
                pass