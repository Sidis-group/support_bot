import datetime

from pydantic import BaseModel


class TelegramUser(BaseModel):
    telegram_id: int
    full_name: str
    join_time: datetime.datetime
    language: str

class SupportRequest(BaseModel):
    id: int
    user_id: int
    created_time: datetime.datetime

class   Messages(BaseModel):
    start_command: str
    send_command: str
    greetings_text: str
    start_chat_text: str
    menu_command: str
    favorites_command: str

class Operator(BaseModel):
    telegram_id: int
    full_name: str
    join_time: datetime.datetime

class Favorite(BaseModel):
    id: int
    operator_id: int
    user_id: int
    user_full_name: str
    comment: str

class MailingMessage(BaseModel):
    id: int
    message: str
    created_time: datetime.datetime
    photo_id: str | None = None
    