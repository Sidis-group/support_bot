from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

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

    def set_admins_ids(self):
        if self.admin_ids is None:
            self.admin_ids = []
        executor = ThreadPoolExecutor(1)
        future = executor.submit(get_admins_ids)
        admins_ids = future.result()
        self.admin_ids.extend(admins_ids)
        self.admin_ids = list(map(int, self.admin_ids))


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
    
    config =  Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            deeplink_key=env.str("DEEPLINK_KEY"),
            admin_ids=env.list("ADMINS"),
            name=env.str("BOT_NAME"),
            webhook_url=env.str("WEBHOOK_URL"),
            webhook_host=env.str("WEBHOOK_HOST"),
            webhook_port=env.int("WEBHOOK_PORT"),
        ),
        misc=Miscellaneous(
            firebase_certificate_path=env.str("FIREBASE_CERTIFICATE_PATH"),
        ),
    )
    config.tg_bot.set_admins_ids()
    return config
    