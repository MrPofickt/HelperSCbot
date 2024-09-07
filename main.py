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

def sleeptime(sec):
    time1 = time.time()
    while (time.time() - time1) < sec:
        pass


#начало общения
list_all = [] #1
list_bal = [] #2
list_main = [] #3
list_kv_sessions = [] #4
list_skins = [] #5
list_other = [] #6
list_rup = [] #7
def botstart():
    list_all.clear()
    list_bal.clear()
    list_main.clear()
    list_kv_sessions.clear()
    list_skins.clear()
    list_other.clear()
    list_rup.clear()
    for id in js["Users"]:
        if js["Users"][str(id)]['settings'][1] == '2':
            list_bal.append(js["Users"][str(id)]['chatid'])
    for id in js["Users"]:
        if js["Users"][str(id)]['settings'][1] == '3':
            list_main.append(js["Users"][str(id)]['chatid'])
    for id in js["Users"]:
        if js["Users"][str(id)]['settings'][1] == '4':
            list_kv_sessions.append(js["Users"][str(id)]['chatid'])
    for id in js["Users"]:
        if js["Users"][str(id)]['settings'][1] == '5':
            list_skins.append(js["Users"][str(id)]['chatid'])
    for id in js["Users"]:
        if js["Users"][str(id)]['settings'][1] == '6':
            list_other.append(js["Users"][str(id)]['chatid'])
    for id in js["Users"]:
        if js["Users"][str(id)]['settings'][1] == '7':
            list_rup.append(js["Users"][str(id)]['chatid'])
    for id in js["Users"]:
        if js["Users"][str(id)]['settings'][1] == '1':
            list_all.append(js["Users"][str(id)]['chatid'])
            list_bal.append(js["Users"][str(id)]['chatid'])
            list_main.append(js["Users"][str(id)]['chatid'])
            list_kv_sessions.append(js["Users"][str(id)]['chatid'])
            list_skins.append(js["Users"][str(id)]['chatid'])
            list_other.append(js["Users"][str(id)]['chatid'])
            list_rup.append(js["Users"][str(id)]['chatid'])





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
    item1 = types.InlineKeyboardButton(text="Все", callback_data='all') #1
    item2 = types.InlineKeyboardButton(text='Балансеры', callback_data='bal') #2
    item3 = types.InlineKeyboardButton(text="Главные в EXBO", callback_data='main') #3
    item4 = types.InlineKeyboardButton(text="КВ и сессии", callback_data='kv_sessions') #4
    item5 = types.InlineKeyboardButton(text="Краски/скины/анимации/звуки", callback_data='skins') #5
    item6 = types.InlineKeyboardButton(text="другие", callback_data='other') #6
    item7 = types.InlineKeyboardButton(text="рупоры", callback_data='rupor') #7
    item8 = types.InlineKeyboardButton(text="сбросить", callback_data='clear')

    markup.add(item1, item2, item3,item4, item5, item6, item7, item8)
    bot.send_message(user_id, "Выберите разработчиков какой категории вы будете отслеживать", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    markup = telebot.types.ReplyKeyboardRemove()
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
                bot.send_message(call.message.chat.id, 'Запомню: ты выбрал подписку на балансеров', reply_markup=markup)
    elif call.data == "main":
        for id in js["Users"]:
            if js["Users"][id]['chatid'] == call.message.chat.id:
                # Получаем текущие настройки
                current_settings = js["Users"][id]['settings']

                # Изменяем второй символ
                new_settings = current_settings[:1] + '3' + current_settings[2:]

                # Обновляем значение в словаре
                js["Users"][id]['settings'] = new_settings

                save()  # Сохраните изменения
                bot.send_message(call.message.chat.id, 'Запомню: ты выбрал подписку на главных в эксбо', reply_markup=markup)
    elif call.data == "kv_sessions":
        for id in js["Users"]:
            if js["Users"][id]['chatid'] == call.message.chat.id:
                # Получаем текущие настройки
                current_settings = js["Users"][id]['settings']

                # Изменяем второй символ
                new_settings = current_settings[:1] + '4' + current_settings[2:]

                # Обновляем значение в словаре
                js["Users"][id]['settings'] = new_settings

                save()  # Сохраните изменения
                bot.send_message(call.message.chat.id, 'Запомню: ты выбрал подписку на разработчиков кв и сессионок', reply_markup=markup)
    elif call.data == "skins":
        for id in js["Users"]:
            if js["Users"][id]['chatid'] == call.message.chat.id:
                # Получаем текущие настройки
                current_settings = js["Users"][id]['settings']

                # Изменяем второй символ
                new_settings = current_settings[:1] + '5' + current_settings[2:]

                # Обновляем значение в словаре
                js["Users"][id]['settings'] = new_settings

                save()  # Сохраните изменения
                bot.send_message(call.message.chat.id, 'Запомню: ты выбрал подписку на разработчиков кв и сессионок', reply_markup=markup)
    elif call.data == "other":
        for id in js["Users"]:
            if js["Users"][id]['chatid'] == call.message.chat.id:
                # Получаем текущие настройки
                current_settings = js["Users"][id]['settings']

                # Изменяем второй символ
                new_settings = current_settings[:1] + '6' + current_settings[2:]

                # Обновляем значение в словаре
                js["Users"][id]['settings'] = new_settings

                save()  # Сохраните изменения
                bot.send_message(call.message.chat.id, 'Запомню: ты выбрал подписку на остальных разработчиков', reply_markup=markup)
    elif call.data == "rupor":
        for id in js["Users"]:
            if js["Users"][id]['chatid'] == call.message.chat.id:
                # Получаем текущие настройки
                current_settings = js["Users"][id]['settings']

                # Изменяем второй символ
                new_settings = current_settings[:1] + '4' + current_settings[2:]

                # Обновляем значение в словаре
                js["Users"][id]['settings'] = new_settings

                save()  # Сохраните изменения
                bot.send_message(call.message.chat.id, 'Запомню: ты выбрал подписку на рупоров', reply_markup=markup)
    elif call.data == "all":
        for id in js["Users"]:
            if js["Users"][id]['chatid'] == call.message.chat.id:
                # Получаем текущие настройки
                current_settings = js["Users"][id]['settings']

                # Изменяем второй символ
                new_settings = current_settings[:1] + '1' + current_settings[2:]

                # Обновляем значение в словаре
                js["Users"][id]['settings'] = new_settings

                save()  # Сохраните изменения
                bot.send_message(call.message.chat.id, 'Запомню: ты выбрал подписку на всех', reply_markup=markup)
    elif call.data == "clear":
        for id in js["Users"]:
            if js["Users"][id]['chatid'] == call.message.chat.id:
                # Получаем текущие настройки
                current_settings = js["Users"][id]['settings']

                # Изменяем второй символ
                new_settings = current_settings[:1] + '0' + current_settings[2:]

                # Обновляем значение в словаре
                js["Users"][id]['settings'] = new_settings

                save()  # Сохраните изменения
                bot.send_message(call.message.chat.id, 'Ты сбросил настройки', reply_markup=markup)
    telebot.types.ReplyKeyboardRemove()


def returnwhileforum(list_r, list_raz):
    for name in list_r:  # Изменено: используем имя вместо индекса
        print(1)
        print(name)
        new_messages = forum_mes([name])
        if new_messages:
            print(2)
            for message in new_messages:  # отправка всех полученных сообщений по очереди
                print(3)

                # Проверяем, является ли message кортежем
                if isinstance(message, tuple):
                    # Извлекаем строку из кортежа
                    clean_message = message[0]  # Предполагаем, что нужная строка находится в первом элементе кортежа
                else:
                    clean_message = message

                # Убираем символы новой строки
                clean_message = clean_message.replace(r'\n', '\n')  # Заменяем \n на /n
                print(clean_message)

                try:
                    print(4)
                    for j in list_raz:
                        print(j)
                        bot.send_message(j, f"Новое сообщение от {name}: \n{clean_message} \n ссылка на сообщение: {message[1]}")
                        print(5)
                except Exception as e:
                    print(f"Ошибка при отправке сообщения: {e}")  # Выводим ошибку для отладки


print(list_rup, list_bal, list_all)


def whileForum():
    stop = False
    balansers = ['zubzalinaza', 'Furgon', 'Acidragon', 'Boreus']
    rupers = ['Hreddd', 'Slyshashchii', 'normist', 'Prizrak132', 'ThaneST']
    skin_zvuk = ['Plastinka', 'grin_d']
    main = ['ZIV', 'RomeO', 'Folken', 'Gorlyli', 'Kazugaia', '__NightSkill__', 'USEC', 'moonshy5', 'Gorodskovich']
    sessionki = ['Kommynist', 'WWtddw']
    other_raz =  ['RedShark', '6eximmortal', 'Erildorian']



    while not stop:
        returnwhileforum(balansers, list_bal)
        returnwhileforum(main, list_main)
        returnwhileforum(sessionki, list_kv_sessions)
        returnwhileforum(skin_zvuk, list_skins)
        returnwhileforum(other_raz, list_other)
        returnwhileforum(rupers, list_rup)
        botstart()




# Запуск фонового потока
thread = threading.Thread(target=whileForum)
thread.daemon = True
thread.start()

print('bot start')
bot.polling(none_stop=True, interval=0)
print('bot stop')