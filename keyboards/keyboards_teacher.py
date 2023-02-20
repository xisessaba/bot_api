################################################################################
#                                                                              #
#                            Клавиатура учителя                                #
#                                                                              #
#                                                                              #
################################################################################


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import http_api
import requests



def get_keyboard_teacher(name: str, lookup=''):
    if name == "menu_teacher":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Заказы📚") 
        keyboard.add("Мои решения✉️")
        keyboard.add("Статистика📝")
        keyboard.add("Тех поддержка💻")
    elif name == "orders":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Решить✍️")
        keyboard.add("Отклонено цена💸")
        keyboard.add("Отклонено время на решения⏱")
        keyboard.add("Отклонено СПАМ🚫")
        keyboard.add("Назад🔚")
    elif name == "download":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Загрузить решение")
        keyboard.add("Не могу решить")
        keyboard.add("Назад🔚")
    elif name == "my_solutions":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Решенные задачи")
        keyboard.add("Ожидают решения")
        keyboard.add("Ожидают оплату")
        keyboard.add("Назад🔚")
    elif name == "my_solutions_2":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Загрузить решение")
        keyboard.add("Не могу решить")
        keyboard.add("Назад🔚")
    elif name == "registartion":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Регистрация📝")
    elif name == "payment":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Оплачено", "Не оплачено" )
        keyboard.add("Назад🔚")
    elif name == "grade":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        request_kb = requests.get(f'{http_api}/grade/')
        for i in request_kb.json():
            keyboard.add(i['grade'])
    elif name == "subject":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        req = requests.get(f'{http_api}/subject/?grade__grade={lookup}') #ОТПРАВЛЯЕМ ЗАПРОС НА СЕРВЕР И ПОЛУЧАЕМ ПРЕДМЕ>       
        for reqs in req.json(): # С ПОМОЩЬЮ ЦИКЛА ВЫВОДИМ КЛАВИАТУРУ
            keyboard.insert(reqs['subject'])


    return keyboard
    