from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import BOT_TOKEN


from handlers import start, help_command, handle_language_change, todo_command
from message_handler import message_handler


def main():

    updater = Updater(token=BOT_TOKEN)
    dp = updater.dispatcher
    job_queue = updater.job_queue

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('language', handle_language_change))
    dp.add_handler(CommandHandler('todo', todo_command))

    dp.add_handler(MessageHandler(Filters.text, message_handler))
    print("Bot started.....")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
