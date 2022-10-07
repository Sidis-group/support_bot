import asyncio
import typing

from aiogram.bot import Bot
from aiogram.types import Message
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import CantInitiateConversation, BotBlocked
from aiohttp import ClientSession



async def mailing(
    dp: Dispatcher,
    users_ids: list[int],
    message: Message,
    ) -> dict:
    '''Use this function to send messages to users.'''
    bot = dp.bot
    result = {
        'success': [],
        'failed': [],
    }
    while users_ids: 
        await asyncio.sleep(0.5)
        user_id = users_ids.pop()
        user_state = dp.current_state(user=user_id, chat=user_id)
        if await user_state.get_state() is not None:
            continue
        try:
            if message.photo:
                await bot.send_photo(
                    photo=message.photo[-1].file_id,
                )
            await bot.copy_message(
                from_chat_id=message.from_user.id,
                message_id=message.message_id,
                chat_id=user_id,
            )
        except (CantInitiateConversation, BotBlocked):
            result['failed'].append(user_id)
            continue
        result['success'].append(user_id)
        
async def request(
    session: ClientSession,
    method: str,
    url: str,
    **kwargs: typing.Any,
    ) -> dict:
    '''Use this function to make requests.'''
    async with session.request(method, url, **kwargs) as response:
        return await response.json()