import asyncio
from asgiref.sync import sync_to_async
from dataclasses import dataclass

from environs import Env

from tgbot.services.db import get_admins_ids


@dataclass
class TgBot:
    token: str
    deeplink_key: str
    name: str
    webhook_url: str
    webhook_host: str
    webhook_port: int
    admin_ids: list[int] = None

    async def set_admins_ids(self):
        self.admin_ids = await get_admins_ids()


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
            deeplink_key=env.str("DEEPLINK_KEY"),
            name=env.str("BOT_NAME"),
            webhook_url=env.str("WEBHOOK_URL"),
            webhook_host=env.str("WEBHOOK_HOST"),
            webhook_port=env.int("WEBHOOK_PORT"),
        ),
        misc=Miscellaneous(
            firebase_certificate_path=env.str("FIREBASE_CERTIFICATE_PATH"),
        ),
    )
    