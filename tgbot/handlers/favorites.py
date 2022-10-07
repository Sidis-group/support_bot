import operator
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import quote_html

from tgbot.keyboards import inline
from tgbot.misc import schemas
from tgbot.services import db

async def add_favorites(
    call: CallbackQuery,
    callback_data: dict,
    state: FSMContext,
    ):
    user_id = int(callback_data['id'])
    message_to_edit = await call.message.edit_text(
        text='Напишіть коментар',
        reply_markup=inline.cancel_markup,
    )
    await state.set_state('get_comment')
    await state.update_data(user_id=user_id, message_to_edit=message_to_edit.message_id)

async def get_comment_and_add_favorite(message: Message, state: FSMContext):
    state_data = await state.get_data()
    user_id = state_data['user_id']
    await state.finish()
    comment = quote_html(message.text)
    telegram_user: schemas.TelegramUser = await db.get_telegram_user(user_id)
    await db.add_favorite(
        operator_telegram_id=message.from_user.id,
        user_telegram_id=user_id, 
        comment=comment,
        user_full_name=telegram_user.full_name,
    )
    await message.delete()
    await message.bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=state_data['message_to_edit'],
        text='Користувача додано до обраного',
        reply_markup=inline.cancel_markup,
    )
    
async def see_favorites_message(message: Message):
    await message.delete()
    markup = await create_markup_for_view_favorites(0, message.from_user.id)
    text = await create_text_for_view_favorites(0, message.from_user.id)
    await message.answer(
        text=text,
        reply_markup=markup,
    )

async def see_favorites_callback(call: CallbackQuery, callback_data: dict):
    page = int(callback_data['page'])
    await call.answer()
    markup = await create_markup_for_view_favorites(page, call.from_user.id)
    text = await create_text_for_view_favorites(page, call.from_user.id)
    await call.message.edit_text(
        text=text,
        reply_markup=markup,
    )

async def see_info_about_favorite(
    call: CallbackQuery,
    callback_data: dict,
    ):
    await call.answer()
    favorite_id = int(callback_data['id'])
    favorite: schemas.Favorite = await db.get_favorite(favorite_id)
    await call.message.edit_text(
        text=f'{favorite.user_full_name}: {favorite.comment}',
        reply_markup=inline.manage_favorite_markup(favorite_id),
    )
    
async def delete_favorite(call: CallbackQuery, callback_data: dict):
    await call.answer()
    favorite_id = int(callback_data['id'])
    await db.delete_favorite(favorite_id)
    await call.message.edit_text(
        text='Користувача видалено з обраного',
        reply_markup=inline.favorite_deleted_markup,
    )

async def start_dialog_with_favorite(call: CallbackQuery, callback_data: dict):
    await call.answer()
    favorite_id = int(callback_data['id'])
    favorite: schemas.Favorite = await db.get_favorite(favorite_id)
    await db.delete_favorite(favorite_id)
    try:
        await call.bot.send_message(
            chat_id=favorite.user_id,
            text=f'Оператор хоче з вами зв\'язатися',
            reply_markup=inline.start_dialog_with_operator_markup(call.from_user.id),
        )
    except:
        return await call.message.edit_text(text='Користувач заблокував бота')
    await call.message.edit_text(
        text='Запит на діалог відправлено',
    )

async def create_text_for_view_favorites(page: int, user_id: int):
    favorites: list[schemas.Favorite] = await db.get_favorites(
        user_id
        )
    COLUMN_LENTH = 5
    start = page * COLUMN_LENTH
    end = start + COLUMN_LENTH
    text = ['Обране:\n']
    for favorite in favorites[start:end]:
        text.append(
            f'  <b>{favorite.user_full_name}</b>: {favorite.comment}\n'
        )
    return ''.join(text)

async def create_markup_for_view_favorites(page: int, user_id: int):
    favorites: list[schemas.Favorite] = await db.get_favorites(
        user_id
        )
    markup = inline.page_navigation_for_favorites_markup(favorites, page)
    return markup

def register_favorites_handlers(dp: Dispatcher):
    dp.register_message_handler(
        see_favorites_message,
        commands=['favorites'],
    )
    dp.register_callback_query_handler(
        see_favorites_callback,
        inline.navigation_for_favorite_callback.filter(),
    )
    dp.register_callback_query_handler(
        delete_favorite,
        inline.manage_favorite_callback.filter(action='delete'),
    )
    dp.register_callback_query_handler(
        start_dialog_with_favorite,
        inline.manage_favorite_callback.filter(action='start_dialog'),
    )
    dp.register_callback_query_handler(
        add_favorites,
        inline.add_to_favorite_callback.filter(),
    )
    dp.register_message_handler(
        get_comment_and_add_favorite,
        state='get_comment',
    )
    dp.register_callback_query_handler(
        see_info_about_favorite,
        inline.favorite_callback.filter(),
    )