from aiogram.dispatcher import Dispatcher
from aiogram.types import Message

from tgbot.services import db
from tgbot.misc import schemas
from tgbot.handlers import support
from tgbot.config import Config
from tgbot.misc.commands import set_commands_to_admins


async def start_handler(message: Message, messages: schemas.Messages):
    await message.answer(
        text=messages.greetings_text.format(
            username=message.from_user.full_name
            ).replace('\\n', '\n'),
    )
    await db.add_telegram_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name,
    )
    await support.support_handler(message, messages)
    
async def start_admin(message: Message):
    await db.add_admin(message.from_user.id)
    await message.answer('Ви тепер адміністратор')
    config: Config = message.bot.get('config')
    await config.tg_bot.set_admins_ids()
    await set_commands_to_admins(message.bot)

def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(
        start_admin,
        is_admin_deep_link=True,
    )
    dp.register_message_handler(
        start_handler,
        commands=['start'],
        is_admin=False,
        is_operator=False,
    )