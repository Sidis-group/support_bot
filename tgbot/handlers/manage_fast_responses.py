from aiogram.dispatcher import Dispatcher
from aiogram.types import CallbackQuery, BotCommand, BotCommandScope
from tgbot.config import Config

from tgbot.services import db
from tgbot.keyboards import inline
from tgbot.misc import schemas

async def see_all_fast_responses(call: CallbackQuery, callback_data: dict):
    await call.answer()
    page = int(callback_data.get('page', 0))
    markup = await create_markup_for_view_responses(page)
    await call.message.edit_text(
        text=(
            'Нижче ви бачите список швидких відповідей\n\n'
            'Натиснувши на відповідь ви зможете '
            'переглянути інформацію або видалити '
        ),
        reply_markup=markup
    )

async def create_markup_for_view_responses(page: int):
    responses: list[schemas.FastResponse] = await db.get_fast_responses()
    markup = inline.page_navigation_for_fast_responses_markup(responses, page)
    return markup

async def view_info_about_response(call: CallbackQuery, callback_data: dict):
    await call.answer()
    response_id = int(callback_data.get('id'))
    response: schemas.FastResponse = await db.get_fast_response(response_id)
    await call.message.edit_text(
        text=(
            'Швидка Відповідь\n\n'
            f'ID: {response.id}\n\n'
            f"{response.text}"
        ),
        reply_markup=inline.delete_fast_response_markup(response.id)
    )
    
async def delete_fast_response(
    call: CallbackQuery,
    callback_data: dict,
    messages: schemas.Messages,
    config: Config,
    ):
    await call.answer()
    response_id = int(callback_data.get('id'))
    response: schemas.FastResponse = await db.delete_fast_response(response_id)
    await call.message.edit_text(
        text=(
            f'Відповідь\n {response.text}\nвидалено'
        ),
    )

def register_manage_fast_responses_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        see_all_fast_responses,
        inline.fast_response_navigation_callback.filter(),
    )
    dp.register_callback_query_handler(
        delete_fast_response,
        inline.delete_fast_response_callback.filter(),
    )
    dp.register_callback_query_handler(
        view_info_about_response,
        inline.fast_response_callback.filter()
    )