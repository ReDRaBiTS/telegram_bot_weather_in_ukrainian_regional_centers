import telebot
import sqlite3
import threading
from telebot import types
from variables import API_KEY_TG, CITES_LIST
from requests_w_class import Weather


bot = telebot.TeleBot(API_KEY_TG)
# Створення БД
# Creating a database
db = sqlite3.connect('db.sqlite', check_same_thread=False)
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name VARCHAR(50), second_name VARCHAR(50), user_id INTEGER, chat_id IMTEGER ,city_name VARCHER(20), date DATE)')
db.commit()
cursor.close

# Lock the thread for correct operation of sqlite3
lock = threading.Lock()

# Стартове привітання
# Starting greeting

@bot.message_handler(commands=["start", "overwriting"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        'Вибрати своє місто', callback_data='select_your_city'))
    bot.send_message(message.chat.id, "Виберіть своє місто:",
                     reply_markup=markup)

# Функція для вибору міста
# Function for selecting a city

def choose_a_city(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for city in CITES_LIST:
        markup.add(types.KeyboardButton(f"{city}"))
    return bot.send_message(message.chat.id, "Ось список міст Укріїни, вибереть серед них своє", reply_markup=markup)

# Обробка колбеків
#Callbacks processing 

@bot.callback_query_handler(func=lambda callback: True)
def callbacks(callback):
    if callback.data == 'select_your_city':
        choose_a_city(callback.message)
    elif callback.data == 'change_city':
        with lock:
            cursor.execute('DELETE FROM users WHERE chat_id = %d' %
                           callback.message.chat.id)
            db.commit()
            cursor.close
        choose_a_city(callback.message)
    elif callback.data == 'today_weather':
        print_today_weather(callback.message)
    elif callback.data == 'tomorrow_weather':
        print_tomorrow_weather(callback.message)


# Запис данниз до БД
# Writing data to the database
@bot.message_handler(func=lambda message: message.text.strip() in CITES_LIST)
def write_to_db(message):
    try:
        with lock:
            cursor.execute('SELECT user_id FROM users WHERE user_id = %d' % int(
                message.from_user.id)).fetchall()[0][0]
    except:
        with lock:
            cursor.execute('INSERT INTO users (first_name, second_name, user_id, chat_id, city_name ,date) VALUES ("%s", "%s","%s","%s","%s", DATETIME())' % (
                message.from_user.first_name, message.from_user.last_name, int(message.from_user.id), int(message.chat.id), message.text.strip()))
            db.commit()
            cursor.close
    working_condition(message)

# Панель з кнопками
# Panel with buttons

@bot.message_handler(commands=["work"])
def working_condition(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        "Показати погоду у Вашому місті", callback_data='today_weather')
    button2 = types.InlineKeyboardButton(
        "Вибрати інше місто", callback_data='change_city')
    button3 = types.InlineKeyboardButton(
        "Погода на завтра", callback_data='tomorrow_weather')
    markup.row(button1)
    markup.row(button3)
    markup.row(button2)
    bot.send_message(
        message.chat.id, f'Ви вибрали місто {return_selected_city(message)}, зараз оберіть одну з функцій', reply_markup=markup)


# Виводить сьогоднішню погоду
# Displays today's weather
def print_today_weather(message):
    wtext = Weather(return_selected_city(message))
    message_dict = wtext.output_json()
    bot.send_message(
        message.chat.id, text=f'Погода у місті: {return_selected_city(message)}')
    for title, value in (message_dict.items()):
        bot.send_message(
            message.chat.id, text=f"{title}        {value}", parse_mode='html', disable_notification=True)
    working_condition(message)


# Виводить погоду на завтра
# Displays the weather for tomorrow
def print_tomorrow_weather(message):
    wtext = Weather(return_selected_city(message))
    message_dict = wtext.output_json_tomorrow()
    for title, value in (message_dict.items()):
        bot.send_message(
            message.chat.id, text=f"Прогноз погоди у місті {return_selected_city(message)} на {title}        <b>{value}</b>", parse_mode='html', disable_notification=True)
    working_condition(message)

# Зчитує вибране місто з БД
# Reads the selected city from the database
def return_selected_city(message):
    with lock:
        city_name = cursor.execute(
            'SELECT city_name FROM users WHERE chat_id = %d' % message.chat.id).fetchall()[0][0]
        db.commit()
        cursor.close
    return (city_name)


# Постійна робота програми
# Permanent operation of the program
bot.polling(none_stop=True)
