import yaml
from typing import Union, Literal, List, Optional
from pathlib import Path
from pydantic import BaseModel


class TransactionsConfig(BaseModel):
    mode: Literal["full", "filtered"]
    include_types: Optional[List[str]]
    with_fields: bool


class Config:
    def __init__(self, config_path: Union[str, Path] = "config/config.yaml"):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        self.transactions_config = TransactionsConfig(**config["transactions"])
        self.parsers = config["parsers"]