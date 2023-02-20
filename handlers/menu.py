################################################################################
#                                                                              #
#                              ГЛАВНОЕ МЕНЮ                                    #
#                       ЗДЕСЬ ЗАПУСКАЮТСЯ ВСЕ ФУНКЦИИ                          #
#                                                                              #
################################################################################


from aiogram import types
from keyboards import get_keyboard_teacher
from keyboards import get_keyboard_people
from handlers import http_async
import requests
from create_bot import http_api
from create_bot import bot, dp
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.people import Student
from handlers.teacher import TeacherHandler



class BotMain:
    def __init__(self, bot:bot):
        self.bot = bot
        
        dp.register_message_handler(self.main_handler, commands=['start', 'help'])
        dp.register_message_handler(self.main_handler, text = ['Регистрация📝', 'Тех.поддержка💻'])
        dp.register_message_handler(self.student, text = ['Заказать решение📚','Мои заказы📊','Отмена', 'Активные заказы📈', 'Выполненные заказы📉', 'Статистика по заказам📊', 'Решение верное', 'Решение неверное', 'Назад🔙', ])
        dp.register_message_handler(self.teacher, text = ['Заказы📚', 'Мои решения✉️','Статистика📝', 'Решить✍️', 'Отклонено цена💸', 'Отклонено время на решения⏱', 'Отклонено СПАМ🚫' 'Назад🔚', 'Загрузить решение','Ожидают решения', 'Ожидают оплату',  'Решенные задачи', 'Не могу решить', 'Оплачено', 'Не оплачено', ])


    async def main_handler(self, message: types.Message):
        if message.text == '/start':
            look_user_by_id = message.from_user.id #БЕРЕМ ЧАТ АЙДИ ПОЛЬЗОВАТЕЛЯ ПРИ НАЖАТИИ НА /START 
            res = requests.get(f'{http_api}/telegram-user/?user_id={look_user_by_id}').json() #ПОЛУЧАЕМ ИНФОРМАЦИЮ О ПОЛЬЗОВАТЕЛЕ 
            if res: #ПРОВЕРЯЕМ ЕСТЬ ЛИ ПОЛЬЗОВАТЕЛЬ В БАЗЕ
                if res[0]['role'] == 'student': #ПРОВЕРЯЕМ РОЛЬ ПОЛЬЗОВАТЕЛЯ ЯВЛЯЕТСЯ ЛИ ОН Ученикос
                    await message.answer('Привет, Ученик, рад вас видеть!', reply_markup=get_keyboard_people("people"))#ЕСЛИ СТАТУС ПОЛЬЗОВАТЕЛЯ УЧЕНИК, ТО ОТПРАВИТСЯ ЭТО СООБЩЕНИЕ
                elif res[0]['role'] == 'teacher':
                    await message.answer('Привет учитель, рад вас видеть', reply_markup=get_keyboard_teacher("menu_teacher"))
                else:
                    await message.answer('Привет, вижу тебя впервые.\nЯ бот для учеников. Здесь ты можешь найти решение на свое задание', reply_markup=get_keyboard_people("register"))
            else: #ЕСЛИ ПОЛЬЗОВАТЕЛЯ НЕТ В БАЗЕ ОТПРАВИТСЯ ЭТО СООБЩЕНИЕ
                await message.answer('Привет, вижу тебя впервые.\nЯ бот для учеников. Здесь ты можешь найти решение на свое задание', reply_markup=get_keyboard_people("register"))


        elif message.text == 'Регистрация📝':
            
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton("Отправить номер телефона📱", request_contact=True)) #СОЗДАЕМ КЛАВИАТУРУ
            await bot.send_message(message.from_user.id, 'Отлично! А теперь отправь нам номер телефона', reply_markup=keyboard) #ЕСЛИ УЧИТЕЛЬ, ТО ОТПРАВИТСЯ ЭТО СООБЩЕНИЕ
                    
            @dp.message_handler(content_types=types.ContentTypes.CONTACT)
            async def process_phone(message: types.Contact):
                phone_number = message.contact.phone_number
                # await Registration.description.set()
                # await message.answer('Отлично! Напишите краткое описание о себе', reply_markup=ReplyKeyboardRemove()) #ЕСЛИ УЧИТЕЛЬ, ТО ОТПРАВИТСЯ ЭТО СООБЩЕНИЕ
                    
                # @dp.message_handler(state=Registration.description)
                # async def process_description(message: types.Message, state: FSMContext):

                #     async with state.proxy() as data:
                #         data['description'] = message.text
                #     data_result = await state.get_data()
                #     description = data_result.get('description')
                #     await state.finish()
                


                # data = {
                #         "user_id": message.from_user.id, #СОХРАНЯЕМ В БАЗУ АЙДИ УЧЕНИКА
                #         "username": message.from_user.username, #СОХРАНЯЕМ В БАЗУ ЮЗЕРНЕЙМ УЧЕНИКА
                #         "first_name": message.from_user.first_name, #СОХРАНЯЕМ В БАЗУ НИК ПОЛЬЗОВАТЕЛЯ
                #         "last_name": message.from_user.last_name, #СОХРАНЯЕМ В БАЗУ ФАМИЛИЮ ПОЛЬЗОВАТЕЛЯ
                #         "phone_number": phone_number, #СОХРАНЯЕМ В БАЗУ ТЕЛЕФОН УЧЕНИКА
                #         # "description": description, 
                #         "role": "student", # И ДАЕМ СТАТУС УЧЕНИК
                #         } #

                data_student = {
                        "user_id": message.from_user.id, #СОХРАНЯЕМ В БАЗУ АЙДИ УЧЕНИКА
                        "username": message.from_user.username, #СОХРАНЯЕМ В БАЗУ ЮЗЕРНЕЙМ УЧЕНИКА
                        "first_name": message.from_user.first_name, #СОХРАНЯЕМ В БАЗУ НИК ПОЛЬЗОВАТЕЛЯ
                        "last_name": message.from_user.last_name, #СОХРАНЯЕМ В БАЗУ ФАМИЛИЮ ПОЛЬЗОВАТЕЛЯ
                        "phone_number": phone_number, #СОХРАНЯЕМ В БАЗУ ТЕЛЕФОН УЧЕНИКА
                        # "description": description,
                        "role": "student", # И ДАЕМ СТАТУС УЧЕНИК


                }

                # res = await http_async.user_save(data)
                res_student = await http_async.user_save(data_student)


                    
                if  res_student.status_code == 201:
                    await message.answer('Вы успешно прошли регистрацию\nДобро пожаловать!',reply_markup= get_keyboard_people("people") )
                else:
                    await message.answer('Ошибка регистрации\nПопробуйте еще раз',reply_markup= get_keyboard_teacher("registartion"))


                    




        elif message.text == 'Тех.поддержка💻': #ПРИ НАЖАТИИ НА КНОПКУ ТЕХ ПОДДЕРЖКА СРАБОТАЕТ ЭТОТ ДЕКОРАТОР
            async def support(message: types.Message):
                await message.answer('Уважаемый клиент, чтобы написать по поводу\nРекламы❗️\nЖалобы или предложения❗️\nВам нужно обратиться к https://t.me/stanley66')


    async def student(self, message: types.Message):
        if 'Заказать решение📚' in message.text:

            student = Student(message)

            await student.student_create(message)

        elif 'Мои заказы📊' in message.text:

            student = Student(message)
            
            await student.my_task(message)
        elif 'Активные заказы📈' in message.text:

            student = Student(message)
            
            await student.text_active_orders(message)

        elif 'Выполненные заказы📉' in message.text:

            student = Student(message)

            await student.text_done_orders(message)

        elif 'Статистика по заказам📊' in message.text:
            pass

        elif 'Решение верное' in message.text:
            student = Student(message)

            await student.decision_correct(message)

        elif 'Решение неверное' in message.text:
            student = Student(message)

            await student.decision_incorrect(message)

        elif 'Назад🔙' in message.text:
            student = Student(message)

            await student.text_back(message)

        else:
            print(student)


    

    async def teacher(self,message:types.Message):
        if 'Заказы📚' in message.text:
            teacher = TeacherHandler(message)


            await teacher.teacher_create(message)


        elif 'Решить✍️' in message.text:
            teacher = TeacherHandler(message)

            await teacher.solve(message)

        elif 'Мои решения✉️' in message.text:
            teacher = TeacherHandler(message)

            await teacher.my_solutions(message)

        elif 'Статистика📝' in message.text:
            pass


        elif 'Отклонено цена💸' in message.text:
            pass

        elif 'Отклонено время на решения⏱' in message.text:
            pass

        elif 'Отклонено СПАМ🚫' in message.text:
            pass

        
        elif 'Ожидают решения' in message.text:
            teacher = TeacherHandler(message)

            await teacher.await_problems(message)

        elif 'Ожидают оплату' in message.text:
            teacher = TeacherHandler(message)

            await teacher.await_payment(message)


        elif 'Решенные задачи' in message.text:
            teacher = TeacherHandler(message)

            await teacher.solved_problems(message)

        elif 'Загрузить решение' in message.text:
            teacher = TeacherHandler(message)

            await teacher.post_task(message)
            
        elif 'Не могу решить' in message.text:
            teacher = TeacherHandler(message)

            await teacher.can_not_tasks(message)

        elif 'Оплачено' in message.text:
            teacher = TeacherHandler(message)

            await teacher.pay_order(message)

        elif 'Не оплачено' in message.text:
             teacher = TeacherHandler(message)

             await teacher.not_pay_order(message)

        
        elif 'Назад🔙' in message.text:
            teacher = TeacherHandler(message)

            await teacher.backs(message)

        else:
            print('teacher')