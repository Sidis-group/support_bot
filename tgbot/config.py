from dataclasses import dataclass
from pathlib import Path

from environs import Env


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    webhook_url: str
    webhook_host: str
    webhook_port: int

    @property
    def webhook_path(self):
        return f'/bot/{self.token}'
    
    @property
    def webhook_main_url(self):
        return f'{self.webhook_url}{self.webhook_path}'


@dataclass
class Miscellaneous:
    firebase_certificate_path: str
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    misc: Miscellaneous



def load_config(path: str = None):
    env = Env()
    env.read_env(path)
    
    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            webhook_url=env.str("WEBHOOK_URL"),
            webhook_host=env.str("WEBHOOK_HOST"),
            webhook_port=env.int("WEBHOOK_PORT"),
        ),
        misc=Miscellaneous(
            firebase_certificate_path=env.str("FIREBASE_CERTIFICATE_PATH"),
        ),
    )
    