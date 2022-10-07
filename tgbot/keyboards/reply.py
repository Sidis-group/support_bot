from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

get_phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='📞 Поділитися номером 📞',
                request_contact=True,
            )
        ]
    ],
    resize_keyboard=True
)

remove_kb = ReplyKeyboardRemove()

stop_support_dialog_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text='❗️Зупинити діалог❗️',
            )
        ]
    ],
    resize_keyboard=True
)
