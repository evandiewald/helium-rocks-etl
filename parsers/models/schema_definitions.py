import enum
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text, Float, Boolean, BigInteger, Enum, JSON


Base = declarative_base()


class transaction_type(enum.Enum):
    coinbase_v1 = 1
    security_coinbase_v1 = 2
    oui_v1 = 3
    gen_gateway_v1 = 4
    routing_v1 = 5
    payment_v1 = 6
    security_exchange_v1 = 7
    consensus_group_v1 = 8
    add_gateway_v1 = 9
    assert_location_v1 = 10
    create_htlc_v1 = 11
    redeem_htlc_v1 = 12
    poc_request_v1 = 13
    poc_receipts_v1 = 14
    vars_v1 = 14
    rewards_v1 = 16
    token_burn_v1 = 17
    dc_coinbase_v1 = 18
    token_burn_exchange_rate_v1 = 19
    payment_v2 = 20
    state_channel_open_v1 = 21
    state_channel_close_v1 = 22
    price_oracle_v1 = 23
    transfer_hotspot_v1 = 24
    rewards_v2 = 25
    assert_location_v2 = 26
    gen_validator_v1 = 27
    stake_validator_v1 = 28
    unstake_validator_v1 = 29
    validator_heartbeat_v1 = 30
    transfer_validator_stake_v1 = 31
    gen_price_oracle_v1 = 32
    consensus_group_failure_v1 = 33
    transfer_hotspot_v2 = 34


class FollowerInfo(Base):
    __tablename__ = "follower_info"

    name = Column(Text, primary_key=True)
    value = Column(Integer)


class Transactions(Base):
    __tablename__ = "transactions"

    block = Column(BigInteger)
    hash = Column(Text, primary_key=True)
    type = Column(Enum(transaction_type))
    fields = Column(JSON)


class ChallengeReceiptParsed(Base):
    __tablename__ = "challenge_receipts_parsed"

    block = Column(BigInteger)
    hash = Column(Text, primary_key=True)
    tx_power = Column(Integer)
    challenger_address = Column(Text)
    transmitter_address = Column(Text)
    origin = Column(Text)
    witness_address = Column(Text, primary_key=True)
    witness_is_valid = Column(Boolean)
    witness_invalid_reason = Column(Text)
    witness_signal = Column(Integer)
    witness_snr = Column(Float)
    witness_channel = Column(Integer)
    witness_datarate = Column(Text)
    witness_frequency = Column(Float)
    witness_timestamp = Column(BigInteger)


class PaymentsParsed(Base):
    __tablename__ = "payments_parsed"

    block = Column(BigInteger)
    hash = Column(Text, primary_key=True)
    fee = Column(BigInteger)
    type = Column(Enum(transaction_type))
    payer = Column(Text)
    payee = Column(Text, primary_key=True)
    amount = Column(BigInteger)