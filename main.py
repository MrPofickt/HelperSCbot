import telebot
from config import * #import TOKEN, version()

version() #пишит версию сборки

from db import* #connect db
print('db connect')

import re #библиотека для проверки на наличие спецсимволов


#создаём бота
bot = telebot.TeleBot(TOKEN) #токен в config.py
print('bot connect')

#начало общения
@bot.message_handler(commands=['start'])
def start(message):
    global js #бд
    user_id = message.from_user.id #берёт id пользователя

    #проверка пользователя в бд
    for id in js["Users"]:
        if str(user_id) == str(id):
            bot.send_message(message.from_user.id, f"Привет, {js['Users'][str(user_id)]['name']}. напиши /help")
            break
    else:
        #пользователь не найден
        len_bs = len(js['Users'])
        app = {
            "id": len_bs,
            "idTG": user_id,
            "name": "",
            "namesc": "",
            "vip": False,
            "settings": ""
        }
        #доп проверка
        if str(user_id) in js["Users"]:
            pass
        else:
            js["Users"][user_id] = app #записываем данные
            save() #созранение в бд
            print("[INFO] ADD user", user_id)
            bot.send_message(message.from_user.id, "Зарегистрируйся через команду /reg")


@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.from_user.id, "Список команд:\n /start - начать \n /help - помощь \n /reg - зарегистрироваться/изменить регистрацию \n /dev - связь с разработчиком")

@bot.message_handler(commands=['dev'])
def start(message):
    bot.send_message(message.from_user.id, "discord: mrpofickt, email: anonimgosis@gmail.com")

@bot.message_handler(commands=['reg'])
def start(message):
    bot.send_message(message.from_user.id, "Напиши свой никнейм для бота")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text

    # Проверяем никнейм
    if is_valid_nickname(name):
        reg_z = False #ник не занят
        for id in js["Users"]:
            if js["Users"][str(user_id)]["name"] == name:
                bot.send_message(message.from_user.id, "Некорректный никнейм. Он уже занят.")
                reg_z = True #ник занят
                break
        if reg_z == False:
            bot.send_message(message.from_user.id, f"Никнейм '{name}' принят!")
            js["Users"][str(user_id)]["name"] = name
            save()
            print(f"[INFO] user {user_id} add nick", name)
            bot.send_message(message.from_user.id, "Напиши свой никнейм в сталкрафте")
            bot.register_next_step_handler(message, get_namesc)

    else:
        bot.send_message(message.from_user.id, "Некорректный никнейм. Он должен быть одним словом, без спецсимволов и не длиннее 16 символов.")
        bot.register_next_step_handler(message, get_name)

#проверка правильности ника
def is_valid_nickname(nickname):
    # Проверяем длину
    if len(nickname) > 16:
        return False
    # Проверяем на наличие спецсимволов
    if not re.match("^[A-Za-z0-9]+$", nickname):
        return False
    return True


def get_namesc(message):
    name = message.text.strip()  # Убираем лишние пробелы
    user_id = str(message.from_user.id)  # Приводим user_id к строке для соответствия JSON

    if is_valid_nickname(name):
        bot.send_message(user_id, f"Никнейм в ск '{name}' принят!")
        js["Users"][str(user_id)]["namesc"] = name
        save()
        print(f"[INFO] Пользователь {user_id} добавил ник в sc: {name}")
    else:
        bot.send_message(user_id, "Некорректный никнейм. Он должен быть одним словом, без спецсимволов и не длиннее 16 символов.")
        bot.register_next_step_handler(message, get_name)


print('bot start')
bot.polling(none_stop=True, interval=0)
print('bot stop')