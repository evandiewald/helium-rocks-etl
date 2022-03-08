from typing import Literal
import base64
import base58


def bytes_to_bigint(input_bytes: bytes, byteorder: Literal["big", "little"] = "big") -> int:
    return int.from_bytes(input_bytes, byteorder=byteorder)


def int_to_bytes(input_int: int, length: int = 8, byteorder: Literal["big", "little"] = "big") -> bytes:
    return int(input_int).to_bytes(length=length, byteorder=byteorder)


def deserialize_hash(input_bytes: bytes) -> str:
    # remove last byte
    return base64.urlsafe_b64encode(input_bytes)[:-1].decode("utf-8")


def serialize_hash(input_str: str) -> bytes:
    # append = to end
    return base64.urlsafe_b64decode(str(input_str+"=").encode("utf-8"))


def deserialize_address(input_bytes: bytes) -> str:
    # append \x00 byte to indicate mainnet address
    buffer = b'\x00' + input_bytes
    return base58.b58encode_check(buffer).decode("utf-8")