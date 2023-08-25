import requests
import datetime
from variables import API_KEY_WT


class Weather:

    def __init__(self, city):
        self.city = city

    weather_dict = {
        'Thunderstorm': '⛈ Гроза ⛈',
        'Drizzle': '🌦 Мряка 🌦',
        'Rain': '🌧 Дощ 🌧',
                'Snow': '🌨 Сніг 🌨',
                'Mist': '🌫 Туман🌫 ',
                'Smoke': 'Дим',
                'Haze': '💨 Легкий туман 💨',
                'Dust': 'Пил',
                'Fog': '🌫 Сильний туман 🌫',
                'Sand': 'Пісок',
                'Ash': 'Попіл',
                'Squall': '🌬 Сильний вітер 🌬',
                'Tornado': '🌪 Торнадо 🌪',
                'Clear': '☀️ Ясне небо ☀️',
                'Clouds': '⛅️ Хмарно ⛅️'
    }

    wind_directions = {
        'Північний': (348.75, 11.25),
        'Північно-східний': (11.25, 78.75),
        'Східний': (78.75, 101.25),
        'Південно-східний': (101.25, 168.75),
        'Південний': (168.75, 191.25),
        'Південно-західний': (191.25, 258.75),
        'Західний': (258.75, 281.25),
        'Північно-західний': (281.25, 348.75),
    }

    cities_dict = {
        "Київ": "Kyiv",
        "Харків": "Kharkiv",
        "Одеса": "Odessa",
        "Дніпро": "Dnipro",
        "Донецьк": "Donetsk",
        "Запоріжжя": "Zaporizhzhia",
        "Львів": "Lviv",
        "Кривий Ріг": "Kryvyi Rih",
        "Миколаїв": "Mykolaiv",
        "Маріуполь": "Mariupol",
        "Вінниця": "Vinnytsia",
        "Херсон": "Kherson",
        "Полтава": "Poltava",
        "Чернігів": "Chernihiv",
        "Черкаси": "Cherkasy",
        "Житомир": "Zhytomyr",
        "Суми": "Sumy",
        "Івано-Франківськ": "Ivano-Frankivsk",
        "Тернопіль": "Ternopil",
        "Кропивницький": "Kropyvnytskyi",
        "Ужгород": "Uzhhorod",
        "Луцьк": "Lutsk",
        "Мелітополь": "Melitopol",
        "Кам'янець-Подільський": "Kamianets-Podilskyi",
        "Хмельницький": "Khmelnytskyi",
        "Рівне": "Rivne",
        "Севастополь": "Sevastopol",
        "Сімферополь": "Simferopol",
        "Маріуполь": "Mariupol"
    }

    # Запит на сайт openweathermap.org за сьогоднішньою погоду
    # Request to openweathermap.org for today's weather
    def weather_request(self, city):
        weather_req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WT}&units=metric")
        return weather_req

    # Request to openweathermap.org for tomorrow weather
    def tomorrow_weather_request(self, city):
        weather_req = requests.get(
            f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY_WT}&units=metric")
        return weather_req

    # Форматування тексту
    # Formatting the text
    def print_weather_on_screen(self, json_text):

        values = [
            f"<b> {json_text['main']['temp']} C°    {self.translate_weather(json_text['weather'][0]['main'])}</b>",
            f"<b>{datetime.datetime.fromtimestamp(json_text['sys']['sunrise']).strftime('%H:%M')}</b>   \nЗахід сонця:       <b>{datetime.datetime.fromtimestamp(json_text['sys']['sunset']).strftime('%H:%M')}</b>",
            f"<b>{self.convert_to_wind_direction(json_text['wind']['deg'])}</b>  \nШвідкість вітру:         <b>{json_text['wind']['speed']} м/c</b>",
            f"<b>{round(json_text['main']['pressure']* 0.7500637555419211, 2)} мм.рт.ст</b>"
        ]

        titles = [
            "Погода:",
            "Схід сонця:",
            "Напрямок вітру:",
            "Повітряний тиск:"
        ]
        answer_string = dict(zip(titles, values))

        return answer_string

    # Конвертуємо напрям вітру
    # Convert the wind direction

    def convert_to_wind_direction(self, degrees):

        # Перевірка, щоб кут був у діапазоні [0, 360)
        degrees = degrees % 360

        # Пошук відповідного напрямку
        for direction, (start, end) in self.wind_directions.items():
            if start <= degrees < end:
                return direction

        # Якщо не вдалося знайти відповідний напрямок
        return 'Помилка'

    # Перекладаємо погоду з англійської
    # Translate weather from English
    def translate_weather(self, weather):

        for eng, ukr in self.weather_dict.items():
            if eng == weather:
                return ukr
        return 'Помилка'

    def output_json(self):
        today_weather_req = self.weather_request(self.cities_dict[self.city])
        json_text = today_weather_req.json()
        return self.print_weather_on_screen(json_text)

    def output_json_tomorrow(self):
        tomorrow_weather_req = self.tomorrow_weather_request(
            self.cities_dict[self.city])
        json_text = tomorrow_weather_req.json()
        return self.print_tomorrow_weather(json_text)

    # Форматування тексту для прогноза погоди на завтра
    # Formatting text for tomorrow's weather forecast

    def print_tomorrow_weather(self, json_text):
        values = [
            f"           {json_text['list'][self.tommorow_list_index()]['main']['temp_max']} C°   {self.translate_weather(json_text['list'][self.tommorow_list_index()]['weather'][0]['main'])} \n\n",
        ]

        titles = [
            f"<b>{(datetime.datetime.now()+ datetime.timedelta(days=1)).strftime('%d.%m.%Y')}</b>\n\n",

        ]
        answer_string = dict(zip(titles, values))

        return answer_string

    # Вираховуємо який індекс треба вказати в запиті для отримання інформаії про погоду на завтра
    # Calculate which zip code should be specified in the request to receive information about the weather for tomorrow

    def tommorow_list_index(self):
        # година у ячку було зроблено запит
        hour_now = int(datetime.datetime.now().strftime("%H"))
        hour_list = [x for x in range(24)]
        index_list = [12, 12, 12, 1, 11, 11, 10, 10, 10,
                      9, 9, 9, 8, 8, 8, 7, 7, 7, 6, 6, 6, 5, 5, 5]
        index_dict = dict(zip(hour_list, index_list))
        return index_dict[hour_now]
