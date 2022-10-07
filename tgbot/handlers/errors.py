from aiogram.dispatcher import Dispatcher
from aiogram.types import Update

from tgbot.misc.exceptions import *
from web.app import models


async def support_confirmed_by_other(
    update: Update,
    exception: models.SupportRequest.DoesNotExist,
    ) -> bool:
    await update.callback_query.message.edit_text(
        text='Цей запит вже був підтверджений іншим оператором',
    )
    return True
    

def register_error_handlers(dp: Dispatcher):
    dp.register_errors_handler(
        callback=support_confirmed_by_other,
        exception=models.SupportRequest.DoesNotExist,
    )
    