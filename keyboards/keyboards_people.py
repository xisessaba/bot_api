################################################################################
#                                                                              #
#                            Клавиатура ученика                                #
#                                                                              #
#                                                                              #
################################################################################



from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from create_bot import http_api




def get_keyboard_people(name: str, lookup=''):
    if name == "people":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Заказать решение📚") # done
        keyboard.add("Мои заказы📊") # done
        keyboard.add("Тех.поддержка💻") # done
    elif name == "grade":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        request_kb = requests.get(f'{http_api}/grade/') 
        for i in request_kb.json():
            keyboard.add(i['grade'])
        keyboard.add("Отмена")
    elif name == "subject":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        req = requests.get(f'{http_api}/subject/?grade__grade={lookup}') #ОТПРАВЛЯЕМ ЗАПРОС НА СЕРВЕР И ПОЛУЧАЕМ ПРЕДМЕТЫ ПО КЛАССУ КОТОРЫЕ ЕСТЬ В БД
        for reqs in req.json(): # С ПОМОЩЬЮ ЦИКЛА ВЫВОДИМ КЛАВИАТУРУ
            keyboard.insert(reqs['subject'])
        keyboard.add("Отмена")
    elif name == "active_orders":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Активные заказы📈")
        keyboard.add("Выполненные заказы📉")
        keyboard.add("Статистика по заказам📊")
        keyboard.add("Назад🔙")
    elif name == "active_orders_2":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Решение верное")
        keyboard.add("Решение неверное")
        keyboard.add("Назад🔙")
    elif name == "register":
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add("Регистрация📝")
    elif name == "post_order":
        keyboard = InlineKeyboardMarkup(resize_keyboard = True)
        keyboard.add(InlineKeyboardButton(text = "Разместить задание✅", callback_data = "post_order"))
        keyboard.add(InlineKeyboardButton(text = "Отмена⛔️", callback_data = "cancel"))
    return keyboard

    