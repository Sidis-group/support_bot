from environs import Env

from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


def load_db_config(path: str = None):
    env = Env()
    env.read_env(path)
    return DbConfig(
        host=env.str("DB_HOST"),
        password=env.str("DB_PASS"),
        user=env.str("DB_USER"),
        database=env.str("DB_NAME"),
    )