import telebot
from telebot import types
import back_bot
from data.data_base import db_session
from functions import *

bot = telebot.TeleBot("6011527798:AAEHTIIZUgoEi6lOc9hDW_pF1G1rLVAfKds")
users = {}
db_session.global_init("./data/data_base.db")
session = db_session.create_session()

@bot.message_handler(func=lambda message: message.text == '/exit')
def exit(message):
    users[message.chat.id]["place"] = "none"
    start_message(message)
@bot.message_handler(func=lambda message: message.text == '🔍 Поиск по номеру CVE')
def search_CVE_by_number(message):
    users[message.chat.id]["place"] = "CVE_search_menu"
    if not "number_CVE" in users[message.chat.id]:
        markupRemove = types.ReplyKeyboardRemove()
        sent_message = bot.send_message(message.chat.id,
                                        '📥💬Введите номер CVE\nВ формате "CVE-2023-31702"',reply_markup=markupRemove)
        users[message.chat.id]["number_CVE"]="0"
        return
    else:
        _=back_bot.webAppKeyboard(message.text)
        if _[0]==0:
            sent_message = bot.send_message(message.chat.id,
                                            'Ничего не найдено')
        else:
            sent_message = bot.send_message(message.chat.id,
                                        'Отправляю запрос в бд...',reply_markup=_[1])

        users[message.chat.id].pop("number_CVE",None)
        users[message.chat.id]["place"]="none"

@bot.message_handler(func=lambda message: message.text == '🔍 Поиск по параметрам')
def search_params_menu(message):
    if message.text=="🔍 Поиск по параметрам" and "bd_search" in users[message.chat.id]:
        users[message.chat.id].pop("bd_search", None)
        users[message.chat.id].pop("cond", None)
        sent_message = bot.send_message(message.chat.id,
                                        'Удаление данных предидущих запросов\n')
    markupRemove = types.ReplyKeyboardRemove()
    users[message.chat.id]["place"]= "find_menu"
    if not "cond" in users[message.chat.id]:
        users[message.chat.id]["cond"] = "product"
        sent_message = bot.send_message(message.chat.id,
                                        '📝Введите название продукта или вендора\n Например:\n"macOS"\n"Firefox"\n"Ethernet Controllers"\nБез кавычек\n Вводите название так чтобы количество запросов не было болшим, иначе мы не полностью обработаем запрос\n➡️🚪 Для выхода введите /exit',reply_markup=markupRemove)
        return

    match users[message.chat.id]["cond"]:
        case "product":
            users[message.chat.id]["cond"] = "version"
            users[message.chat.id]["bd_search"]={}
            users[message.chat.id]["bd_search"]["product"]=message.text
            sent_message = bot.send_message(message.chat.id,
                                            '📝Введите версию продукта \n Например:\n" 2019.010.20100"\n"72.0.3626.121"\n"66.0.2"\nБез кавычек\n Если Версии нету напишите -',reply_markup=markupRemove)
        case "version":
            users[message.chat.id]["bd_search"]["version"] = message.text
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            itembtn1 = types.KeyboardButton('Поиск')
            itembtn2 = types.KeyboardButton('Отмена')
            markup.add(itembtn1, itembtn2)
            sent_message = bot.send_message(message.chat.id,'Мы готовы к поиску',reply_markup=markup)
            users[message.chat.id]["cond"] = "req"
        case "req":
            if message.text=="Поиск":
                parametrs= None
                ans = back_bot.CVE_profuct_find(users[message.chat.id]["bd_search"]["product"]+users[message.chat.id]["bd_search"]["version"], parametrs)
                if len(ans)==0:
                    sent_message = bot.send_message(message.chat.id,"🙃Ничего не найдено, попробуйте снова")
                    users[message.chat.id].pop("bd_search", None)
                    users[message.chat.id].pop("cond", None)
                    return
                for i in ans:
                    markup=back_bot.Get_inline_marrkup(f"CVE-{i[0]}")[1]
                    if users[message.chat.id]["lang"]=="eu":
                        sent_message = bot.send_message(message.chat.id, f"💢CVE Номер:{i[0]}\n\nℹ️Описание CVE:{i[1]}",
                                                        reply_markup=markup)
                    else:
                        sent_message = bot.send_message(message.chat.id, f"💢CVE Номер:{i[0]}\n\nℹ️Описание CVE:{back_bot.translate(i[1])}",
                                                        reply_markup=markup)

                users[message.chat.id]["place"] = "sort_menu"
                itembtn1 = types.KeyboardButton('🔍 Уровень критичности')
                itembtn2 = types.KeyboardButton('🔍 CVSS рейтинг')
                itembtn3 = types.KeyboardButton('🔍 Метрики CVSS')
                itembtn4 = types.KeyboardButton('🔍 EPSS рейтинг')
                itembtn5 = types.KeyboardButton('🔍 Дата/время регистрации CVE')
                itembtn6 = types.KeyboardButton('🔍 Присутсвие PoC/CVE WriteUp')
                itembtn7 = types.KeyboardButton('🧐 Выполнить сортировку')
                itembtn8 = types.KeyboardButton('🔙 Выход из поиска CVE')
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8)
                sent_message = bot.send_message(message.chat.id,
                                                'Мы можем отсортировать список по этим категориям:\n'
                                                '🔍 Уровень критичности\n'
                                                '🔍 CVSS рейтинг\n'
                                                '🔍 Метрики CVSS\n'
                                                '🔍 EPSS рейтинг\n'
                                                '🔍 Дата/время регистрации CVE\n'
                                                '🔍 Присутсвие PoC/CVE WriteUp\n', reply_markup=markup)
            else:
                users[message.chat.id].pop("bd_search", None)
                users[message.chat.id].pop("cond", None)



def find_CVE_parametr(name,version,parametrs):
    if parametrs is None:
        print("no parms")
    else:
        print(name,version,parametrs)

def user_set_parametr_to_sort(message):
    users[message.chat.id]["place"] = "sort_menu"
    if not "sort_parametrs" in users[message.chat.id]:
        users[message.chat.id]["sort_parametrs"]={}
    if "waiting_ans" in users[message.chat.id]:
        users[message.chat.id]["sort_parametrs"][users[message.chat.id]["waiting_ans"]]=message.text
        users[message.chat.id].pop("waiting_ans")
        message.text="_"
    markupRemove = types.ReplyKeyboardRemove()
    match message.text:
        case '🔍 Уровень критичности':
            sent_message = bot.send_message(message.chat.id,'Введите промежуток от 1 до 10\n Например:\n"4-7"',reply_markup=markupRemove)
            users[message.chat.id]["waiting_ans"]="critic_lvl"
        case '🔍 CVSS рейтинг':
            sent_message = bot.send_message(message.chat.id, 'Введите промежуток от 1 до 10\n Например:\n"2-4"',reply_markup=markupRemove)
            users[message.chat.id]["waiting_ans"] = "CVSS_rating"
            print("2")
        case '🔍 Метрики CVSS':
            sent_message = bot.send_message(message.chat.id, 'Введите название метрик, которые нужно учитывать при поиске\n Например:\n"Network"\n"Adjacent Network"\n"Local"\nБез кавычек',reply_markup=markupRemove)
            users[message.chat.id]["waiting_ans"] = "metric_CVSS"
            print("3")
        case '🔍 EPSS рейтинг':
            sent_message = bot.send_message(message.chat.id, 'Введите промежуток от 1 до 10\n Например:\n"4-7"',reply_markup=markupRemove)
            users[message.chat.id]["waiting_ans"] = "EPSS_rating"
        case '🔍 Дата/время регистрации CVE':
            sent_message = bot.send_message(message.chat.id,
                                            'Введите промежуток в формате ДД:ММ:ГГ-ДД:ММ:ГГ\n Например:\n"16:02:23"\n"26:05:23"\nБез кавычек',reply_markup=markupRemove)
            users[message.chat.id]["waiting_ans"] = "date_CVE"
        case '🔍 Присутсвие PoC/CVE WriteUp':
            sent_message = bot.send_message(message.chat.id,
                                            'Введите on/off чтобы все ответы содержали CVE WriteUp и PoC\n Например:\n"on"\n"off\nБез кавычек',reply_markup=markupRemove)
            users[message.chat.id]["waiting_ans"] = "PoC/CVE_writeUp"
        case '🧐 Выполнить сортировку':
            find_CVE_parametr(users[message.chat.id]["bd_search"]["product"],users[message.chat.id]["bd_search"]["version"],users[message.chat.id]["sort_parametrs"])
        case '🔙 Выход из поиска CVE':
            users[message.chat.id]["place"]="none"
            echo_message(message)
        case _:
            itembtn1 = types.KeyboardButton('🔍 Уровень критичности')
            itembtn2 = types.KeyboardButton('🔍 CVSS рейтинг')
            itembtn3 = types.KeyboardButton('🔍 Метрики CVSS')
            itembtn4 = types.KeyboardButton('🔍 EPSS рейтинг')
            itembtn5 = types.KeyboardButton('🔍 Дата/время регистрации CVE')
            itembtn6 = types.KeyboardButton('🔍 Присутсвие PoC/CVE WriteUp')
            itembtn7 = types.KeyboardButton('🧐 Выполнить сортировку')
            itembtn8 = types.KeyboardButton('🔙 Выход из поиска CVE')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(itembtn1, itembtn2, itembtn3,itembtn4,itembtn5,itembtn6,itembtn7,itembtn8)
            sent_message = bot.send_message(message.chat.id,
                                            'Мы можем отсортировать список по этим категориям:\n'
                                            '🔍 Уровень критичности\n'
                                            '🔍 CVSS рейтинг\n'
                                            '🔍 Метрики CVSS\n'
                                            '🔍 EPSS рейтинг\n'
                                            '🔍 Дата/время регистрации CVE\n'
                                            '🔍 Присутсвие PoC/CVE WriteUp\n',reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '📩 Настройка уведомлений')
def notifications_menu(message):
    users[message.chat.id]["place"] = "notice_menu"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('📥 Подписаться')
    itembtn2 = types.KeyboardButton('📤 Отписаться')
    itembtn3 = types.KeyboardButton('🛠️ Настроить уведомления')
    itembtn4 = types.KeyboardButton('🛠️ Выйти из меню')
    markup.add(itembtn1, itembtn2, itembtn3,itembtn4)
    bot.send_message(message.chat.id, "Выбери, что ты хочешь сделать:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🛠️ Выйти из меню')
def back(message):
    users[message.chat.id]["place"]="none"
    start_message(message)

@bot.message_handler(func=lambda message: message.text == '📥 Подписаться')
def hello_sub(message):
    bot.send_message(message.chat.id, "Вы подписаны")

@bot.message_handler(func=lambda message: message.text == '📤 Отписаться')
def bay_sub(message):
    bot.send_message(message.chat.id, "Вы отписаны")

@bot.message_handler(func=lambda message: message.text == '🛠️ Настроить уведомления')
def configure_notifications_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('🔢 Регулярность уведомлений')
    itembtn2 = types.KeyboardButton('🚨 Уведомления по уровням')
    itembtn3 = types.KeyboardButton('🌟 Уведомления по рейтингам')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Выбери, какие уведомления тебе нужны, или выбери дополнительные пункты:",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🔢 Регулярность уведомлений')
def notification_frequency_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('🕒 Каждые 30 минут')
    itembtn2 = types.KeyboardButton('🕕 Каждый час')
    itembtn3 = types.KeyboardButton('🗓️ Каждый день')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Выбери, с какой регулярностью ты хочешь получать уведомления:",
                     reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '🚨 Уведомления по уровням')
def notification_severity_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('🔴 Critical')
    itembtn2 = types.KeyboardButton('🟠 High')
    itembtn3 = types.KeyboardButton('🟡 Medium')
    itembtn4 = types.KeyboardButton('🟢 Low')
    itembtn5 = types.KeyboardButton('🔵 None')
    itembtn5 = types.KeyboardButton('🔵 Выйти в меню уведомлений')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    if users[message.chat.id]["place"]!="notice_lvl_menu":
        bot.send_message(message.chat.id, "Выбери, по каким уровням уязвимостей ты хочешь получать уведомления, чтобы отключить уведомления об одной из категорий нажмите ее еще раз:",
                        reply_markup=markup)
    users[message.chat.id]["place"]="notice_lvl_menu"
@bot.message_handler(func=lambda message: message.text == '🔵 Выйти в меню уведомлений')
def back_menu(message):
    users[message.chat.id]["place"]="none"
    echo_message(message)

@bot.message_handler(func=lambda
        message: message.text == '🔴 Critical' or message.text == '🟠 High' or message.text == '🟡 Medium' or message.text == '🟢 Low' or message.text == '🔵 None')
def back(message):
    bot.send_message(message.chat.id,
                     f"Ты подписался на уведомления о новых уязвимостях с уровнем критичности {message.text}.")
    notification_severity_menu(message)


@bot.message_handler(func=lambda message: message.text == '🌟 Уведомления по рейтингам')
def notification_cvss_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('⭐ 9.0 - 10.0')
    itembtn2 = types.KeyboardButton('🌟 7.0 - 8.9')
    itembtn3 = types.KeyboardButton('✨ 4.0 - 6.9')
    itembtn4 = types.KeyboardButton('💫 0.1 - 3.9')
    itembtn5 = types.KeyboardButton('🔵 Выйти в меню уведомлений')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4,itembtn5)
    if users[message.chat.id]["place"]!="notice_rating_menu":
        bot.send_message(message.chat.id, "Выбери, по каким уровням уязвимостей ты хочешь получать уведомления, чтобы отключить уведомления об одной из категорий нажмите ее еще раз:",
                        reply_markup=markup)
    users[message.chat.id]["place"]="notice_rating_menu"



@bot.message_handler(func=lambda
        message: message.text == '⭐ 9.0 - 10.0' or message.text == '🌟 7.0 - 8.9' or message.text == '✨ 4.0 - 6.9' or message.text == '💫 0.1 - 3.9')
def rating_notifications(message):
    bot.send_message(message.chat.id, f"Ваш ответ принят. {message.text}")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    try:
        if  not message.chat.id in users:
            start_message(message)
            return
        if message.text=="ru":
            users[message.chat.id]["lang"]="ru"
            start_message(message)
            return
        if message.text=="eu":
            users[message.chat.id]["lang"]="eu"
            start_message(message)
            return
        else:
            match users[message.chat.id]["place"]:
                case "find_menu":
                    search_params_menu(message)
                    return
                case "sort_menu":
                    user_set_parametr_to_sort(message)
                case "CVE_search_menu":
                    search_CVE_by_number(message)
                case "notice_menu":
                    notifications_menu(message)
                case "notice_lvl_menu":
                    notification_severity_menu(message)
                case "notice_rating_menu":
                    notification_cvss_menu(message)
                case _:
                    start_message(message)
    except:
        print("error\n")
@bot.message_handler(commands=['/start'])
def start_message(message):
    if not message.chat.id in users:
        users[message.chat.id]={}
        users[message.chat.id]["place"] = "none"
        users[message.chat.id]["lang"] = "eu"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('🔍 Поиск по номеру CVE')
    itembtn2 = types.KeyboardButton('🔍 Поиск по параметрам')
    itembtn3 = types.KeyboardButton('📩 Настройка уведомлений')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, f"Привет! Я помогу тебе найти информацию об уязвимостях. Выбери, что тебе нужно\nЧтобы переключить язык напишите eu или ru\nСейчас {users[message.chat.id]['lang']}:",
                     reply_markup=markup)


if __name__ == '__main__':
    bot.polling()
