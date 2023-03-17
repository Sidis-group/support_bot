import re
from aiogram.utils.callback_data import CallbackData
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, \
    InlineKeyboardButton
from grpc import Call

from tgbot.misc import schemas    


cancel_button = InlineKeyboardButton(
    text='❎',
    callback_data='cancel',
)
cancel_markup = InlineKeyboardMarkup().add(cancel_button)

confirm_support_request_callback = CallbackData('confirm_support_request', 'id')
def confirm_support_request_markup(
    support_request_id: int
    ) -> InlineKeyboardMarkup: 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Підтвердити',
                    callback_data=confirm_support_request_callback.new(
                        id=support_request_id,
                    )
                )
            ]
        ]
    )

mailing_message_callback = CallbackData('mailing_message', 'id')
def confirm_mailing_message(
    message_id: int
    ) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✅Надіслати',
                    callback_data=mailing_message_callback.new(
                        id=message_id,
                    )
                )
            ],
            [
                
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data='back_to_enter_message'
                ),
                cancel_button,
            ]
        ]
    )

mailing_message_user_callback = CallbackData('mailing_message_user', 'id')
def confirm_mailing_message_user(
    message_id: int
    ) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✅Надіслати',
                    callback_data=mailing_message_user_callback.new(
                        id=message_id,
                    )
                )
            ],
            [
                
                InlineKeyboardButton(
                    text='⬅️',
                    callback_data='uback_to_enter_message'
                ),
                cancel_button,
            ]
        ]
    )
 
    

operator_navigation_callback = CallbackData('operator_navigation', 'page')
fast_response_navigation_callback = CallbackData('f_resp_navigation', 'page')
operators_menu_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='📜Переглянути операторів📜',
                callback_data=operator_navigation_callback.new(
                    page=0,
                )
            )
        ],
        [
            InlineKeyboardButton(
                text='➕ Додати оператора ➕',
                callback_data='add_operator',
            )
        ],
        [
            InlineKeyboardButton(
                text='📜Переглянути швидкі відповіді📜',
                callback_data=fast_response_navigation_callback.new(
                    page=0,
                )
            )
        ],
 
        [
            InlineKeyboardButton(
                text='➕ Додати швидку відповідь ➕',
                callback_data="add_fast_response"
            )
        ],
        [cancel_button]
    ]
)

operator_callback = CallbackData('operator', 'telegram_id')
def page_navigation_for_operators_markup(
    operators: list[schemas.Operator], page: int
) -> InlineKeyboardMarkup:
    COLUMN_LENTH = 5
    markup = InlineKeyboardMarkup()
    start = page * COLUMN_LENTH
    end = start + COLUMN_LENTH
    for operator in operators[start:end]:
        markup.add(
            InlineKeyboardButton(
                text=f'{operator.full_name}',
                callback_data=operator_callback.new(telegram_id=operator.telegram_id),
            )
        )
    markup = add_navigation_buttons(
        markup, page, COLUMN_LENTH, len(operators), operator_navigation_callback
        )
    markup.add(
        InlineKeyboardButton(
            text='⬅',
            callback_data='operators_menu',
        ),
        cancel_button
    )
    return markup

fast_response_callback = CallbackData('fast_response', 'id')
def page_navigation_for_fast_responses_markup(
    responses: list[schemas.FastResponse], page: int
) -> InlineKeyboardMarkup:
    COLUMN_LENTH = 5
    markup = InlineKeyboardMarkup()
    start = page * COLUMN_LENTH
    end = start + COLUMN_LENTH
    for response in responses[start:end]:
        markup.add(
            InlineKeyboardButton(
                text=f'{response.text}',
                callback_data=fast_response_callback.new(id=response.id),
            )
        )
    markup = add_navigation_buttons(
        markup, page, COLUMN_LENTH, len(responses), fast_response_navigation_callback
        )
    markup.add(
        InlineKeyboardButton(
            text='⬅',
            callback_data='operators_menu',
        ),
        cancel_button
    )
    return markup
 
    
def add_navigation_buttons(
    markup: InlineKeyboardMarkup, page: int, column_lenth: int, total_items: int,
    callback: CallbackData,
    ) -> InlineKeyboardMarkup:
    if page == 0 and total_items > column_lenth:
        markup.row(
            InlineKeyboardButton(
                text='⠀',
                callback_data='first_page',
            ),
            InlineKeyboardButton(
                text='➡️',
                callback_data=callback.new(page=page+1),
            )
        )
    elif page == 0:
        pass
    elif page == total_items // column_lenth:
        markup.row(
            InlineKeyboardButton(
                text='⬅️',
                callback_data=callback.new(page=page-1),
            ),
            InlineKeyboardButton(
                text='⠀',
                callback_data='last_page',
            )
        )
    else:
        markup.row(
            InlineKeyboardButton(
                text='⬅️',
                callback_data=callback.new(page=page-1),
            ),
            InlineKeyboardButton(
                text='➡️',
                callback_data=callback.new(page=page+1),
            )
        )
    return markup

delete_operator_callback = CallbackData('delete', 'telegram_id')
def delete_operator_markup(operator_telegram_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='❌ Видалити ❌',
                    callback_data=delete_operator_callback.new(
                        telegram_id=operator_telegram_id,
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text='⬅',
                    callback_data=operator_navigation_callback.new(
                        page=0
                    ),
                ),
                cancel_button
            ]
        ]
    )

def apply_operator_markup(deep_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='↗️ Стати оператором ↗️',
                    url=deep_link,
                )
            ]
        ]
    )

add_to_favorite_callback = CallbackData('add_to_favorite', 'id')
def add_to_favorite_markup(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='👍 Додати в обране 👍',
                    callback_data=add_to_favorite_callback.new(
                        id=user_id,
                    )
                )
            ],[cancel_button]
        ]
    )

favorite_callback = CallbackData('favorite', 'id')
navigation_for_favorite_callback = CallbackData('navigation_for_favorite', 'page')
def page_navigation_for_favorites_markup(
    favorites: list[schemas.Favorite], page: int
) -> InlineKeyboardMarkup:
    COLUMN_LENTH = 5
    markup = InlineKeyboardMarkup()
    start = page * COLUMN_LENTH
    end = start + COLUMN_LENTH
    for favorite in favorites[start:end]:
        markup.add(
            InlineKeyboardButton(
                text=f'{favorite.user_full_name}',
                callback_data=favorite_callback.new(id=favorite.id),
            )
        )
    markup = add_navigation_buttons(
        markup, page, COLUMN_LENTH, len(favorites),
        navigation_for_favorite_callback,
        )
    markup.add(cancel_button)
    return markup


manage_favorite_callback = CallbackData('manage_favorite', 'id', 'action')
def manage_favorite_markup(favorite_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='Почати діалог',
                    callback_data=manage_favorite_callback.new(
                        id=favorite_id,
                        action='start_dialog',
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text='Видалити з обраних',
                    callback_data=manage_favorite_callback.new(
                        id=favorite_id,
                        action='delete',
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text='⬅',
                    callback_data=navigation_for_favorite_callback.new(
                        page=0
                    ),
                ),
                cancel_button
            ],
        ]
    )
                        
start_dialog_callback = CallbackData('start_dialog', 'telegram_id')
def start_dialog_with_operator_markup(operator_telegram_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='👤 Почати діалог 👤',
                    callback_data=start_dialog_callback.new(
                        telegram_id=operator_telegram_id,
                    )
                )
            ],
            [
                cancel_button
            ]
        ]
    )

favorite_deleted_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='⬅',
                callback_data=navigation_for_favorite_callback.new(
                    page=0
                ),
            ),
            cancel_button
        ]
    ]
)

markup_after_creating_link = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='⬅',
                callback_data='operators_menu',
            ),
            cancel_button
        ]
    ]
)

def parse_buttons(message: str): 
    buttons = re.findall(r'<a .+"(.+)">(.+)</a>', message)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text,
                    url=url
                )
            ] for url, text in buttons
        ]
    )

delete_fast_response_callback = CallbackData('delete_fr', 'id')
def delete_fast_response_markup(response_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='❌ Видалити ❌',
                    callback_data=delete_fast_response_callback.new(
                        id=response_id
                    ),
                )
            ],
            [
                InlineKeyboardButton(
                    text='⬅',
                    callback_data=fast_response_navigation_callback.new(
                        page=0
                    ),
                ),
                cancel_button
            ]
        ]
    )


send_mode = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Всім",
                callback_data="all",
            )
        ],
        [
            InlineKeyboardButton(
                text="Певному користувачу",
                switch_inline_query_current_chat="",
            )
        ],[cancel_button]

    ]
)

connect_opeartor = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Підключити оператора",
                callback_data="connect_operator",
            )
        ]
    ]
)