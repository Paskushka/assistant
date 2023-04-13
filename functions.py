import datetime
import re
import requests
import webbrowser
import speech_recognition as sr
import pyttsx3
import user

from googletrans import Translator, constants
from user import User
from user import client
from audioProcessor import AudioProcessor

def extract_city_function(command: str):
    pattern = r"погода в ([\w\s]+)"
    match = re.search(pattern, command.lower())
    if match:
        return match.group(1)
    else:
        return None


def weather_function(a):
    # замените на свой API ключ OpenWeatherMap
    api_key = "d3b9ddd02bf307000417e311a213a7f4"
    base_url = f"https://api.openweathermap.org/data/2.5/weather?q={user.client.town}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    translator = Translator()
    if response.status_code == 200:
        data = response.json()
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return translator.translate(text=
            f"In {user.client.town} {weather}, temperature {int(temperature)} degrees celsius, humidity {int(humidity)} percents, and wind speed {int(wind_speed)} meters per second.",
            dest="ru").text
    else:
        return "Извините, я не смог получить информацию о погоде в этом городе."


def hello_function(a) -> str:
    return "Хабар принес?"


def doing_function(a) -> str:
    return "Можно и передохнуть маленько"


def time_function(a) -> str:
    now = datetime.datetime.now()
    return "Сейчас " + str(now.hour) + ":" + str(now.minute)


def stop_function(a) -> str:
    return "Ну, удачной охоты, сталкер."


def default_function(a) -> str:
    return "Не удалось распознать команду."


def mood_function(a) -> str:
    return "Какие дела могут быть у робота? Не крашнулся и то хорошо"


def joke_function(a) -> str:
    return "Колобок повесился, ахаххаха"


def commands_function(a) -> str:
    return "Пока что я могу: найти информацию в интернете, рассказать анектод, сказать сколько сейчас времени, поприветсвовать вас, попрощаться с кожанным, также вы можете поинтересоваться как у меня дела"


def search_function(a) -> str:  # type: ignore
    sentence:str = ""
    for i in a:
        sentence += ' ' + i
    try:
        webbrowser.open_new_tab("https://www.google.com/search?q="+sentence)
        return "Открываю браузер"
    except:
        return "Не удалось открыть"
    
def youtube_function(a)->str:
    sentence:str = ""
    for i in a:
        sentence += ' ' + i
    print(sentence)
    url = "https://www.youtube.com/results?search_query=" + sentence
    try:
        webbrowser.get().open(url)
        return "Открываю ютуб"
    except:
        return "Не удалось открыть"

def settings_function(a)->str:
    settings = AudioProcessor()

    settings.answer_text_to_audio("Выберете что вы хотите поменять: имя, пол, основной язык, дополнительный язык, город")
    audio = recognize_speech()
    parametr = settings.audio_to_text(audio)

    if parametr == "имя":
        settings.answer_text_to_audio("Скажите как вас зовут")
        audio = recognize_speech()
        name = settings.audio_to_text(audio)
        client.name = name
    elif parametr == "пол":
        settings.answer_text_to_audio("Скажите какого вы пола")
        audio = recognize_speech()
        sex = settings.audio_to_text(audio)
        client.sex = sex
    elif parametr == "основной язык":
        settings.answer_text_to_audio("Каким будет ваш основной язык")
        audio = recognize_speech()
        language = settings.audio_to_text(audio)
        client.language = language
    elif parametr == "дополнительный язык":
        settings.answer_text_to_audio("Каким будет ваш дополнительный язык")
        audio = recognize_speech()
        second_language = settings.audio_to_text(audio)
        client.secondLanguage = second_language
    elif parametr == "город":
        settings.answer_text_to_audio("Каким будет ваш город")
        audio = recognize_speech()
        town = settings.audio_to_text(audio)
        client.town = town

    settings.answer_text_to_audio("Изменения были успешно введены")

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        audio = r.listen(source, phrase_time_limit=5)
        return audio

