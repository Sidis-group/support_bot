from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery


async def delete_message(message: Message):
    await message.delete()

def register_system_handlers(dp: Dispatcher):
    dp.register_message_handler(
        delete_message,
        )