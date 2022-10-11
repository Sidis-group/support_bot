import base64
import hashlib
from inspect import signature
import typing

from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import  load_config


class AdminDeepLink(BoundFilter):
    key = 'is_admin_deep_link'

    def __init__(self, is_admin_deep_link: typing.Optional[bool] = None):
        self.is_admin_deep_link = is_admin_deep_link

    async def check(self, obj):
        if self.is_admin_deep_link is None:
            return False
        config = load_config()
        args: str = obj.get_args()
        try: 
            decoded_args = base64.b64decode(args).decode()
        except:
            return False
        try:
            key, signature = decoded_args.split('|')
        except ValueError:
            return False
        hash = hashlib.md5(
            f'{key}|{config.tg_bot.name}|{config.tg_bot.deeplink_key}'.encode()
        ).hexdigest()
        if hash == signature:
            return True
        return False



