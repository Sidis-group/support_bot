import asyncio
import re

from aiogram.types import Message, CallbackQuery, ContentTypes, ChosenInlineResult, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, Chat
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils.exceptions import CantInitiateConversation, BotBlocked

from tgbot.services import db
from tgbot.misc import schemas
from tgbot.misc import userfull
from tgbot.keyboards import inline


async def select_user(query: InlineQuery):
    if query.query:
        users = await db.search_telegram_user(query.query)
    else:
        users = await db.get_telegram_users()

    results = [
        InlineQueryResultArticle(
            id=user.telegram_id,
            title=user.full_name,
            input_message_content=InputTextMessageContent(
                message_text=user.telegram_id,
            )
        )
        for user in users
    ]

    await query.answer(results)


async def set_user(result: ChosenInlineResult, state: FSMContext):
    await state.update_data(user_id=result.result_id)
    message_to_delete = await result.bot.send_message(
        chat_id=result.from_user.id,
        text='Напишіть ваше повідомлення',
        reply_markup=inline.cancel_markup,
    )
    await state.set_state('uget_message_to_send')
    await state.update_data(message_to_delete=message_to_delete.message_id)
    
    
async def send_handler(message: Message | CallbackQuery, state: FSMContext):
    if isinstance(message, CallbackQuery):
        await message.answer()
        message = message.message
    await message.delete()
    message_to_delete = await message.answer(
        text='Напишіть ваше повідомлення',
        reply_markup=inline.cancel_markup,
    )
    await state.set_state('uget_message_to_send')
    await state.update_data(message_to_delete=message_to_delete.message_id)



async def get_message_to_send(message: Message, state: FSMContext):
    state_data = await state.get_data()
    await state.finish()
    await state.update_data(user_id=state_data["user_id"])
    message_photo = message.photo
    message_text_without_links = re.sub(r'<a[^<]+</a>', '', message.parse_entities()) 
    buttons_data = re.findall(r'<a .+"(.+)">(.+)</a>', message.parse_entities())
    buttons_message = ''.join(
        f'<a href="{url}">{text}</a>\n' for url, text in buttons_data)
    message_text = message.parse_entities()
    await message.delete()
    del_message = await message.bot.edit_message_text(
        text='1',
        chat_id=message.chat.id,
        message_id=state_data['message_to_delete'],
    )
    mailing_message: schemas.MailingMessage = await db.add_mailing_message(
        message=message_text,
        photo_id=message_photo[-1].file_id if message_photo else None,
    )
    await del_message.delete()
    if message.content_type == 'text':
        await message.answer(
            text=(
                f'{message_text_without_links}\n'
                f'Кнопки:\n'
                f'{buttons_message}'
                '-----------------------------\n'
                '<b>Ви підтверджуєте надсилання '
                'повідомлення?</b>'
            ),
            reply_markup=inline.confirm_mailing_message_user(mailing_message.id),
        )
    else: 
        await message.answer_photo(
            photo=message_photo[-1].file_id,
            caption=(
                f'{message_text_without_links}\n\n'
                '-----------------------------\n'
                '<b>Ви підтверджуєте надсилання '
                'повідомлення?</b>'
            ),
            reply_markup=inline.confirm_mailing_message_user(mailing_message.id)
        )


async def send_message_to_users(
    call: CallbackQuery,
    dp: Dispatcher,
    state: FSMContext,
    callback_data: dict,
    ):
    message_id_to_send = int(callback_data['id'])
    state_data = await state.get_data()
    mailing_message = await db.get_mailing_message(message_id_to_send)
    await call.message.delete()
    message = await call.message.answer( 
        text='Починаю розсилку',
    )
    await mailing(
        dp=dp,
        users_ids=[state_data["user_id"]],
        mailing_message=mailing_message,
    )
 
    await message.edit_text(
        text='Розсилка завершена',
    )

async def mailing(
    dp: Dispatcher,
    users_ids: list[int],
    mailing_message: schemas.MailingMessage,
    ) -> dict:
    '''Use this function to send messages to users.'''
    bot = dp.bot
    result = {
        'success': [],
        'failed': [],
    }
    buttons = inline.parse_buttons(mailing_message.message)
    message_text_without_links = re.sub(r'<a[^<]+</a>', '', mailing_message.message) 
    while users_ids: 
        await asyncio.sleep(0.5)
        user_id = users_ids.pop()
        user_state = dp.current_state(user=user_id, chat=user_id)
        if await user_state.get_state() is not None:
            continue
        try:
            if mailing_message.photo_id:
                await bot.send_photo(
                    photo=mailing_message.photo_id,
                    caption=message_text_without_links,
                    chat_id=user_id,
                    reply_markup=buttons,
                )
            else: 
                await bot.send_message(
                    chat_id=user_id,
                    text=message_text_without_links,
                    reply_markup=buttons,
                )
        except (CantInitiateConversation, BotBlocked):
            result['failed'].append(user_id)
            continue
        result['success'].append(user_id)

def register_send_message_to_user_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        send_handler,
        text='uback_to_enter_message',
    )
    dp.register_chosen_inline_handler(
        set_user
    )
    dp.register_inline_handler(
        select_user,
        is_admin=True,
    )
    dp.register_message_handler(
        get_message_to_send,
        state='uget_message_to_send',
        content_types=ContentTypes.ANY,
    )
    dp.register_callback_query_handler(
        send_message_to_users,
        inline.mailing_message_user_callback.filter(),
    )