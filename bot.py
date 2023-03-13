import sys
import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScope
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.exceptions import ChatNotFound
from aiogram.utils.executor import start_webhook

from tgbot.misc.setup_django import setup_django; setup_django()
from tgbot.filters.admin import AdminFilter
from tgbot.misc import schemas
from tgbot.services import db, firebase
from tgbot.config import load_config, Config
from tgbot.filters.operator import OperatorFilter
from tgbot.handlers.send import register_send_handlers
from tgbot.filters.admin_deep_link import AdminDeepLink
from tgbot.handlers.start import register_start_handlers
from tgbot.handlers.errors import register_error_handlers
from tgbot.handlers.system import register_system_handlers
from tgbot.handlers.add_fast_response import register_add_fast_response_handlers
from tgbot.handlers.support import register_support_handlers
from tgbot.filters.operator_deep_link import OperatorDeepLink
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.handlers.favorites import register_favorites_handlers
from tgbot.handlers.add_operator import register_add_operator_handlers
from tgbot.handlers.operators_menu import register_operators_menu_handlers
from tgbot.handlers.manage_operators import register_manage_operators_handlers
from tgbot.handlers.manage_fast_responses import register_manage_fast_responses_handlers
from tgbot.handlers.send_message_to_user import register_send_message_to_user_handlers

logger = logging.getLogger(__name__)


def register_all_middlewares(
    dp: Dispatcher, 
    config: Config,
    storage: RedisStorage2 | MemoryStorage,
    scheduler: AsyncIOScheduler,
    messages: schemas.Messages,
    ):
    dp.setup_middleware(
        EnvironmentMiddleware(
            config=config,
            dp=dp,
            storage=storage,
            scheduler=scheduler,
            messages=messages
        )
    )

def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(OperatorFilter)
    dp.filters_factory.bind(OperatorDeepLink)
    dp.filters_factory.bind(AdminDeepLink)


def register_all_handlers(dp: Dispatcher):
    register_favorites_handlers(dp)
    register_add_operator_handlers(dp)
    register_start_handlers(dp)
    register_support_handlers(dp)
    register_send_handlers(dp)
    register_error_handlers(dp)
    register_operators_menu_handlers(dp)
    register_manage_operators_handlers(dp)
    register_add_fast_response_handlers(dp)
    register_manage_fast_responses_handlers(dp)
    register_send_message_to_user_handlers(dp)
    register_system_handlers(dp)

async def set_commands_to_bot(bot: Bot):
    messages: schemas.Messages = bot['messages']
    await bot.set_my_commands(
        commands=[
            BotCommand(command="/start", description=messages.start_command),
        ]
    )

async def set_commands_to_operators(bot: Bot):
    messages: schemas.Messages = bot['messages']
    operators: list[schemas.Operator] = await db.get_operators()
    operators_ids = [operator.telegram_id for operator in operators]
    for operator_id in operators_ids:
        await bot.set_my_commands(
            commands=[
                BotCommand(command='/favorites', description=messages.favorites_command),
            ],
            scope=BotCommandScope(chat_id=operator_id, type='chat')
        )


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

async def on_startup(dp: Dispatcher):
    formatter = logging.Formatter(
        fmt=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        datefmt="%H:%M:%S"
    )
    logging.basicConfig(
        level=logging.INFO,
        format=formatter._fmt,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('log/bot/bot.log'),
        ]
    )

    logger.info("Starting bot")
    config = load_config(".env")
    logger.info('Making migrations')
    os.system('python3 django_manage.py makemigrations')
    logger.info('Applying migrations')
    os.system('python3 django_manage.py migrate')

    scheduler = AsyncIOScheduler()
    messages = firebase.get_custom_messages()

    bot['config'] = config
    bot['messages'] = messages
    register_all_middlewares(dp, config, storage, scheduler, messages)
    register_all_filters(dp)
    register_all_handlers(dp)

    await set_commands_to_operators(bot)
    await set_commands_to_admins(bot)
    await set_commands_to_bot(bot)
    await dp.bot.set_webhook(
        config.tg_bot.webhook_main_url
    )

    # start
    scheduler.start()

async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await dp.bot.session.close()


if __name__ == '__main__':
    config = load_config(".env")
    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    start_webhook(
        dispatcher=dp,
        webhook_path=config.tg_bot.webhook_path,
        skip_updates=True,
        host=config.tg_bot.webhook_host,
        port=config.tg_bot.webhook_port,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )
        
