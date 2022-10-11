from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards import inline


async def show_operators_menu_handler(message: Message):
    await message.delete()
    await message.answer(
        text='Натискайте кнопку',
        reply_markup=inline.operators_menu_markup,
    )
async def show_operators_menu_handler_call(call: CallbackQuery):
    await call.message.edit_text(
        text='Натискайте кнопку',
        reply_markup=inline.operators_menu_markup,
    )


def register_operators_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(
        show_operators_menu_handler,
        commands=['menu'],
        is_admin=True
    )
    dp.register_callback_query_handler(
        show_operators_menu_handler_call,
        text='operators_menu',
    )