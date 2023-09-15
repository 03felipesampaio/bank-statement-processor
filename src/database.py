from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv, dotenv_values
from pathlib import Path
import os


env_file = Path('.env')

if env_file.exists():
      env = load_dotenv(env_file)


env = os.environ

url = f'{env["DB"]}+{env["DB_DRIVER"]}://{env["DB_USER"]}:' \
      f'{env["DB_PWD"]}@{env["DB_HOST"]}:{env["DB_PORT"]}' \
      f'/{env["DB_DEFAULT"]}'

engine = create_engine(url)

SessionLocal = sessionmaker(engine)

Base = declarative_base()
