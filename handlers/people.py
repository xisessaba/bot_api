################################################################################
#                                                                              #
#                                ФАЙЛ УЧЕНИКА                                  #
#                                                                              #
#                                                                              #
################################################################################


from aiogram import types, Dispatcher
from keyboards import get_keyboard_people
from aiogram.types import ReplyKeyboardRemove 
from create_bot import bot, dp
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from create_bot import http_api
from handlers import http_async


import requests


#СОЗДАЕМ КЛАСС TASK ДЛЯ ХРАНЕНИЯ ДАННЫХ О ЗАДАНИИ

class Student:
    def __init__(self, message: types.Message):
        self.bot = bot
        self.message = message

    async def student_create(self, message: types.Message):
        

        class Task(StatesGroup):
            grade = State()  #state для хранения класса
            subject = State() #state для хранения предмета
            price = State() #state для хранения цены
            time = State() #state для хранения даты
            photo =State() #state для хранения фото


        await Task.grade.set() #ПЕРЕДАЕМ В СЛОВАРЬ
        await message.reply("Выберите класс:", reply_markup=get_keyboard_people("grade"))

                        




        @dp.message_handler(state=Task.grade) #ФУНКЦИЯ ХРАНЕНИЯ КЛАССА
        async def load_class(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['grade'] = message.text
                await Task.next() 
                await message.reply("Выберите Предмет📚:", reply_markup=get_keyboard_people("subject", message.text))



        @dp.message_handler(state=Task.subject) #ЗДЕСЬ МЫ СОХРАНЯЕМ ПРЕДМЕТ
        async def load_subjects(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['subjects'] = message.text
            await Task.next()
            await message.reply('Введите вашу цену (стандартная цена - 200 тг)', reply_markup=ReplyKeyboardRemove())


        @dp.message_handler(state=Task.price) #ЗДЕСЬ МЫ СОХРАНЯЕМ ЦЕНУ
        async def load_price(message: types.Message, state: FSMContext):
            try:
                async with state.proxy() as data:
                    data['price'] = int(message.text)
                await Task.next()
                await message.reply('Введите время, за которое нужно решить задание.')
            except ValueError: #ЕСЛИ ПОЛЬЗОВАТЕЛЬ ОТПРАВИТ ЦЕНУ С СИМВОЛОМ ОТПРАВИТСЯ ЭТО СООБЩЕНИЕ
                await message.reply("Вы ввели не число, попробуйте еще раз.")


        @dp.message_handler(state=Task.time) #ЗДЕСЬ МЫ ХРАНИМ ВРЕМЯ
        async def load_time(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['time'] = message.text
            await Task.next()
            await message.reply('Загрузите задачу.')


        @dp.message_handler(content_types=['photo'], state=Task.photo) #ЗДЕСЬ МЫ ХРАНИМ ФОТО
        async def load_photo(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['photo'] = message.photo[0].file_id #ФОТО БУДЕМ ХРАНИТЬ НА СЕРВЕРЕ ТЕЛЕГРАММА
                # new_photo = bot.download_file(data['photo'].file_path)
            await Task.next()

            data = await state.get_data() #ПОЛУЧАЕМ ВСЕ ДАННЫЕ ИЗ СЛОВАРЯ КОТОРЫЙ ВВЕЛ ПОЛЬЗОВАТЕЛЬ И СОХРАНЯЕМ В БАЗЕ
            grade = data.get('grade') 
            subject = data.get('subjects')
            price = data.get('price')
            time = data.get('time')
            photo = data.get('photo')
            data_result = {
                "price": price,
                "user": message.from_user.id,
                "subject": subject,
                "photo": photo,

                # "data_to_complete": time,
                }
            await message.answer(f"Класс: {grade}\nПредмет: {subject}\nЦена: {price}\nВремя на решения: {time}") #ОТПРАВЛЯЕМ ПОЛЬЗОВАТЕЛЮ ПОЛУЧЕННЫЕ ДАННЫЕ


            res = await http_async.order_save(data_result) #ОТПРАВЯЛЕМ ЗАПРОС ЧТО БЫ СОХРАНИТЬ ДАННЫЕ 

            if res.status_code == 201: # ЕСЛИ ЗАПРОС ОТПРАВИТСЯ БЕЗ ОШИБОК ОТПРАВИТСЯ ЭТО СООБЩЕНИЕ
                await message.reply('Задание успешно загружено!', reply_markup=get_keyboard_people("people"))
            else: # ЕСЛИ ЗАПРОС ВЫЗВАЛ ОШИБКУ СРАБОТАЕТ ЭТО СООБЩЕНИЕ
                await message.reply('Что-то пошло не так, попробуйте еще раз.', reply_markup=get_keyboard_people("people"))
            to_send_teachers = requests.get(f'{http_api}/telegram-user/?role=teacher').json() #ПОЛУЧАЕМ СПИСОК УЧИТЕЛЕЙ
            print(to_send_teachers)

            for to_send in to_send_teachers: # СОЗДАЕМ ЦИКЛ ЧТОБЫ НАЙТИ ДАННЫЕ УЧИТЕЛЯ В МАССИВЕ                        # ОТПРАВЛЯЕМ УВЕДОМЛЕНИЕ УЧИТЕЛЮ О НОВОМ ЗАКАЗЕ
                
                await bot.send_photo(to_send['user_id'], photo, caption=f'Есть новый заказ: {res.json()["order_id"]}')

                




            await state.finish() #ОЧИЩАЕМ СЛОВАРЬ
        




    async def my_task(self, message: types.Message):
        await message.answer("Мои заказы📊", reply_markup=get_keyboard_people("active_orders"))



    async def text_active_orders(self, message: types.Message):
        await message.answer("Активные заказы📈", reply_markup=get_keyboard_people("active_orders"))  
        my_orders = requests.get(f'{http_api}/order-list/?user__user_id={message.from_user.id}&order_process__status=in_progress').json() # ОТПРАВЛЯЕМ ЗАПРОС И ПОЛУЧАЕМ СПИСОК ЗАКАЗОВ ПОЛЬЗОВАТЕЛЯ С СТАТУСОМ НА ПРОВЕРКЕ 

        if my_orders: # С ПОМОЩЬЮ УСЛОВИЯ ПРОВЕРЯЕМ ЕСТЬ ЛИ ЗАКАЗЫ ПОЛЬЗОВАТЕЛЯ СО СТАТУСОМ НА ПРОВЕРКЕ
            for my_order in my_orders:
                print(my_orders)

                await bot.send_photo(message.from_user.id, my_order['photo'], caption=f'Ваш заказ: {my_order["id"]}\nПредмет: {my_order["subject"]["subject"]}\nЦена: {my_order["price"]}')
        else: # ЕСЛИ ЗАКАЗОВ НЕТ ТО ВЫВОДИМ СООБЩЕНИЕ
            await message.answer("У вас нет заказов", reply_markup=get_keyboard_people("active_orders"))    



    






    async def text_done_orders(self, message: types.Message):

        my_orders = requests.get(f'{http_api}/order-list/?user__user_id={message.from_user.id}&order_process__status=on_check').json() # ОТПРАВЛЯЕМ ЗАПРОС И ПОЛУЧАЕМ СПИСОК ЗАКАЗОВ ПОЛЬЗОВАТЕЛЯ С СТАТУСОМ НА ПРОВЕРКЕ 

        await message.answer("Выполненные заказы📉", reply_markup=get_keyboard_people("active_orders_2"))

        if my_orders: # С ПОМОЩЬЮ УСЛОВИЯ ПРОВЕРЯЕМ ЕСТЬ ЛИ ЗАКАЗЫ ПОЛЬЗОВАТЕЛЯ СО СТАТУСОМ НА ПРОВЕРКЕ
            for my_order in my_orders:
                print("---")
                print(my_order)
                await bot.send_photo(message.from_user.id, my_order['photo'], caption=f'Ваш заказ : {my_order["id"]}\nx')
                for order_process in my_order['order_process']:
                    #    await bot.send_message(message.from_user.id,f'Решение заказа: {my_order["id"]}', reply_markup=get_keyboard_people("active_orders_2"))

                
                        await bot.send_photo(message.from_user.id, order_process['photo'], caption=f'Решение заказа: {my_order["id"]}\nПредмет: {my_order["subject"]["subject"]}')
        else: # ЕСЛИ ЗАКАЗОВ НЕТ ТО ВЫВОДИМ СООБЩЕНИЕ
            await message.answer("У вас нет заказов", reply_markup=get_keyboard_people("people"))
            

        # @dp.message_handler(text = "Решение верное") # ПРИ НАЖАТИИ НА КНОПКУ РЕШЕНИЕ ВЕРНОЕ СРАБОТАЕТ ЭТО ФУНКЦИЯ
    async def decision_correct(self,message: types.Message):
        class OrderProcess(StatesGroup):
            order_process_id = State()
            order_process_status_id = State()
        await OrderProcess.order_process_id.set()
        await message.answer("Введите номер заказа!", reply_markup=ReplyKeyboardRemove())

        @dp.message_handler(state=OrderProcess.order_process_id)
        async def decision_create(message: types.Message, state: FSMContext):
            async with state.proxy() as order_process_status:
                order_process_status['order_process_id'] = message.text
            data_result = await state.get_data()
            order_process_id = data_result.get('order_process_id')
            
            order_status_done = requests.patch(f'{http_api}/order-process/{11}/', {'order_id': order_process_id, 'status':'done'})

            if order_status_done.status_code == 202:
                await message.answer("Заказ успешно выполнен!", reply_markup=get_keyboard_people("people"))
                await state.finish()

            else:
                await message.answer("Заказ не найден!", reply_markup=get_keyboard_people("active_orders"))
                await state.finish()
                

        # @dp.message_handler(text = "Решение неверное") # НЕ НАСТРОЕНО ЕЩЕ , НО ТУТ МЫ ОТПРАВИМ ЗАПРОС И ПОМЕНЯЕМ СТАТУС ЗАКАЗА АРБИТРАЖ
    async def decision_incorrect(self,message: types.Message):
        class OrderProcess(StatesGroup):
            order_process_id = State()
            order_process_status_id = State()
        await OrderProcess.order_process_status_id.set()
        await message.answer("Введите номер заказа!", reply_markup=ReplyKeyboardRemove())

        @dp.message_handler(state=OrderProcess.order_process_status_id)
        async def order_process_func(message: types.Message, state: FSMContext):
            async with state.proxy() as order_process_status:
                order_process_status['order_process_status_id'] = message.text
            data_result = await state.get_data()
            order_process_status_id = data_result.get('order_process_status_id')
            
            
            order_status_arbitrage = requests.patch(f'{http_api}/order-process/{11}/', {'order_id': order_process_status_id, 'status':'dispute'})

            if order_status_arbitrage.status_code == 202:
                await message.answer("Мы сожалеем, что не смогли вам помочь.\nЗадание отправится в статус Арбитраж и в течении дня вам вернут деньги)", reply_markup=get_keyboard_people("active_orders"))
                await state.finish()

            else:
                await message.answer("Вы ввели неправильный номер заказа\nПопробуйте еще раз", reply_markup=get_keyboard_people("active_orders"))
                await state.finish()
            


        # @dp.message_handler(text = "Статистика по заказам📊") #Здесь мы выведем всю стату ученика
    async def text_statistic_orders(self,message: types.Message):
        await message.answer("Статистика по заказам📊", reply_markup=get_keyboard_people("active_orders_2"))




        # @dp.message_handler(text = "Назад🔙")
    async def text_back(self,message: types.Message):
        await message.answer("Вы вышли в главное меню!", reply_markup=get_keyboard_people("people"))




      
            


            





