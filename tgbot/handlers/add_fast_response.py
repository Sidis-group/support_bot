import uuid

from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, BotCommand, BotCommandScope
from aiogram.utils.deep_linking import get_start_link


from tgbot.keyboards import inline
from tgbot.misc import schemas, states
from tgbot.services import db
from tgbot.config import Config


async def input_fast_response(call: CallbackQuery, state: FSMContext):
    await state.set_state("input_fast_response")

    m = await call.message.edit_text(text="Введіть текст швидкої відповіді")

    await state.update_data(start_message_id=m.message_id)


async def save_fast_response(message: Message, state: FSMContext):
    await db.add_fast_response(text=message.text)

    await message.delete()

    state_data = await state.get_data()
    await state.finish()

    await message.bot.edit_message_text(
        text="Швидку відповідь додано",
        chat_id=message.chat.id,
        message_id=state_data["start_message_id"],
    )



def register_add_fast_response_handlers(dp: Dispatcher):
    dp.register_message_handler(
        save_fast_response,
        state="input_fast_response",
    )
    dp.register_callback_query_handler(
        input_fast_response,
        text="add_fast_response",
    )

