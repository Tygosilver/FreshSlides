# -*- coding: utf-8 -*-
import telebot
from telebot import types
import sqlite3 as sq
import os


bot = telebot.TeleBot('7328072519:AAG_ApmO9-TQtq1d_qMgA_ua5vOpBi2X6HY')

@bot.message_handler(commands=['start'])
def startcom(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()


    cur.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, name varchar(100), tg_id varchar(500), flag_zakaz int default 0, chatid int)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS workers (user_id INTEGER PRIMARY KEY, name varchar(100), tg_id varchar(500), tg_id_ispoln varchar(500) default ".", typeispoln varchar(100), theme varchar(1000))')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS prezi (id INTEGER PRIMARY KEY, tg_id varchar(500), count int, theme varchar(1000), date varchar(100), taken int default 0)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS dokl (id INTEGER PRIMARY KEY, tg_id varchar(500), count int, theme varchar(1000), date varchar(100), taken int default 0)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS izodokl (id INTEGER PRIMARY KEY, tg_id varchar(500), count int, theme varchar(1000), date varchar(100), taken int default 0)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS prezidokl (id INTEGER PRIMARY KEY, tg_id varchar(500), count_list int, count_slide int, theme varchar(1000), date varchar(100), taken int default 0)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS proj (id INTEGER PRIMARY KEY, tg_id varchar(500), theme varchar(1000), flag_product int, date varchar(100), taken int default 0)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS recen (id INTEGER PRIMARY KEY, tg_id varchar(500), theme varchar(1000), date varchar(100), taken int default 0)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS flai (id INTEGER PRIMARY KEY, tg_id varchar(500), theme varchar(1000), date varchar(100), taken int default 0)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, tg_id varchar(500), theme varchar(1000), taken int default 0)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS stix (id INTEGER PRIMARY KEY, tg_id varchar(500), taken int default 0)')
    conn.commit()
    cur.execute('CREATE TABLE IF NOT EXISTS rassilka (user_id INTEGER PRIMARY KEY, name varchar(100), tg_id varchar(500))')
    conn.commit()

    username = '@' + message.from_user.username
    tg_id = message.from_user.id
    cur.execute('SELECT name FROM users')
    useri = cur.fetchall()
    flag_name = 1
    for user in useri:
        if user[0] == username:
            flag_name = 0
           # cur.execute('INSERT INTO users (name, tg_id) VALUES ("%s","%s")' % (username, tg_id))
           # conn.commit()
    print('user ', message.from_user.username, message.from_user.id)
    if flag_name == 1:
        cur.execute('INSERT INTO users (name, tg_id, chatid) VALUES ("%s","%s", "%d")' % (username, tg_id, message.chat.id))
        conn.commit()
    #print(useri)
    #print(tg_id, username)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    infoBTN = types.KeyboardButton('Информация о нас')
    workBTN = types.KeyboardButton('Заказать работу')
    speakBTN = types.KeyboardButton('Поговорить со своим исполнителем')
    markup.row(infoBTN, workBTN, speakBTN)
    bot.send_message(message.chat.id, 'Выберете нужную категорию', reply_markup=markup)
    cur.close()
    conn.close()
    #if message.text == 'Заказать работу.':

@bot.message_handler(commands=['worker'])
def worker_sign(message):
    bot.send_message(message.chat.id, 'Введите пароль для панели работника')
    bot.register_next_step_handler(message, worker_password)

@bot.message_handler(content_types=['text'])
def menu_info(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()

    if message.chat.type == 'private':
        if message.text == 'Условия сотрудничества и детали оплаты':
            bot.send_message(message.chat.id, '* Вы вносите предоплату 30%\n* Мы направляем результаты работы с водяными знаками\n* Слушаем Ваши правки один раз и исправляем работу\n* Мы направляем исправленную работу с водяными знаками\n* Мы принимаем полную оплату от Вас')
        elif message.text == 'Языки, которыми мы владеем':
            bot.send_message(message.chat.id, 'Русский, Английский, Китайский, Белорусский, Киргизский, Французский (начальный), Итальянский (начальный)')
        elif message.text == 'Скидки и акции':
            bot.send_message(message.chat.id, 'Скидка 5% за отзыв, который Вы разрешите нам опубликовать; Скидка 10% за публикацию в соц.сети с ссылкой на бота (соц.сети: телеграмм (телеграмм-канал или общий чат с друзьями/коллегами/одноклассниками), инстаграм (история))')
        elif message.text == 'Низкие цены':
            bot.send_message(message.chat.id, 'Объем и сложность работы невысоки, низкие требования к антиплагиату, простой дизайн, информационное содержание')
        elif message.text == 'Средние цены':
            bot.send_message(message.chat.id, 'Цена зависит от объема и сроков, от 100р/слайд и 250/р лист А4 текста. дизайн усложненный, интересный, можно с анимацией, высокая степень оригинальности текста')
        elif message.text == 'Высокие цены':
            bot.send_message(message.chat.id, 'Бизнес-презентации и курсовые/кандидатские работы. цена договорная')
        elif message.text == 'Расценки':
            bot.send_message(message.chat.id, 'Текстовой доклад стандарт 250р/лист А4 (титульный бесплатно)\n* Доклад с изображениями 300р/лист А4 (титульный бесплатно)\n* Презентация по готовому тексту 100р/1 слайд (титульный считается)\n* Доклад + презентация под ключ 100р/слайд + 250р/лист А4\n* Школьный проект под ключ (т.е. по правилам) 6500р - без продукта; 7500р/с продуктом\n* Брошюры, флаеры 1000р/штука\n* Меню 10.000р тут добавка')
        elif message.text == 'Цены на работы':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            lowBTN = types.KeyboardButton('Низкие цены')
            midleBTN = types.KeyboardButton('Средние цены')
            highBTN = types.KeyboardButton('Высокие цены')
            moduleBTN = types.KeyboardButton('Расценки')
            menuBTN = types.KeyboardButton('Вернуться в меню')
            markup.row(lowBTN, midleBTN)
            markup.row(highBTN, moduleBTN)
            markup.row(menuBTN)
            bot.send_message(message.chat.id, 'Выберете нужную категорию цен', reply_markup=markup)
        elif message.text == 'Примеры работ':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            prezBTN = types.KeyboardButton('Презентации')
            textBTN = types.KeyboardButton('Тексты')
            projBTN = types.KeyboardButton('Школьные проекты')
            flaiBTN = types.KeyboardButton('Брошюры и флаеры')
            menuBTN = types.KeyboardButton('Вернуться в меню')
            markup.row(prezBTN, textBTN)
            markup.row(projBTN, flaiBTN)
            markup.row(menuBTN)
            bot.send_message(message.chat.id, 'Примеры каких работ вы хотели бы увидеть', reply_markup=markup)
        elif message.text == 'Информация о нас':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            priceBTN = types.KeyboardButton('Цены на работы')
            detailsBTN = types.KeyboardButton('Условия сотрудничества и детали оплаты')
            examBTN = types.KeyboardButton('Примеры работ')
            langBTN = types.KeyboardButton('Языки, которыми мы владеем')
            discBTN = types.KeyboardButton('Скидки и акции')
            callBTN = types.KeyboardButton('Отзывы')
            menuBTN = types.KeyboardButton('Вернуться в меню')
            markup.row(priceBTN, detailsBTN)
            markup.row(examBTN, callBTN)
            markup.row(langBTN, discBTN)
            markup.row(menuBTN)
            bot.send_message(message.chat.id, 'Какая информация именно вас интересует?', reply_markup=markup)
        elif message.text == 'Вернуться в меню':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            infoBTN = types.KeyboardButton('Информация о нас')
            workBTN = types.KeyboardButton('Заказать работу')
            speakBTN = types.KeyboardButton('Поговорить со своим исполнителем')
            markup.row(infoBTN, workBTN, speakBTN)
            bot.send_message(message.chat.id, 'Выберете нужную категорию', reply_markup=markup)

        elif message.text == 'Заказать работу':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            prezBTN = types.KeyboardButton('Презентация')
            doklBTN = types.KeyboardButton('Доклад')
            izodoklBTN = types.KeyboardButton('Доклад с изображениями')
            doklprezBTN = types.KeyboardButton('Презентация + Доклад')
            projBTN = types.KeyboardButton('Школьный проект')
            recenBTN = types.KeyboardButton('Рецензия/Сочинение')
            flaiBTN = types.KeyboardButton('Флаеры/Ваучеры/Брошюры')
            cardBTN = types.KeyboardButton('Карточка товара')
            stixBTN = types.KeyboardButton('Стихотворение/Текст Песни')
            menuBTN = types.KeyboardButton('Вернуться в меню')
            markup.row(prezBTN, doklBTN, izodoklBTN)
            markup.row(doklprezBTN, projBTN, recenBTN)
            markup.row(cardBTN, stixBTN, flaiBTN)
            markup.row(menuBTN)
            bot.send_message(message.chat.id, 'Какую работу вы хотели бы заказать?', reply_markup=markup)

        elif message.text == 'Презентация':
            tg_id = message.from_user.id
            cur.execute('SELECT tg_id FROM prezi')
            ids = cur.fetchall()
            flag_id = 1
            for idi in ids:
                if int(idi[0]) == tg_id:
                    flag_id = 0
            if flag_id == 1:
                cur.execute('INSERT INTO prezi (tg_id) VALUES ("%s")' % (tg_id))
                conn.commit()
            cur.execute('UPDATE users SET flag_zakaz = "%d" WHERE tg_id = "%s"' % (1, message.from_user.id))
            conn.commit()
            bot.send_message(message.chat.id, 'Cколько примерно слайдов у вас будет? (ответьте в сообщении)')
            bot.register_next_step_handler(message, prez_count)
        elif message.text == 'Доклад':
            tg_id = message.from_user.id
            cur.execute('SELECT tg_id FROM dokl')
            ids = cur.fetchall()
            flag_id = 1
            for idi in ids:
                if int(idi[0]) == tg_id:
                    flag_id = 0
            if flag_id == 1:
                cur.execute('INSERT INTO dokl (tg_id) VALUES ("%s")' % (tg_id))
                conn.commit()
            cur.execute('UPDATE users SET flag_zakaz = "%d" WHERE tg_id = "%s"' % (1, message.from_user.id))
            conn.commit()
            bot.send_message(message.chat.id, 'Сколько примерно листов А4 будет в вашем докладе? (ответьте в сообщении)')
            bot.register_next_step_handler(message, dokl_count)
        elif message.text == 'Доклад с изображениями':
            tg_id = message.from_user.id
            cur.execute('SELECT tg_id FROM izodokl')
            ids = cur.fetchall()
            flag_id = 1
            for idi in ids:
                if int(idi[0]) == tg_id:
                    flag_id = 0
            if flag_id == 1:
                cur.execute('INSERT INTO izodokl (tg_id) VALUES ("%s")' % (tg_id))
                conn.commit()
            cur.execute('UPDATE users SET flag_zakaz = "%d" WHERE tg_id = "%s"' % (1, message.from_user.id))
            conn.commit()
            bot.send_message(message.chat.id, 'Сколько примерно листов А4 будет в вашем докладе? (ответьте в сообщении)')
            bot.register_next_step_handler(message, izodokl_count)
        elif message.text == 'Презентация + Доклад':
            tg_id = message.from_user.id
            cur.execute('SELECT tg_id FROM prezidokl')
            ids = cur.fetchall()
            flag_id = 1
            for idi in ids:
                if int(idi[0]) == tg_id:
                    flag_id = 0
            if flag_id == 1:
                cur.execute('INSERT INTO prezidokl (tg_id) VALUES ("%s")' % (tg_id))
                conn.commit()
            cur.execute('UPDATE users SET flag_zakaz = "%d" WHERE tg_id = "%s"' % (1, message.from_user.id))
            conn.commit()
            bot.send_message(message.chat.id, 'Cколько примерно слайдов у вас будет? (ответьте в сообщении)')
            bot.register_next_step_handler(message, prezidokl_count1)
        elif message.text == 'Школьный проект':
            tg_id = message.from_user.id
            cur.execute('SELECT tg_id FROM proj')
            ids = cur.fetchall()
            flag_id = 1
            for idi in ids:
                if int(idi[0]) == tg_id:
                    flag_id = 0
            if flag_id == 1:
                cur.execute('INSERT INTO proj (tg_id) VALUES ("%s")' % (tg_id))
                conn.commit()
            cur.execute('UPDATE users SET flag_zakaz = "%d" WHERE tg_id = "%s"' % (1, message.from_user.id))
            conn.commit()
            bot.send_message(message.chat.id, 'Какова тема Вашего проекта? (ответьте в сообщении)')
            bot.register_next_step_handler(message, proj_theme)
        elif message.text == 'Рецензия/Сочинение':
            tg_id = message.from_user.id
            cur.execute('SELECT tg_id FROM recen')
            ids = cur.fetchall()
            flag_id = 1
            for idi in ids:
                if int(idi[0]) == tg_id:
                    flag_id = 0
            if flag_id == 1:
                cur.execute('INSERT INTO recen (tg_id) VALUES ("%s")' % (tg_id))
                conn.commit()
            cur.execute('UPDATE users SET flag_zakaz = "%d" WHERE tg_id = "%s"' % (1, message.from_user.id))
            conn.commit()
            bot.send_message(message.chat.id, 'Какова тема рецензии/сочинения?')
            bot.register_next_step_handler(message, recen_theme)
        elif message.text == 'Флаеры/Ваучеры/Брошюры':
            tg_id = message.from_user.id
            cur.execute('SELECT tg_id FROM flai')
            ids = cur.fetchall()
            flag_id = 1
            for idi in ids:
                if int(idi[0]) == tg_id:
                    flag_id = 0
            if flag_id == 1:
                cur.execute('INSERT INTO flai (tg_id) VALUES ("%s")' % (tg_id))
                conn.commit()
            cur.execute('UPDATE users SET flag_zakaz = "%d" WHERE tg_id = "%s"' % (1, message.from_user.id))
            conn.commit()
            bot.send_message(message.chat.id, 'Для какой категории услуг/продукта необходимо создать флаеры, ваучеры или брошюры?')
            bot.register_next_step_handler(message, flai_theme)
        elif message.text == 'Карточка товара':
            tg_id = message.from_user.id
            cur.execute('SELECT tg_id FROM card')
            ids = cur.fetchall()
            flag_id = 1
            for idi in ids:
                if int(idi[0]) == tg_id:
                    flag_id = 0
            if flag_id == 1:
                cur.execute('INSERT INTO card (tg_id) VALUES ("%s")' % (tg_id))
                conn.commit()
            cur.execute('UPDATE users SET flag_zakaz = "%d" WHERE tg_id = "%s"' % (1, message.from_user.id))
            conn.commit()
            bot.send_message(message.chat.id, 'Для какого товара необходимо создать карточку?')
            bot.register_next_step_handler(message, card_theme)
        elif message.text == 'Стихотворение/Текст Песни':
            tg_id = message.from_user.id
            cur.execute('SELECT tg_id FROM stix')
            ids = cur.fetchall()
            flag_id = 1
            for idi in ids:
                if int(idi[0]) == tg_id:
                    flag_id = 0
            if flag_id == 1:
                cur.execute('INSERT INTO stix (tg_id) VALUES ("%s")' % (tg_id))
                conn.commit()
            cur.execute('UPDATE users SET flag_zakaz = "%d" WHERE tg_id = "%s"' % (1, message.from_user.id))
            conn.commit()
            bot.send_message(message.chat.id, 'Добрый день! Спасибо, что обратились к нам. Ожидайте ответа исполнителя')
        elif message.text == 'Поговорить со своим исполнителем':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            tg_id_ispoln = message.from_user.id
            cur.execute('SELECT tg_id FROM workers')
            ids_worker = cur.fetchall()
            cur.execute('SELECT tg_id_ispoln FROM workers')
            ids_ispoln = cur.fetchall()
            cur.execute('SELECT typeispoln FROM workers')
            typess = cur.fetchall()
            cur.execute('SELECT theme FROM workers')
            themes = cur.fetchall()

            menuBTN = types.KeyboardButton('Вернуться в меню')
            markup.row(menuBTN)

            for i in range(len(ids_ispoln)):
                if int(ids_ispoln[i][0]) == int(tg_id_ispoln):
                    if typess[i][0] == 'prezi':
                        bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашей презентации: %s' % (ids_worker[i][0], themes[i][0]))
                    if typess[i][0] == 'dokl':
                        bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего доклада: %s' % (ids_worker[i][0], themes[i][0]))
                    if typess[i][0] == 'izodokl':
                        bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего доклада: %s' % (ids_worker[i][0], themes[i][0]))
                    if typess[i][0] == 'prezidokl':
                        bot.send_message(message.chat.id,'ID вашего заказа: %s\nТема вашей презентации и доклада: %s' % (ids_worker[i][0], themes[i][0]))
                    if typess[i][0] == 'proj':
                        bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего проекта: %s' % (ids_worker[i][0], themes[i][0]))
                    if typess[i][0] == 'recen':
                        bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашей рецензии: %s' % (ids_worker[i][0], themes[i][0]))
                    if typess[i][0] == 'flai':
                        bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего флаера: %s' % (ids_worker[i][0], themes[i][0]))
                    if typess[i][0] == 'card':
                        bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашей карточки: %s' % (ids_worker[i][0], themes[i][0]))
                    if typess[i][0] == 'stix':
                        bot.send_message(message.chat.id, 'ID вашего заказа: %s' % (ids_worker[i][0]))
            bot.send_message(message.chat.id, 'Введите ID заказа, с исполнителем которого хотите поговорить', reply_markup=markup)
            bot.register_next_step_handler(message, client_talk)


def client_talk(message):
    if message.text == 'Вернуться в меню':
        menu_info(message)
    else:
        worker_id = message.text
        try:
            test_worker = int(message.text)
        except:
            bot.send_message(message.chat.id, 'Некоректное значение')
            bot.register_next_step_handler(message, client_talk)
            return
        bot.send_message(message.chat.id, 'Можете начинать разговор!')
        bot.register_next_step_handler(message, client_speak, worker_id)

def client_speak(message, worker_id):
    if message.text == 'Вернуться в меню':
        return menu_info(message)
    bot.send_message(worker_id, 'Заказчик (ID заказа: %s) вам пишет:' %(message.chat.id))
    try:
        bot.send_message(worker_id, message.text)
    except:
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = ('D:/programs/Python/botTG/files/client/' + message.document.file_name)
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            file = open(src, 'rb')
            bot.send_document(worker_id, file)
            file.close()
            try:
                os.remove(src)
            except OSError as error:
                print(error)
        except:
            bot.send_message(message.chat.id, 'Некоректный текст')
    bot.register_next_step_handler(message, client_speak, worker_id)

def prez_count(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    if message.text == 'Вернуться в меню':
        menu_info(message)
        return
    try:
        count = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, prez_count)
        return

    cur.execute('UPDATE prezi SET count = "%d" WHERE tg_id = "%s"' % (count, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'Какая у вас тема презентации?')
    bot.register_next_step_handler(message, prez_theme)

def prez_theme(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    theme = message.text
    cur.execute('UPDATE prezi SET theme = "%s" WHERE tg_id = "%s"' % (theme, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'К какому числу и времени необходимо выполнить заказ? (формат: 01.01.1970)')
    bot.register_next_step_handler(message, prez_date)

def prez_date(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    date = message.text
    cur.execute('UPDATE prezi SET date = "%s" WHERE tg_id = "%s"' % (date, message.from_user.id))
    conn.commit()
    cur.execute('SELECT id FROM prezi WHERE tg_id = "%s"' % (message.from_user.id))
    ids = cur.fetchall()
    cur.execute('SELECT count FROM prezi WHERE tg_id = "%s"' % (message.from_user.id))
    counts = cur.fetchall()
    cur.execute('SELECT theme FROM prezi WHERE tg_id = "%s"' % (message.from_user.id))
    themes = cur.fetchall()
    cur.execute('SELECT date FROM prezi WHERE tg_id = "%s"' % (message.from_user.id))
    dates = cur.fetchall()
    cur.execute('SELECT tg_id FROM rassilka')
    ids_worker = cur.fetchall()
    for i in range(len(ids_worker)):
        bot.send_message(ids_worker[i][0], 'Новый заказ!\nПрезентация')
        bot.send_message(ids_worker[i][0], 'ID: %d\nКол-во Слайдов: %d\nТема презентации: %s\nДедлайн: %s' % (ids[0][0], counts[0][0], themes[0][0], dates[0][0]))

    bot.send_message(message.chat.id, 'Спасибо за ответ! Ожидайте ответа исполнителя ')



def dokl_count(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    if message.text == 'Вернуться в меню':
        menu_info(message)
        return
    try:
        count = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, dokl_count)
        return
    cur.execute('UPDATE dokl SET count = "%d" WHERE tg_id = "%s"' % (count, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'Какая у вас тема доклада?')
    bot.register_next_step_handler(message, dokl_theme)

def dokl_theme(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    theme = message.text
    cur.execute('UPDATE dokl SET theme = "%s" WHERE tg_id = "%s"' % (theme, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'К какому числу и времени необходимо выполнить заказ? (формат: 01.01.1970)')
    bot.register_next_step_handler(message, dokl_date)


def dokl_date(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    date = message.text
    cur.execute('UPDATE dokl SET date = "%s" WHERE tg_id = "%s"' % (date, message.from_user.id))
    conn.commit()

    cur.execute('SELECT id FROM dokl WHERE tg_id = "%s"' % (message.from_user.id))
    ids = cur.fetchall()
    cur.execute('SELECT count FROM dokl WHERE tg_id = "%s"' % (message.from_user.id))
    counts = cur.fetchall()
    cur.execute('SELECT theme FROM dokl WHERE tg_id = "%s"' % (message.from_user.id))
    themes = cur.fetchall()
    cur.execute('SELECT date FROM dokl WHERE tg_id = "%s"' % (message.from_user.id))
    dates = cur.fetchall()
    cur.execute('SELECT tg_id FROM rassilka')
    ids_worker = cur.fetchall()
    for i in range(len(ids_worker)):
        bot.send_message(ids_worker[i][0], 'Новый заказ!\nДоклад')
        bot.send_message(ids_worker[i][0]
                         , 'ID: %d\nКол-во Листов А4: %d\nТема доклада: %s\nДедлайн: %s' % (ids[0][0], counts[0][0], themes[0][0], dates[0][0]))

    bot.send_message(message.chat.id, 'Спасибо за ответ! Ожидайте ответа исполнителя ')



def prezidokl_count1(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    if message.text == 'Вернуться в меню':
        menu_info(message)
        return
    try:
        count = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, prezidokl_count1)
        return
    cur.execute('UPDATE prezidokl SET count_slide = "%d" WHERE tg_id = "%s"' % (count, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'Cколько примерно листов А4 будет в вашем докладе?')
    bot.register_next_step_handler(message, prezidokl_count2)

def prezidokl_count2(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    try:
        count = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, prezidokl_count2)
        return
    cur.execute('UPDATE prezidokl SET count_list = "%d" WHERE tg_id = "%s"' % (count, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'Какая у вас тема доклада с презентацией?')
    bot.register_next_step_handler(message, prezidokl_theme)

def prezidokl_theme(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    theme = message.text
    cur.execute('UPDATE prezidokl SET theme = "%s" WHERE tg_id = "%s"' % (theme, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'К какому числу и времени необходимо выполнить заказ? (формат: 01.01.1970)')
    bot.register_next_step_handler(message, prezidokl_date)


def prezidokl_date(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    date = message.text
    cur.execute('UPDATE prezidokl SET date = "%s" WHERE tg_id = "%s"' % (date, message.from_user.id))
    conn.commit()

    cur.execute('SELECT id FROM prezidokl WHERE tg_id = "%s"' % (message.from_user.id))
    ids = cur.fetchall()
    cur.execute('SELECT count_list FROM prezidokl WHERE tg_id = "%s"' % (message.from_user.id))
    counts1 = cur.fetchall()
    cur.execute('SELECT count_slide FROM prezidokl WHERE tg_id = "%s"' % (message.from_user.id))
    counts2 = cur.fetchall()
    cur.execute('SELECT theme FROM prezidokl WHERE tg_id = "%s"' % (message.from_user.id))
    themes = cur.fetchall()
    cur.execute('SELECT date FROM prezidokl WHERE tg_id = "%s"' % (message.from_user.id))
    dates = cur.fetchall()
    cur.execute('SELECT tg_id FROM rassilka')
    ids_worker = cur.fetchall()
    for i in range(len(ids_worker)):
        bot.send_message(ids_worker[i][0], 'Новый заказ!\nПрезентация + доклад')
        bot.send_message(ids_worker[i][0],'ID: %d\nКол-во Листов А4 в докладе: %d\nКол-во Слайдов: %d\nТема: %s\nДедлайн: %s' % (ids[0][0], counts1[0][0], counts2[0][0], themes[0][0], dates[0][0]))

    bot.send_message(message.chat.id, 'Спасибо за ответ! Ожидайте ответа исполнителя ')



def izodokl_count(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    if message.text == 'Вернуться в меню':
        menu_info(message)
        return
    try:
        count = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, izodokl_count)
        return
    cur.execute('UPDATE izodokl SET count = "%d" WHERE tg_id = "%s"' % (count, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'Какая у вас тема доклада?')
    bot.register_next_step_handler(message, izodokl_theme)

def izodokl_theme(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    theme = message.text
    cur.execute('UPDATE izodokl SET theme = "%s" WHERE tg_id = "%s"' % (theme, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'К какому числу и времени необходимо выполнить заказ? (формат: 01.01.1970)')
    bot.register_next_step_handler(message, izodokl_date)


def izodokl_date(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    date = message.text
    cur.execute('UPDATE izodokl SET date = "%s" WHERE tg_id = "%s"' % (date, message.from_user.id))
    conn.commit()

    cur.execute('SELECT id FROM izodokl WHERE tg_id = "%s"' % (message.from_user.id))
    ids = cur.fetchall()
    cur.execute('SELECT count FROM izodokl WHERE tg_id = "%s"' % (message.from_user.id))
    counts = cur.fetchall()
    cur.execute('SELECT theme FROM izodokl WHERE tg_id = "%s"' % (message.from_user.id))
    themes = cur.fetchall()
    cur.execute('SELECT date FROM izodokl WHERE tg_id = "%s"' % (message.from_user.id))
    dates = cur.fetchall()
    cur.execute('SELECT tg_id FROM rassilka')
    ids_worker = cur.fetchall()
    for i in range(len(ids_worker)):
        bot.send_message(ids_worker[i][0], 'Новый заказ!\nДоклад с изображениями')
        bot.send_message(ids_worker[i][0],  'ID: %d\nКол-во Листов А4: %d\nТема доклада: %s\nДедлайн: %s' % (ids[0][0], counts[0][0], themes[0][0], dates[0][0]))


    bot.send_message(message.chat.id, 'Спасибо за ответ! Ожидайте ответа исполнителя ')



def proj_theme(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    if message.text == 'Вернуться в меню':
        menu_info(message)
        return
    theme = message.text
    cur.execute('UPDATE proj SET theme = "%s" WHERE tg_id = "%s"' % (theme, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'Нужен ли вам продукт проекта? (Да/Нет)')
    bot.register_next_step_handler(message, proj_product)

def proj_product(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    flagtext = message.text
    flag = 0
    if flagtext.lower == 'нет':
        flag = 0
    else:
        flag = 1
    cur.execute('UPDATE proj SET flag_product = "%s" WHERE tg_id = "%s"' % (flag, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'К какому числу и времени необходимо выполнить заказ? (формат: 01.01.1970)')
    bot.register_next_step_handler(message, proj_date)

def proj_date(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    date = message.text
    cur.execute('UPDATE proj SET date = "%s" WHERE tg_id = "%s"' % (date, message.from_user.id))
    conn.commit()

    cur.execute('SELECT id FROM proj WHERE tg_id = "%s"' % (message.from_user.id))
    ids = cur.fetchall()
    cur.execute('SELECT flag_product FROM proj WHERE tg_id = "%s"' % (message.from_user.id))
    flags = cur.fetchall()
    cur.execute('SELECT theme FROM proj WHERE tg_id = "%s"' % (message.from_user.id))
    themes = cur.fetchall()
    cur.execute('SELECT date FROM proj WHERE tg_id = "%s"' % (message.from_user.id))
    dates = cur.fetchall()
    cur.execute('SELECT tg_id FROM rassilka')
    ids_worker = cur.fetchall()
    for i in range(len(ids_worker)):
        bot.send_message(ids_worker[i][0], 'Новый заказ!\nШкольный Проект')
        bot.send_message(ids_worker[i][0],'ID: %d\nНаличие продукта (1 - есть, 0 - нету): %d\nТема проекта: %s\nДедлайн: %s' % (ids[0][0], flags[0][0], themes[0][0], dates[0][0]))

    bot.send_message(message.chat.id, 'Спасибо за ответ! Ожидайте ответа исполнителя ')




def recen_theme(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    if message.text == 'Вернуться в меню':
        menu_info(message)
        return
    theme = message.text
    cur.execute('UPDATE recen SET theme = "%s" WHERE tg_id = "%s"' % (theme, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'К какому числу и времени необходимо выполнить заказ? (формат: 01.01.1970)')
    bot.register_next_step_handler(message, recen_date)

def recen_date(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    date = message.text
    cur.execute('UPDATE recen SET date = "%s" WHERE tg_id = "%s"' % (date, message.from_user.id))
    conn.commit()

    cur.execute('SELECT id FROM recen WHERE tg_id = "%s"' % (message.from_user.id))
    ids = cur.fetchall()
    cur.execute('SELECT theme FROM recen WHERE tg_id = "%s"' % (message.from_user.id))
    themes = cur.fetchall()
    cur.execute('SELECT date FROM recen WHERE tg_id = "%s"' % (message.from_user.id))
    dates = cur.fetchall()
    cur.execute('SELECT tg_id FROM rassilka')
    ids_worker = cur.fetchall()
    for i in range(len(ids_worker)):
        bot.send_message(ids_worker[i][0], 'Новый заказ!\nРецензия')
        bot.send_message(ids_worker[i][0],'ID: %d\nТема: %s\nДедлайн: %s' % (ids[0][0], themes[0][0], dates[0][0]))


    bot.send_message(message.chat.id, 'Спасибо за ответ! Ожидайте ответа исполнителя ')



def flai_theme(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    theme = message.text
    if message.text == 'Вернуться в меню':
        menu_info(message)
        return
    cur.execute('UPDATE flai SET theme = "%s" WHERE tg_id = "%s"' % (theme, message.from_user.id))
    conn.commit()
    bot.send_message(message.chat.id, 'К какому числу и времени необходимо выполнить заказ? (формат: 01.01.1970)')
    bot.register_next_step_handler(message, flai_date)

def flai_date(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    date = message.text
    cur.execute('UPDATE flai SET date = "%s" WHERE tg_id = "%s"' % (date, message.from_user.id))
    conn.commit()

    cur.execute('SELECT id FROM flai WHERE tg_id = "%s"' % (message.from_user.id))
    ids = cur.fetchall()
    cur.execute('SELECT theme FROM flai WHERE tg_id = "%s"' % (message.from_user.id))
    themes = cur.fetchall()
    cur.execute('SELECT date FROM flai WHERE tg_id = "%s"' % (message.from_user.id))
    dates = cur.fetchall()
    cur.execute('SELECT tg_id FROM rassilka')
    ids_worker = cur.fetchall()
    for i in range(len(ids_worker)):
        bot.send_message(ids_worker[i][0], 'Новый заказ!\nФлаер')
        bot.send_message(ids_worker[i][0],'ID: %d\nТема: %s\nДедлайн: %s' % (ids[0][0], themes[0][0], dates[0][0]))

    bot.send_message(message.chat.id, 'Спасибо за ответ! Ожидайте ответа исполнителя ')



def card_theme(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    theme = message.text
    cur.execute('UPDATE card SET theme = "%s" WHERE tg_id = "%s"' % (theme, message.from_user.id))
    conn.commit()

    cur.execute('SELECT id FROM card WHERE tg_id = "%s"' % (message.from_user.id))
    ids = cur.fetchall()
    cur.execute('SELECT theme FROM card WHERE tg_id = "%s"' % (message.from_user.id))
    themes = cur.fetchall()
    cur.execute('SELECT tg_id FROM rassilka')
    ids_worker = cur.fetchall()
    for i in range(len(ids_worker)):
        bot.send_message(ids_worker[i][0], 'Новый заказ!\nКарточка')
        bot.send_message(ids_worker[i][0], 'ID: %d\nТема: %s' % (ids[0][0], themes[0][0]))

    bot.send_message(message.chat.id, 'Спасибо за ответ! Ожидайте ответа исполнителя')




def worker_password(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    if message.text == 'password':
        cur.execute('SELECT tg_id FROM rassilka')
        ids_worker = cur.fetchall()
        flag = 0
        for i in range(len(ids_worker)):
            if int(ids_worker[i][0]) == int(message.from_user.id):
                flag = 1
        print('worker ', message.from_user.username, message.from_user.id)
        if flag == 0:
            cur.execute('INSERT INTO rassilka (name, tg_id) VALUES ("@%s", "%s")' % (message.from_user.username, message.from_user.id))
            conn.commit()
        worker_panel(message)
    else:
        bot.send_message(message.chat.id, 'Неверно!')

def worker_panel(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    checkBTN = types.KeyboardButton('Посмотреть все доступные заказы (ID. Вся информация о заказе)')
    takeBTN = types.KeyboardButton('Взять заказ')
    dialBTN = types.KeyboardButton('Перейти в диалог с заказчиком')
    menuBTN = types.KeyboardButton('Вернуться в меню работника')
    endBTN = types.KeyboardButton('Закрыть заказ')
    markup.row(checkBTN, takeBTN)
    markup.row(dialBTN, endBTN)
    markup.row(menuBTN)
    bot.send_message(message.chat.id, 'Добро пожаловать! Если вы хотите выйти из Рабочей панели пропишите /start', reply_markup=markup)
    bot.register_next_step_handler(message, worker_choice)

def worker_choice(message):
    if message.text == 'Взять заказ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        prezBTN = types.KeyboardButton('Презентация (работник)')
        doklBTN = types.KeyboardButton('Доклад (работник)')
        izodoklBTN = types.KeyboardButton('Доклад с изображениями (работник)')
        doklprezBTN = types.KeyboardButton('Презентация + Доклад (работник)')
        projBTN = types.KeyboardButton('Школьный проект (работник)')
        recenBTN = types.KeyboardButton('Рецензия/Сочинение (работник)')
        flaiBTN = types.KeyboardButton('Флаеры/Ваучеры/Брошюры (работник)')
        cardBTN = types.KeyboardButton('Карточка товара (работник)')
        stixBTN = types.KeyboardButton('Стихотворение/Текст Песни (работник)')
        menuBTN = types.KeyboardButton('Вернуться в меню работника')
        markup.row(prezBTN, doklBTN, izodoklBTN)
        markup.row(doklprezBTN, projBTN, recenBTN)
        markup.row(cardBTN, stixBTN, flaiBTN)
        markup.row(menuBTN)
        bot.send_message(message.chat.id, 'Выберите вид заказа который взять', reply_markup=markup)
        bot.register_next_step_handler(message, worker_type)
    elif message.text == 'Посмотреть все доступные заказы (ID. Вся информация о заказе)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        prezBTN = types.KeyboardButton('Презентация (работник)')
        doklBTN = types.KeyboardButton('Доклад (работник)')
        izodoklBTN = types.KeyboardButton('Доклад с изображениями (работник)')
        doklprezBTN = types.KeyboardButton('Презентация + Доклад (работник)')
        projBTN = types.KeyboardButton('Школьный проект (работник)')
        recenBTN = types.KeyboardButton('Рецензия/Сочинение (работник)')
        flaiBTN = types.KeyboardButton('Флаеры/Ваучеры/Брошюры (работник)')
        cardBTN = types.KeyboardButton('Карточка товара (работник)')
        stixBTN = types.KeyboardButton('Стихотворение/Текст Песни (работник)')
        menuBTN = types.KeyboardButton('Вернуться в меню работника')
        markup.row(prezBTN, doklBTN, izodoklBTN)
        markup.row(doklprezBTN, projBTN, recenBTN)
        markup.row(cardBTN, stixBTN, flaiBTN)
        markup.row(menuBTN)
        bot.send_message(message.chat.id, 'Выберите вид заказа который хотите посмотреть', reply_markup=markup)
        bot.register_next_step_handler(message, worker_zakazi)
    elif message.text == 'Перейти в диалог с заказчиком':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        conn = sq.connect('database.sql')
        cur = conn.cursor()
        tg_id = message.from_user.id
        cur.execute('SELECT tg_id FROM workers')
        ids_worker = cur.fetchall()
        cur.execute('SELECT tg_id_ispoln FROM workers')
        ids_ispoln = cur.fetchall()
        cur.execute('SELECT typeispoln FROM workers')
        typess = cur.fetchall()
        cur.execute('SELECT theme FROM workers')
        themes = cur.fetchall()

        menuBTN = types.KeyboardButton('Вернуться в меню работника')
        markup.row(menuBTN)

        for i in range(len(ids_worker)):
            if int(ids_worker[i][0]) == int(tg_id):
                if typess[i][0] == 'prezi':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашей презентации: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'dokl':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего доклада: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'izodokl':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего доклада: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'prezidokl':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашей презентации и доклада: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'proj':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего проекта: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'recen':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашей рецензии: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'flai':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего флаера: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'card':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашей карточки: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'stix':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s' % (ids_ispoln[i][0]))
        bot.send_message(message.chat.id, 'Введите ID заказа, с покупателем которого хотите поговорить, либо нажмите кнопку возврата в Меню', reply_markup=markup)
        bot.register_next_step_handler(message, worker_talk)
    elif message.text == 'Закрыть заказ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        conn = sq.connect('database.sql')
        cur = conn.cursor()
        tg_id = message.from_user.id
        cur.execute('SELECT tg_id FROM workers')
        ids_worker = cur.fetchall()
        cur.execute('SELECT tg_id_ispoln FROM workers')
        ids_ispoln = cur.fetchall()
        cur.execute('SELECT typeispoln FROM workers')
        typess = cur.fetchall()
        cur.execute('SELECT theme FROM workers')
        themes = cur.fetchall()

        menuBTN = types.KeyboardButton('Вернуться в меню работника')
        markup.row(menuBTN)

        for i in range(len(ids_worker)):
            if int(ids_worker[i][0]) == int(tg_id):
                if typess[i][0] == 'prezi':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашей презентации: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'dokl':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего доклада: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'izodokl':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего доклада: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'prezidokl':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашей презентации и доклада: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'proj':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего проекта: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'recen':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашей рецензии: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'flai':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашего флаера: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'card':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s\nТема вашей карточки: %s' % (ids_ispoln[i][0], themes[i][0]))
                if typess[i][0] == 'stix':
                    bot.send_message(message.chat.id, 'ID вашего заказа: %s' % (ids_ispoln[i][0]))
        bot.send_message(message.chat.id, 'Введите ID заказа, который хотите закрыть')
        bot.register_next_step_handler(message, end_zakaz)

    elif message.text == '/start':
        startcom(message)
    elif message.text == 'Вернуться в меню работника':
        worker_panel(message)


def worker_talk(message):
    if message.text == 'Вернуться в меню работника':
        worker_panel(message)
    else:
        client_id = message.text
        try:
            test_client = int(message.text)
        except:
            bot.send_message(message.chat.id, 'Неверный ID')
            bot.register_next_step_handler(message, worker_talk)
            return
        bot.send_message(message.chat.id, 'Можете начинать разговор')
        bot.register_next_step_handler(message, worker_speak, client_id)

def worker_speak(message, client_id):
    if message.text == 'Вернуться в меню работника':
        return worker_panel(message)
    bot.send_message(client_id, 'Исполнитель вам пишет:')
    try:
        bot.send_message(client_id, message.text)
    except:
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = ('D:/programs/Python/botTG/files/worker/' + message.document.file_name)
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            file = open(src, 'rb')
            bot.send_document(client_id, file)
            file.close()
            try:
                os.remove(src)
            except OSError as error:
                print(error)
        except:
            bot.send_message(message.chat.id, 'Некоректный текст')

    bot.register_next_step_handler(message, worker_speak, client_id)

def worker_type(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    if message.text == 'Презентация (работник)':
        bot.send_message(message.chat.id, 'Введите ID заказа')
        bot.register_next_step_handler(message, worker_prez)
    elif message.text == 'Доклад (работник)':
        bot.send_message(message.chat.id, 'Введите ID заказа')
        bot.register_next_step_handler(message, worker_dokl)
    elif message.text == 'Доклад с изображениями (работник)':
        bot.send_message(message.chat.id, 'Введите ID заказа')
        bot.register_next_step_handler(message, worker_izodokl)
    elif message.text == 'Презентация + Доклад (работник)':
        bot.send_message(message.chat.id, 'Введите ID заказа')
        bot.register_next_step_handler(message, worker_prezidokl)
    elif message.text == 'Школьный проект (работник)':
        bot.send_message(message.chat.id, 'Введите ID заказа')
        bot.register_next_step_handler(message, worker_proj)
    elif message.text == 'Рецензия/Сочинение (работник)':
        bot.send_message(message.chat.id, 'Введите ID заказа')
        bot.register_next_step_handler(message, worker_recen)
    elif message.text == 'Флаеры/Ваучеры/Брошюры (работник)':
        bot.send_message(message.chat.id, 'Введите ID заказа')
        bot.register_next_step_handler(message, worker_flai)
    elif message.text == 'Карточка товара (работник)':
        bot.send_message(message.chat.id, 'Введите ID заказа')
        bot.register_next_step_handler(message, worker_card)
    elif message.text == 'Стихотворение/Текст Песни (работник)':
        bot.send_message(message.chat.id, 'Введите ID заказа')
        bot.register_next_step_handler(message, worker_stix)
    elif message.text == 'Вернуться в меню работника':
        worker_panel(message)

def worker_prez(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    idwork = message.text
    try:
        testids = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, worker_prez)
        return
    cur.execute('SELECT id FROM prezi')
    ids = cur.fetchall()
    cur.execute('SELECT tg_id FROM prezi')
    tg_ids = cur.fetchall()
    cur.execute('SELECT theme FROM prezi')
    themes = cur.fetchall()

    menuBTN = types.KeyboardButton('Вернуться в меню работника')
    markup.row(menuBTN)

    for i in range(len(ids)):
        if ids[i][0] == int(idwork):
            cur.execute('INSERT INTO workers (name, tg_id, tg_id_ispoln, typeispoln, theme) VALUES ("@%s", "%s", "%s", "prezi", "%s")' % (message.from_user.username, message.from_user.id, tg_ids[i][0], themes[i][0]))
            conn.commit()
            cur.execute('UPDATE prezi SET taken = "1" WHERE id = "%s"' % (ids[i][0]))
            conn.commit()
    bot.send_message(message.chat.id, 'Чтобы вернуться обратно в меню, нажмите кнопку', reply_markup=markup)
    bot.register_next_step_handler(message, worker_panel)

def worker_dokl(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    idwork = message.text
    try:
        testids = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, worker_dokl)
        return
    cur.execute('SELECT id FROM dokl')
    ids = cur.fetchall()
    cur.execute('SELECT tg_id FROM dokl')
    tg_ids = cur.fetchall()
    cur.execute('SELECT theme FROM dokl')
    themes = cur.fetchall()

    menuBTN = types.KeyboardButton('Вернуться в меню работника')
    markup.row(menuBTN)

    for i in range(len(ids)):
        if ids[i][0] == int(idwork):
            cur.execute('INSERT INTO workers (name, tg_id, tg_id_ispoln, typeispoln, theme) VALUES ("@%s", "%s", "%s", "dokl", "%s")' % ( message.from_user.username, message.from_user.id, tg_ids[i][0], themes[i][0]))
            conn.commit()
            cur.execute('UPDATE dokl SET taken = "1" WHERE id = "%s"' % (ids[i][0]))
            conn.commit()
    bot.send_message(message.chat.id, 'Чтобы вернуться обратно в меню, нажмите кнопку', reply_markup=markup)
    bot.register_next_step_handler(message, worker_panel)

def worker_izodokl(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    idwork = message.text
    try:
        testids = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, worker_izodokl)
        return
    cur.execute('SELECT id FROM izodokl')
    ids = cur.fetchall()
    cur.execute('SELECT tg_id FROM izodokl')
    tg_ids = cur.fetchall()
    cur.execute('SELECT theme FROM izodokl')
    themes = cur.fetchall()

    menuBTN = types.KeyboardButton('Вернуться в меню работника')
    markup.row(menuBTN)

    for i in range(len(ids)):
        if ids[i][0] == int(idwork):
            cur.execute('INSERT INTO workers (name, tg_id, tg_id_ispoln, typeispoln, theme) VALUES ("@%s", "%s", "%s", "izodokl", "%s")' % (message.from_user.username, message.from_user.id, tg_ids[i][0], themes[i][0]))
            conn.commit()
            cur.execute('UPDATE izodokl SET taken = "1" WHERE id = "%s"' % (ids[i][0]))
            conn.commit()
    bot.send_message(message.chat.id, 'Чтобы вернуться обратно в меню, нажмите кнопку', reply_markup=markup)
    bot.register_next_step_handler(message, worker_panel)

def worker_prezidokl(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    idwork = message.text
    try:
        testids = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, worker_prezidokl)
        return
    cur.execute('SELECT id FROM prezidokl')
    ids = cur.fetchall()
    cur.execute('SELECT tg_id FROM prezidokl')
    tg_ids = cur.fetchall()
    cur.execute('SELECT theme FROM prezidokl')
    themes = cur.fetchall()

    menuBTN = types.KeyboardButton('Вернуться в меню работника')
    markup.row(menuBTN)

    for i in range(len(ids)):
        if ids[i][0] == int(idwork):
            cur.execute('INSERT INTO workers (name, tg_id, tg_id_ispoln, typeispoln, theme) VALUES ("@%s", "%s", "%s", "prezidokl", "%s")' % (message.from_user.username, message.from_user.id, tg_ids[i][0], themes[i][0]))
            conn.commit()
            cur.execute('UPDATE prezidokl SET taken = "1" WHERE id = "%s"' % (ids[i][0]))
            conn.commit()
    bot.send_message(message.chat.id, 'Чтобы вернуться обратно в меню, нажмите кнопку', reply_markup=markup)
    bot.register_next_step_handler(message, worker_panel)

def worker_proj(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    idwork = message.text
    try:
        testids = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, worker_proj)
        return
    cur.execute('SELECT id FROM proj')
    ids = cur.fetchall()
    cur.execute('SELECT tg_id FROM proj')
    tg_ids = cur.fetchall()
    cur.execute('SELECT theme FROM proj')
    themes = cur.fetchall()

    menuBTN = types.KeyboardButton('Вернуться в меню работника')
    markup.row(menuBTN)

    for i in range(len(ids)):
        if ids[i][0] == int(idwork):
            cur.execute('INSERT INTO workers (name, tg_id, tg_id_ispoln, typeispoln, theme) VALUES ("@%s", "%s", "%s", "proj", "%s")' % (message.from_user.username, message.from_user.id, tg_ids[i][0], themes[i][0]))
            conn.commit()
            cur.execute('UPDATE proj SET taken = "1" WHERE id = "%s"' % (ids[i][0]))
            conn.commit()
    bot.send_message(message.chat.id, 'Чтобы вернуться обратно в меню, нажмите кнопку', reply_markup=markup)
    bot.register_next_step_handler(message, worker_panel)

def worker_recen(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    idwork = message.text
    try:
        testids = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, worker_recen)
        return
    cur.execute('SELECT id FROM recen')
    ids = cur.fetchall()
    cur.execute('SELECT tg_id FROM recen')
    tg_ids = cur.fetchall()
    cur.execute('SELECT theme FROM recen')
    themes = cur.fetchall()

    menuBTN = types.KeyboardButton('Вернуться в меню работника')
    markup.row(menuBTN)

    for i in range(len(ids)):
        if ids[i][0] == int(idwork):
            cur.execute('INSERT INTO workers (name, tg_id, tg_id_ispoln, typeispoln, theme) VALUES ("@%s", "%s", "%s", "recen", "%s")' % (message.from_user.username, message.from_user.id, tg_ids[i][0], themes[i][0]))
            conn.commit()
            cur.execute('UPDATE recen SET taken = "1" WHERE id = "%s"' % (ids[i][0]))
            conn.commit()
    bot.send_message(message.chat.id, 'Чтобы вернуться обратно в меню, нажмите кнопку', reply_markup=markup)
    bot.register_next_step_handler(message, worker_panel)

def worker_flai(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    idwork = message.text
    try:
        testids = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, worker_flai)
        return
    cur.execute('SELECT id FROM flai')
    ids = cur.fetchall()
    cur.execute('SELECT tg_id FROM flai')
    tg_ids = cur.fetchall()
    cur.execute('SELECT theme FROM flai')
    themes = cur.fetchall()

    menuBTN = types.KeyboardButton('Вернуться в меню работника')
    markup.row(menuBTN)

    for i in range(len(ids)):
        if ids[i][0] == int(idwork):
            cur.execute('INSERT INTO workers (name, tg_id, tg_id_ispoln, typeispoln, theme) VALUES ("@%s", "%s", "%s", "flai", "%s")' % (message.from_user.username, message.from_user.id, tg_ids[i][0], themes[i][0]))
            conn.commit()
            cur.execute('UPDATE flai SET taken = "1" WHERE id = "%s"' % (ids[i][0]))
            conn.commit()
    bot.send_message(message.chat.id, 'Чтобы вернуться обратно в меню, нажмите кнопку', reply_markup=markup)
    bot.register_next_step_handler(message, worker_panel)

def worker_card(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    idwork = message.text
    try:
        testids = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, worker_card)
        return
    cur.execute('SELECT id FROM card')
    ids = cur.fetchall()
    cur.execute('SELECT tg_id FROM card')
    tg_ids = cur.fetchall()
    cur.execute('SELECT theme FROM card')
    themes = cur.fetchall()

    menuBTN = types.KeyboardButton('Вернуться в меню работника')
    markup.row(menuBTN)

    for i in range(len(ids)):
        if ids[i][0] == int(idwork):
            cur.execute('INSERT INTO workers (name, tg_id, tg_id_ispoln, typeispoln, theme) VALUES ("@%s", "%s", "%s", "card", "%s")' % (message.from_user.username, message.from_user.id, tg_ids[i][0], themes[i][0]))
            conn.commit()
            cur.execute('UPDATE card SET taken = "1" WHERE id = "%s"' % (ids[i][0]))
            conn.commit()
    bot.send_message(message.chat.id, 'Чтобы вернуться обратно в меню, нажмите кнопку', reply_markup=markup)
    bot.register_next_step_handler(message, worker_panel)

def worker_stix(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    idwork = message.text
    try:
        testids = int(message.text)
    except:
        bot.send_message(message.chat.id, 'Некоректное значение')
        bot.register_next_step_handler(message, worker_stix)
        return
    cur.execute('SELECT id FROM stix')
    ids = cur.fetchall()
    cur.execute('SELECT tg_id FROM stix')
    tg_ids = cur.fetchall()

    menuBTN = types.KeyboardButton('Вернуться в меню работника')
    markup.row(menuBTN)

    for i in range(len(ids)):
        if ids[i][0] == int(idwork):
            cur.execute('INSERT INTO workers (name, tg_id, tg_id_ispoln, typeispoln) VALUES ("@%s", "%s", "%s", "stix")' % (message.from_user.username, message.from_user.id, tg_ids[i][0]))
            conn.commit()
            cur.execute('UPDATE stix SET taken = "1" WHERE id = "%s"' % (ids[i][0]))
            conn.commit()
    bot.send_message(message.chat.id, 'Чтобы вернуться обратно в меню, нажмите кнопку', reply_markup=markup)
    bot.register_next_step_handler(message, worker_panel)

def worker_zakazi(message):
    conn = sq.connect('database.sql')
    cur = conn.cursor()
    if message.text == 'Презентация (работник)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        checkBTN = types.KeyboardButton('Посмотреть все доступные заказы (ID. Вся информация о заказе)')
        markup.row(checkBTN)
        cur.execute('SELECT id FROM prezi')
        ids = cur.fetchall()
        cur.execute('SELECT count FROM prezi')
        counts = cur.fetchall()
        cur.execute('SELECT theme FROM prezi')
        themes = cur.fetchall()
        cur.execute('SELECT date FROM prezi')
        dates = cur.fetchall()
        cur.execute('SELECT taken FROM prezi')
        taken = cur.fetchall()
        for i in range(len(ids)):
            if int(taken[i][0]) == 0:
                bot.send_message(message.chat.id, 'ID: %d\nКол-во Слайдов: %d\nТема презентации: %s\nДедлайн: %s' % (ids[i][0], counts[i][0], themes[i][0], dates[i][0]))
        bot.send_message(message.chat.id, 'Нажмите кнопку чтобы вернуться к информации о заказах', reply_markup=markup)
        bot.register_next_step_handler(message, worker_choice)
    elif message.text == 'Доклад (работник)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        checkBTN = types.KeyboardButton('Посмотреть все доступные заказы (ID. Вся информация о заказе)')
        markup.row(checkBTN)
        cur.execute('SELECT id FROM dokl')
        ids = cur.fetchall()
        cur.execute('SELECT count FROM dokl')
        counts = cur.fetchall()
        cur.execute('SELECT theme FROM dokl')
        themes = cur.fetchall()
        cur.execute('SELECT date FROM dokl')
        dates = cur.fetchall()
        cur.execute('SELECT taken FROM dokl')
        taken = cur.fetchall()
        for i in range(len(ids)):
            if int(taken[i][0]) == 0:
                bot.send_message(message.chat.id, 'ID: %d\nКол-во Листов А4: %d\nТема доклада: %s\nДедлайн: %s' % (ids[i][0], counts[i][0], themes[i][0], dates[i][0]))
        bot.send_message(message.chat.id, 'Нажмите кнопку чтобы вернуться к информации о заказах', reply_markup=markup)
        bot.register_next_step_handler(message, worker_choice)
    elif message.text == 'Доклад с изображениями (работник)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        checkBTN = types.KeyboardButton('Посмотреть все доступные заказы (ID. Вся информация о заказе)')
        markup.row(checkBTN)
        cur.execute('SELECT id FROM izodokl')
        ids = cur.fetchall()
        cur.execute('SELECT count FROM izodokl')
        counts = cur.fetchall()
        cur.execute('SELECT theme FROM izodokl')
        themes = cur.fetchall()
        cur.execute('SELECT date FROM izodokl')
        dates = cur.fetchall()
        cur.execute('SELECT taken FROM izodokl')
        taken = cur.fetchall()
        for i in range(len(ids)):
            if int(taken[i][0]) == 0:
                bot.send_message(message.chat.id, 'ID: %d\nКол-во Листов А4: %d\nТема доклада: %s\nДедлайн: %s' % (ids[i][0], counts[i][0], themes[i][0], dates[i][0]))
        bot.send_message(message.chat.id, 'Нажмите кнопку чтобы вернуться к информации о заказах',reply_markup=markup)
        bot.register_next_step_handler(message, worker_choice)
    elif message.text == 'Презентация + Доклад (работник)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        checkBTN = types.KeyboardButton('Посмотреть все доступные заказы (ID. Вся информация о заказе)')
        markup.row(checkBTN)
        cur.execute('SELECT id FROM prezidokl')
        ids = cur.fetchall()
        cur.execute('SELECT count_list FROM prezidokl')
        counts1 = cur.fetchall()
        cur.execute('SELECT count_slide FROM prezidokl')
        counts2 = cur.fetchall()
        cur.execute('SELECT theme FROM prezidokl')
        themes = cur.fetchall()
        cur.execute('SELECT date FROM prezidokl')
        dates = cur.fetchall()
        cur.execute('SELECT taken FROM prezidokl')
        taken = cur.fetchall()
        for i in range(len(ids)):
            if int(taken[i][0]) == 0:
                bot.send_message(message.chat.id, 'ID: %d\nКол-во Листов А4 в докладе: %d\nКол-во Слайдов: %d\nТема: %s\nДедлайн: %s' % (ids[i][0], counts1[i][0], counts2[i][0], themes[i][0], dates[i][0]))
        bot.send_message(message.chat.id, 'Нажмите кнопку чтобы вернуться к информации о заказах', reply_markup=markup)
        bot.register_next_step_handler(message, worker_choice)
    elif message.text == 'Школьный проект (работник)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        checkBTN = types.KeyboardButton('Посмотреть все доступные заказы (ID. Вся информация о заказе)')
        markup.row(checkBTN)
        cur.execute('SELECT id FROM proj')
        ids = cur.fetchall()
        cur.execute('SELECT flag_product FROM proj')
        flags = cur.fetchall()
        cur.execute('SELECT theme FROM proj')
        themes = cur.fetchall()
        cur.execute('SELECT date FROM proj')
        dates = cur.fetchall()
        cur.execute('SELECT taken FROM proj')
        taken = cur.fetchall()
        for i in range(len(ids)):
            if int(taken[i][0]) == 0:
                bot.send_message(message.chat.id, 'ID: %d\nНаличие продукта (1 - есть, 0 - нету): %d\nТема проекта: %s\nДедлайн: %s' % (ids[i][0], flags[i][0], themes[i][0], dates[i][0]))
        bot.send_message(message.chat.id, 'Нажмите кнопку чтобы вернуться к информации о заказах', reply_markup=markup)
        bot.register_next_step_handler(message, worker_choice)
    elif message.text == 'Рецензия/Сочинение (работник)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        checkBTN = types.KeyboardButton('Посмотреть все доступные заказы (ID. Вся информация о заказе)')
        markup.row(checkBTN)
        cur.execute('SELECT id FROM recen')
        ids = cur.fetchall()
        cur.execute('SELECT theme FROM recen')
        themes = cur.fetchall()
        cur.execute('SELECT date FROM recen')
        dates = cur.fetchall()
        cur.execute('SELECT taken FROM recen')
        taken = cur.fetchall()
        for i in range(len(ids)):
            if int(taken[i][0]) == 0:
                bot.send_message(message.chat.id, 'ID: %d\nТема: %s\nДедлайн: %s' % (ids[i][0], themes[i][0], dates[i][0]))
        bot.send_message(message.chat.id, 'Нажмите кнопку чтобы вернуться к информации о заказах', reply_markup=markup)
        bot.register_next_step_handler(message, worker_choice)
    elif message.text == 'Флаеры/Ваучеры/Брошюры (работник)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        checkBTN = types.KeyboardButton('Посмотреть все доступные заказы (ID. Вся информация о заказе)')
        markup.row(checkBTN)
        cur.execute('SELECT id FROM flai')
        ids = cur.fetchall()
        cur.execute('SELECT theme FROM flai')
        themes = cur.fetchall()
        cur.execute('SELECT date FROM flai')
        dates = cur.fetchall()
        cur.execute('SELECT taken FROM flai')
        taken = cur.fetchall()
        for i in range(len(ids)):
            if int(taken[i][0]) == 0:
                bot.send_message(message.chat.id, 'ID: %d\nТема: %s\nДедлайн: %s' % (ids[i][0], themes[i][0], dates[i][0]))
        bot.send_message(message.chat.id, 'Нажмите кнопку чтобы вернуться к информации о заказах', reply_markup=markup)
        bot.register_next_step_handler(message, worker_choice)
    elif message.text == 'Карточка товара (работник)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        checkBTN = types.KeyboardButton('Посмотреть все доступные заказы (ID. Вся информация о заказе)')
        markup.row(checkBTN)
        cur.execute('SELECT id FROM card')
        ids = cur.fetchall()
        cur.execute('SELECT theme FROM card')
        themes = cur.fetchall()
        cur.execute('SELECT taken FROM card')
        taken = cur.fetchall()
        for i in range(len(ids)):
            if int(taken[i][0]) == 0:

                bot.send_message(message.chat.id, 'ID: %d\nТема: %s' % (ids[i][0], themes[i][0]))
        bot.send_message(message.chat.id, 'Нажмите кнопку чтобы вернуться к информации о заказах', reply_markup=markup)
        bot.register_next_step_handler(message, worker_choice)
    elif message.text == 'Стихотворение/Текст Песни (работник)':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        checkBTN = types.KeyboardButton('Посмотреть все доступные заказы (ID. Вся информация о заказе)')
        markup.row(checkBTN)
        cur.execute('SELECT id FROM stix')
        ids = cur.fetchall()
        cur.execute('SELECT taken FROM stix')
        taken = cur.fetchall()
        for i in range(len(ids)):
            if int(taken[i][0]) == 0:
                bot.send_message(message.chat.id, 'ID: %d' % (ids[i][0]))
        bot.send_message(message.chat.id, 'Нажмите кнопку чтобы вернуться к информации о заказах', reply_markup=markup)
        bot.register_next_step_handler(message, worker_choice)
    elif message.text == 'Вернуться в меню работника':
        worker_panel(message)


def end_zakaz(message):
    if message.text == 'Вернуться в меню работника':
        worker_panel(message)
    else:
        client_id = message.text
        try:
            test_client = int(message.text)
        except:
            bot.send_message(message.chat.id, 'Неверный ID')
            bot.register_next_step_handler(message, end_zakaz)
            return
        conn = sq.connect('database.sql')
        cur = conn.cursor()
        cur.execute('DELETE FROM workers WHERE tg_id_ispoln = "%s"' % (client_id))
        conn.commit()
        bot.send_message(message.chat.id, 'Заказ закрыт')
        worker_panel(message)

bot.polling(none_stop=True)
