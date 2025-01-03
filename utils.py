import json

from config import LANGUAGES
from database import Database

db = Database()


def load_translations():
    translations = {}
    for lang in LANGUAGES:

        with open(f"langs/{lang}.json", "r", encoding="utf-8") as file:
            translations[lang] = json.load(file)

    return translations


TRANSLATIONS = load_translations()


def get_translation(key, language = "en"):
    return TRANSLATIONS.get(language, {}).get(key, key)


def get_user_lang(user_id):
    user_data = db.get_user_by_chat_id(user_id)
    return user_data[4] if user_data else 'uz'
