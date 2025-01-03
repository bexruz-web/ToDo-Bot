from utils import get_translation
from database import Database

db = Database()


def send_task_notification(context):
    try:
        user_data = db.get_user_by_chat_id(context.job.context['chat_id'])
        user_language = user_data[4] if user_data else 'uz'

        chat_id = context.job.context['chat_id']
        task_name = context.job.context['task_name']

        message = get_translation("task_notification", user_language).format(task_name=task_name)
        context.bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"xatolik: {e}")


