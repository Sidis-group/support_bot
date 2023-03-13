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


def fast_responses_kb(responses: list) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text='❗️Зупинити діалог❗️',
                ),
 
            ],
            *[
            [
                KeyboardButton(
                    text=response.text
                )
            ] for response in responses
            ]
        ],
        resize_keyboard=True
    )