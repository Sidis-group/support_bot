from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScope
from aiogram.utils.exceptions import ChatNotFound


from tgbot.misc import schemas
from tgbot.config import Config
from tgbot.services import db


async def set_commands_to_admins(bot: Bot):
    messages: schemas.Messages = bot['messages']
    config: Config = bot['config']
    operators: list[schemas.Operator] = await db.get_operators()
    operators_ids = [operator.telegram_id for operator in operators]
    for admin_id in config.tg_bot.admin_ids:
        try:
            if admin_id not in operators_ids:
                await bot.set_my_commands(
                    commands=[
                        BotCommand(command="/send", description=messages.send_command),
                        BotCommand(command='/menu', description=messages.menu_command),
                    ],
                    scope=BotCommandScope(chat_id=admin_id, type='chat')
                )
            else:
                await bot.set_my_commands(
                    commands=[
                        BotCommand(command="/send", description=messages.send_command),
                        BotCommand(command='/menu', description=messages.menu_command),
                        BotCommand(command='/favorites', description=messages.favorites_command),
                    ],
                    scope=BotCommandScope(chat_id=admin_id, type='chat')
                )
        except ChatNotFound:
            pass