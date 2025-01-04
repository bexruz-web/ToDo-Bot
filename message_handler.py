from telegram import ReplyKeyboardRemove
from datetime import datetime, timedelta

from database import Database
from send_task import send_task_notification
from utils import get_translation
from buttons import todo_buttons


db = Database()


def message_handler(update, context):
    user = update.effective_user
    text = update.message.text

    # Foydalanuvchi tilini bazadan olish
    user_data = db.get_user_by_chat_id(user.id)
    user_language = user_data[4] if user_data else 'uz'

    state = context.user_data.get('state', "")

    if state == "LANGUAGE_CHANGE":
        language_map = {
            "Uzbek": "uz",
            "English": "en"
        }

        if text in language_map:
            new_language = language_map[text]
            db.update_user_language(user.id, new_language)
            message = get_translation('language_changed', new_language)
            update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
            context.user_data['state'] = "TODO_MENU"
            todo_buttons(update, context)
        else:
            message = get_translation("invalid_option_lang", user_language)
            update.message.reply_text(message)

    elif state == "TODO_MENU":
        if text == get_translation("task_add", user_language):
            context.user_data['state'] = "ADD_TASK_NAME"
            message = get_translation("enter_task_name", user_language)
            update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())

        elif text == get_translation("task_list", user_language):
            tasks = db.get_tasks_by_chat_id(user.id)
            if tasks:
                tasks_message = "\n".join([f"• {task[1].capitalize()} --- {task[2]}" for task in tasks])
                message = f"{get_translation('tasks_list', user_language)}\n\n{tasks_message}"
                update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())

            else:
                tasks_message = get_translation("no_tasks", user_language)
                update.message.reply_text(tasks_message, reply_markup=ReplyKeyboardRemove())

        elif text == get_translation("task_remove", user_language):
            context.user_data['state'] = "REMOVE_TASK"
            tasks = db.get_tasks_by_chat_id(user.id)

            if tasks:
                tasks_message = "\n".join([f"• {task[1].capitalize()} --- {task[2]}" for task in tasks])
                message = f"{get_translation('tasks_list', user_language)}\n\n{tasks_message}"
                update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())

                message = get_translation("task_name_to_remove", user_language)
                update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())

            else:
                message = get_translation("no_tasks", user_language)
                update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())
                context.user_data['state'] = "TODO_MENU"
                todo_buttons(update, context)
                return
        else:
            update.message.reply_text(get_translation("invalid_option", user_language))

    elif state == "ADD_TASK_NAME":
        context.user_data['task_name'] = text.capitalize()
        context.user_data['state'] = "ADD_TASK_TIME"
        message = get_translation("enter_task_time", user_language)
        update.message.reply_text(message)

    elif state == "ADD_TASK_TIME":
        task_name = context.user_data.get('task_name', "🤷‍♂️")
        task_time = text

        try:
            task_time_obj = datetime.strptime(task_time, "%H:%M").time()
            now = datetime.now().time()

            # Taskni dbga saqlash
            db.add_task(user.id, task_name, task_time)
            message = get_translation("task_added", user_language).format(task_name=task_name.capitalize(), task_time=task_time)
            update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())

            if task_time_obj >= now:
                schedule_time = datetime.combine(datetime.now().date(), task_time_obj)  # Masalan natija: 2024-12-28 15:30:00
            else:
                schedule_time = datetime.combine(datetime.now().date() + timedelta(days=1), task_time_obj)

            delay = (schedule_time - datetime.now()).total_seconds()
            if delay > 0:
                context.job_queue.run_once(
                    send_task_notification, delay, context={'chat_id': user.id, 'task_name': task_name}
                )
                print(f"reja: {schedule_time}")
            else:
                print("Error")

        except ValueError as e:
            print(f"{e}")
            message = get_translation("invalid_time_format", user_language)
            update.message.reply_text(message)
            return

        context.user_data['state'] = ""

    elif state == "REMOVE_TASK":
        task_name = text.capitalize()
        tasks = db.get_tasks_by_chat_id(user.id)

        task_to_remove = next((task for task in tasks if task[1].capitalize() == task_name), None)
        if task_to_remove:
            task_id = task_to_remove[0]
            db.remove_task(task_id)
            message = get_translation("task_removed", user_language).format(task_name=task_name)
        else:
            message = get_translation("task_not_found", user_language)

        update.message.reply_text(message, reply_markup=ReplyKeyboardRemove())

        context.user_data['state'] = "TODO_MENU"
        todo_buttons(update, context)
