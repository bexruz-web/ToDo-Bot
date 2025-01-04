from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import BotCommand
from database import Database
from utils import get_translation
from buttons import todo_buttons

db = Database()


def start(update, context):
    commands = [
        BotCommand(command='start', description="Boshlash | Start"),
        BotCommand(command='todo', description="Vazifalar | To-do"),
        BotCommand(command='help', description="Yordam | Help"),
        BotCommand(command='language', description="Tilni tanlash | Choose lang"),
    ]
    context.bot.set_my_commands(commands=commands)

    user = update.effective_user
    user_db = db.get_user_by_chat_id(user.id)

    if user_db is None:
        db.create_user(
            first_name=user.first_name,
            username=user.username if user.username else "Username yo'q",
            chat_id=user.id,
            lang="uz"          # default til
        )

        user_data = db.get_user_by_chat_id(user.id)
        user_lang = user_data[4] if user_data else 'uz'

        message = get_translation("welcome_message", user_lang).format(user.first_name)
        update.message.reply_text(message, reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")

    else:
        user_data = db.get_user_by_chat_id(user.id)
        user_lang = user_data[4] if user_data else 'uz'

        message = get_translation('regular_welcome_message', user_lang).format(user.first_name)
        update.message.reply_text(message, reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")


def help_command(update, context):
    user = update.effective_user

    user_data = db.get_user_by_chat_id(user.id)
    user_language = user_data[4] if user_data else 'uz'

    message = get_translation('help_message', user_language)
    update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())


def todo_command(update, context):
    text = update.message.text

    if text == "/todo":
        todo_buttons(update, context)

        context.user_data['state'] = "TODO_MENU"


def handle_language_change(update, context):
    context.user_data['state'] = "LANGUAGE_CHANGE"
    """Foydalanuvchi tilini ozgartirish"""
    user = update.effective_user
    text = update.message.text

    user_data = db.get_user_by_chat_id(user.id)
    user_language = user_data[4] if user_data else 'uz'

    if text == "/language":
        keyboard = [
            ['Uzbek'],
            ['English'],
        ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        choose_language_message = get_translation("choose_language", user_language)
        update.message.reply_text(choose_language_message, reply_markup=reply_markup)
        return
