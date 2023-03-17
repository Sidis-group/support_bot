from firebase_admin import credentials, firestore, initialize_app
from google.cloud.firestore_v1.client import Client

from tgbot.config import load_config
from tgbot.misc import schemas


config = load_config()

credential = credentials.Certificate(config.misc.firebase_certificate_path)

initialize_app(credential)

firebase_db: Client = firestore.client()

def get(bot_name: str, collection: str, field: str):
    bots_collection = firebase_db.collection(collection)
    bot_document = bots_collection.document(bot_name)
    bot_field_data = bot_document.get()     
    try:
        current_field = bot_field_data.get(field)
    except KeyError:
        current_field = 'No value'
    return current_field

def get_custom_messages() -> schemas.Messages:
    messages_texts_needed = schemas.Messages.schema()['properties'].keys()
    messages = {}
    for message_text_need in messages_texts_needed:
        messages[message_text_need] = get("SidisTestsBot", 'setup', message_text_need)
    return schemas.Messages(**messages)
