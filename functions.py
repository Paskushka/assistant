import datetime
import re
import requests
from googletrans import Translator
import pyautogui as pg
import keyboard
import webbrowser
import speech_recognition as sr
import user
from user import client
from audioProcessor import AudioProcessor
import time
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pybrightness
import subprocess
import platform
import wikipedia
import openai
import os
import pywinauto
import random
import geocoder


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


def spotify_function(a) -> str:
    sentence = ''.join(a)
    # открывает и ищет в Spotify через браузер
    url = "https://open.spotify.com/search/" + sentence
    webbrowser.get().open(url)
    return "Открываю спотифай"


def launch_desktop_spotify(a) -> str:
    # запуск десктопного приложения Spotify и запуск существующей песни
    sentence: str = ""
    for i in a:
        sentence += i
    print(sentence)
    pg.moveTo(250, 1050)
    pg.click()
    time.sleep(1)
    try:
        keyboard.write("spotify")
        keyboard.send("enter")
        time.sleep(3)
        keyboard.press(" ")
        return "Открываю спотифай"
    except FileNotFoundError:
        return "Не удалось открыть, пробую открыть через браузер"


def mood_function(a) -> str:
    return "Какие дела могут быть у робота? Не крашнулся и то хорошо"

def joke_function(a) -> str:
    random_number = random.randint(0, 3)
    if random_number == 0:
        return "Если вы внезапно оказались в яме, первое, что нужно сделать - перестать копать!"
    elif random_number == 1:
        return "Штирлиц уходил от ответа, ответ неотступно следовал за ним."
    elif random_number == 2:
        return "Уходя из квартиры, делай селфи с утюгом! Так ты избежишь ненужных сомнений."
    elif random_number == 3:
        return "Колобок повесился, ахаххаха"

def commands_function(a) -> str:
    return "Пока что я могу: повторить за вами, настроить яркость и звук, выключить компьютер, изменить расскладку клавиатуры, подбросить монетку, рассказать или написать что-нибудь, найти информацию в интернете, рассказать прогноз погоды, найти видео в ютубе, рассказать анекдот, сказать сколько сейчас времени, найти определение в википедии, настроить данные о пользователе,  поприветсвовать вас, попрощаться с вами, найти песню в спотифай, также вы можете поинтересоваться как у меня дела"


def search_function(a) -> str:  # type: ignore
    sentence = ''.join(a)
    try:
        webbrowser.open_new_tab("https://www.google.com/search?q=" + sentence)
        return "Открываю браузер"
    except:
        return "Не удалось открыть браузер"


def youtube_function(a) -> str:
    # print(sentence)
    sentence = ''.join(a)
    url = "https://www.youtube.com/results?search_query=" + sentence
    try:
        webbrowser.get().open(url)
        return "Открываю ютуб"
    except:
        return "Не удалось открыть ютуб"


def wikipedia_function(query) -> str:
    sentence = ''.join(query)
    url = "https://ru.wikipedia.org/wiki/Special:Search?search=" + sentence
    try:
        webbrowser.get().open(url)
        return "Открываю Википедию"
    except:
        return "Не удалось открыть Википедию"


def settings_function(a) -> str:
    settings = AudioProcessor()

    settings.answer_text_to_audio(
        "Выберете что вы хотите поменять: имя, пол, основной язык, дополнительный язык, город")
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

    return "Изменения были успешно введены"


def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Говорите...")
        audio = r.listen(source, phrase_time_limit=5)
        return audio


def repeat_function(a) -> str:
    sentence = ''.join(a)
    repeat = AudioProcessor()
    repeat.answer_text_to_audio(sentence)
    return ""



# функция работает по типу яркость + число на которое надо установить текущюу яркость в процентах
def brightness_function(a) -> str:
    sentence = ' '.join(a)
    number = int(re.findall(r'\d+', sentence)[0] + re.findall(r'\d+', sentence)[1])
    pybrightness.custom(number)
    return ""
    
# оч опасная функция честно первый раз было оч страшно запускать
def off_function (a) -> str:
    subprocess.call('shutdown /s /t 2', shell=True)
    return ""


def key_board_function(a) -> str:
    keyboard.press_and_release('left alt + shift')
    return ""


def write_function_function(a) -> str:
    sentence = "напиши " + ''.join(a)

    print(sentence)
    openai.api_key = "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"
    model_engine = "text-davinci-002"
    openai.api_base = "https://api.openai.com/v1/"

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=sentence,
        max_tokens=3000,
        n = 1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    generated_text = message.strip()
    try:
        answer = "Запрос: " + sentence + ' ' + generated_text
        with open('function.txt', 'w') as f:
            f.write(answer)
        os.system("function.txt")
        return "Задание выполнено"

    except:
        return "Задание не выполнено"


def say_function(a) -> str:
    sentence = "расскажи " + ''.join(a)
    print(sentence)
    openai.api_key = "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"
    model_engine = "text-davinci-002"
    openai.api_base = "https://api.openai.com/v1/"

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=sentence,
        max_tokens=2000,
        n = 1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    generated_text = message.strip()

    return generated_text

def coin_function(a) -> str:
    random_number = random.randint(0, 1)
    if random_number == 0:
        return "Выпал орел"
    else:
        return "Выпала решка"
    
def sound_function(a) -> str:
     devices = AudioUtilities.GetSpeakers()
     interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
     volume = cast(interface, POINTER(IAudioEndpointVolume))
     current_volume = volume.GetMasterVolumeLevelScalar()
     if current_volume == 0:
        new_volume = 0.5
     else:
         new_volume = 0
     volume.SetMasterVolumeLevelScalar(new_volume, None)
     return ""
    
def where_function(a) -> str:
    g = geocoder.ip('me')
    lat = g.latlng[0]
    lng = g.latlng[1]
    str = f"Вы находитесь на координатах {lat} градусов широты и {lng} градусов долготы"
    return str

# def app_function(a) -> str:
#     sentence = ' '.join(a)
#     settings = AudioProcessor()
#     settings.answer_text_to_audio("Скажите название приложения")
#     audio = recognize_speech()
#     text = settings.audio_to_text(audio)
#     pyautogui.press("win")
#     pyautogui.typewrite(text)
#     pyautogui.press("enter")
