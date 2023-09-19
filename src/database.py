from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv, dotenv_values
from pathlib import Path
import os


env_file = Path('.env')

if env_file.exists() and not os.getenv('USE_COMPOSE_DB'):
      env = load_dotenv(env_file)


env = os.environ

url = f'{env["DB"]}+{env["DB_DRIVER"]}://{env["MYSQL_USER"]}:' \
      f'{env["MYSQL_PASSWORD"]}@{env["MYSQL_HOST"]}:{env["MYSQL_PORT"]}' \
      f'/{env["MYSQL_DB"]}'

print(url)

engine = create_engine(url)

SessionLocal = sessionmaker(engine)

Base = declarative_base()
