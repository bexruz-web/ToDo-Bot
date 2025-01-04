from telegram import ReplyKeyboardMarkup

from database import Database
from utils import get_translation

db = Database()


def todo_buttons(update, context):
    user = update.effective_user

    user_data = db.get_user_by_chat_id(user.id)
    user_language = user_data[4] if user_data else 'uz'

    keyboard = [
        [get_translation("task_add", user_language), get_translation("task_list", user_language)],
        [get_translation("task_remove", user_language)]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    choose_language_message = get_translation('todo_button_for_message', user_language)
    update.message.reply_text(choose_language_message, reply_markup=reply_markup)


