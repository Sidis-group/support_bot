import uuid

from asgiref.sync import sync_to_async

from web.app import models
from tgbot.misc import schemas


@sync_to_async
def add_telegram_user(telegram_id: int, full_name: str) -> None:
    models.TelegramUser.objects.get_or_create(
        telegram_id=telegram_id,
        full_name=full_name,
    )

@sync_to_async
def get_telegram_users() -> schemas.TelegramUser:
    return list(
        schemas.TelegramUser(**user) \
            for user in models.TelegramUser.objects.all().values()
    )

@sync_to_async
def search_telegram_user(query: str) -> list[schemas.TelegramUser]:
    return [
        schemas.TelegramUser(**user) 
        for user in models.TelegramUser.objects.filter(
            full_name__icontains=query).values()
    ]

@sync_to_async
def get_telegram_user(telegram_id: int) -> schemas.TelegramUser:
    return schemas.TelegramUser(
        **models.TelegramUser.objects.get(telegram_id=telegram_id).dict()
    )

@sync_to_async
def add_support_request(
    user_telegram_id: int,
    ) -> schemas.SupportRequest:
    request: models.SupportRequest = models.SupportRequest.objects.create(
        user_id=user_telegram_id,
    )
    return schemas.SupportRequest(**request.dict())

@sync_to_async
def delete_support_request(request_id) -> None:
    models.SupportRequest.objects.get(id=request_id).delete()

@sync_to_async
def get_support_request(id: int) -> schemas.SupportRequest:
    request: models.SupportRequest = models.SupportRequest.objects.get(id=id)
    return schemas.SupportRequest(**request.dict())

@sync_to_async
def add_operator(telegram_id: int, full_name: str) -> schemas.Operator:
    operator: models.Operator = models.Operator.objects.create(
        telegram_id=telegram_id,
        full_name=full_name,
    )
    return schemas.Operator(**operator.dict())

@sync_to_async
def delete_operator(id: int) -> schemas.Operator:
    operator: models.Operator = models.Operator.objects.get(telegram_id=id)
    operator_schema = schemas.Operator(**operator.dict())
    operator.delete()
    return operator_schema

@sync_to_async
def get_operators() -> list[schemas.Operator]:
    return list(
        schemas.Operator(**operator) \
            for operator in models.Operator.objects.all().values()
    )

@sync_to_async
def get_operator(id: int) -> schemas.Operator:
    operator: models.Operator = models.Operator.objects.get(telegram_id=id)
    return schemas.Operator(**operator.dict())

@sync_to_async
def add_operator_confirm_uuid() -> uuid.UUID:
    uuid_ = models.OperatorConfirmUUID.objects.create()
    return uuid_.uuid 

@sync_to_async
def delete_operator_confirm_uuid(uuid_: uuid.UUID) -> None:
    models.OperatorConfirmUUID.objects.get(uuid=uuid_).delete()

@sync_to_async
def get_all_operator_confirm_uuids() -> list[uuid.UUID]:
    return list(
        uuid_.uuid \
            for uuid_ in models.OperatorConfirmUUID.objects.all()
    )

@sync_to_async
def add_favorite(
    operator_telegram_id: int,
    user_telegram_id: int,
    comment: str,
    user_full_name: str,
    ) -> schemas.Favorite:
    favorite: models.Favorite = models.Favorite.objects.create(
        operator_id=operator_telegram_id,
        user_id=user_telegram_id,
        comment=comment,
        user_full_name=user_full_name,
    )
    return schemas.Favorite(**favorite.dict())


@sync_to_async
def get_favorites(
    operator_telegram_id: int,
    ) -> list[schemas.Favorite]:
    return list(
        schemas.Favorite(**favorite.dict()) \
            for favorite in models.Favorite.objects.filter(
                operator_id=operator_telegram_id,
            )
    )

@sync_to_async
def get_favorite(id: int) -> schemas.Favorite:
    favorite: models.Favorite = models.Favorite.objects.get(id=id)
    return schemas.Favorite(**favorite.dict())
@sync_to_async
def delete_favorite(id: int) -> schemas.Favorite:
    favorite: models.Favorite = models.Favorite.objects.get(id=id)
    favorite_schema = schemas.Favorite(**favorite.dict())
    favorite.delete()
    return favorite_schema

#create functions that create, read, delete mailing message
@sync_to_async
def add_mailing_message(message: str, photo_id: str | None=None) -> schemas.MailingMessage:
    mailing_message: models.MailingMessage = models.MailingMessage.objects.create(
        message=message,
        photo_id=photo_id,
    )
    return schemas.MailingMessage(**mailing_message.dict())

@sync_to_async
def delete_mailing_message(id: int) -> schemas.MailingMessage:
    mailing_message: models.MailingMessage = models.MailingMessage.objects.get(id=id)
    mailing_message_schema = schemas.MailingMessage(**mailing_message.dict())
    mailing_message.delete()
    return mailing_message_schema

@sync_to_async
def get_mailing_message(id: int) -> schemas.MailingMessage:
    mailing_message: models.MailingMessage = models.MailingMessage.objects.get(id=id)
    return schemas.MailingMessage(**mailing_message.dict())

@sync_to_async
def add_admin(telegram_id: int, invite_code: str):
    models.Admin.objects.create(telegram_id=telegram_id, invite_code=invite_code)

@sync_to_async
def get_admins_invite_codes() -> list[str]:
    return list(
        admin.invite_code \
            for admin in models.Admin.objects.all()
    )

def get_admins_ids() -> list[int]:
    return list(
        admin.telegram_id \
            for admin in models.Admin.objects.all()
    )

@sync_to_async
def get_fast_responses() -> list[schemas.FastResponse]:
    return [
        schemas.FastResponse(**response.dict()) 
        for response in models.FastResponse.objects.all()
    ]

@sync_to_async
def add_fast_response(text: str) -> None:
    models.FastResponse.objects.create(text=text)

@sync_to_async
def delete_fast_response(response_id: int) -> None:
    resp = models.FastResponse.objects.get(id=response_id)
    s = schemas.FastResponse(**resp.dict())
    resp.delete()
    return s

@sync_to_async
def get_fast_response(response_id: int) -> schemas.FastResponse:
    resp = models.FastResponse.objects.get(id=response_id)
    return schemas.FastResponse(**resp.dict())