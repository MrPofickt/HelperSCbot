import threading

import telebot
from telebot import types


from config import * #import TOKEN, version()
version() #пишит версию сборки

from forum import*#forumMes(nameS) forum_req(name)

from db import* #connect db
print('db connect')

import re #библиотека для проверки на наличие спецсимволов

from threading import Thread #многопоточность



#создаём бота
bot = telebot.TeleBot(TOKEN) #токен в config.py
print('bot connect')

#начало общения
list_bal = []
def botstart():
    for id in js["Users"]:
        if js["Users"][str(id)]['settings'][1] == 2:
            list_bal.append(js["Users"][str(id)])


botstart()


@bot.message_handler(commands=['start'])
def start(message):
    global js #бд
    user_id = message.from_user.id #берёт id пользователя
    chat_id = message.chat.id

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
            "settings": "0000000000",
            "chatid": chat_id
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
    bot.send_message(message.from_user.id, "Список команд:\n /start - начать \n /help - помощь \n /reg - зарегистрироваться/изменить регистрацию \n /dev - связь с разработчиком \n /forum - отслеживание сообщений разработчиков на форуме")

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
        js["Users"][str(user_id)]["chatid"] = message.chat.id
        save()
        print(f"[INFO] Пользователь {user_id} добавил ник в sc: {name}")
    else:
        bot.send_message(user_id, "Некорректный никнейм. Он должен быть одним словом, без спецсимволов и не длиннее 16 символов.")
        bot.register_next_step_handler(message, get_name)


@bot.message_handler(commands=['forum'])
def forum(message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()  # Используем InlineKeyboardMarkup
    item1 = types.InlineKeyboardButton(text="Все", callback_data='all')
    item2 = types.InlineKeyboardButton(text='Балансеры', callback_data='bal')
    item3 = types.InlineKeyboardButton(text="Главные в EXBO", callback_data='main')
    item4 = types.InlineKeyboardButton(text="КВ и сессии", callback_data='kv_sessions')
    item5 = types.InlineKeyboardButton(text="Картоделы/билдеры", callback_data='builders')
    item6 = types.InlineKeyboardButton(text="Краски/скины", callback_data='skins')

    markup.add(item1, item2, item3, item4, item5, item6)
    bot.send_message(user_id, "Выберите разработчиков какой категории вы будете отслеживать", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "bal":
        for id in js["Users"]:
            if js["Users"][id]['chatid'] == call.message.chat.id:
                # Получаем текущие настройки
                current_settings = js["Users"][id]['settings']

                # Изменяем второй символ
                new_settings = current_settings[:1] + '2' + current_settings[2:]

                # Обновляем значение в словаре
                js["Users"][id]['settings'] = new_settings

                save()  # Сохраните изменения
                bot.send_message(call.message.chat.id, 'Запомню : )')
                print(2)



def sleeptime(sec):
    time1 = time.time()
    while (time.time()-time1) >= sec:
        continue


def whileForum():
    stop = False
    while not stop:
        balansers = ['zubzalinaza', 'Furgon', 'Acidragon', 'ThaneST']
        for name in balansers:
            new_messages = forum_mes([name])
            if new_messages:
                for message in new_messages:  # отправка всех полученных сообщений по очереди
                    try:
                        for i in list_bal:
                            bot.send_message(i, f"Новое сообщение от {name}: {message}")
                    except:
                        for i in list_bal:
                            bot.send_message(i, f"Новое сообщение от {name} длинное")
        time.sleep(30)

# Запуск фонового потока
thread = threading.Thread(target=whileForum)
thread.daemon = True
thread.start()

print('bot start')
bot.polling(none_stop=True, interval=0)
print('bot stop')