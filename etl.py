from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.engine import Engine
import os
import argparse
from parsers.models.schema_definitions import Base
from follower import Follower
from config import Config


load_dotenv()

rocks_path = Path(os.getenv("ROCKS_PATH"))

engine = create_engine(os.getenv("POSTGRES_URL"))

config = Config()


def migrate(base: DeclarativeMeta, engine: Engine):
    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)


def start(engine: Engine, config: Config):
    follower = Follower(engine, config)
    follower.run()


parser = argparse.ArgumentParser()
parser.add_argument("command",
                    action="store",
                    choices=["migrate", "start"])

args = parser.parse_args()

match args.command:
    case "migrate":
        migrate(Base, engine)
    case "start":
        start(engine, config)