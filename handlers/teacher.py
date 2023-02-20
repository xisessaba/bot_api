################################################################################
#                                                                              #
#                                ФАЙЛ УЧИТЕЛЯ                                  #
#                                                                              #
#                                                                              #
################################################################################



from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove 
from create_bot import bot, dp
from create_bot import http_api
from keyboards import get_keyboard_teacher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import requests


class TeacherHandler:
    def __init__(self, message: types.Message):
        self.dp = dp
        self.bot = bot
        self.message = message
        self.http_api = http_api
    
    async def teacher_create(self, message: types.Message):

        class Teacher(StatesGroup):
            # order_id = State()
            grade = State()
            subject = State()
            order_id = State()
            order_id2 = State()
            photo = State()



        

       
                # checker_orders_list = requests.get(f"{http_api}/order-process/").json()
                # print(checker_orders_list)

                # for checker_order in checker_orders_list :
                #     teacher_id = message.from_user.id

                #     if checker_order['doer']['user_id'] == teacher_id and checker_order['status'] == 'in_progress' or checker_order['status'] == 'on_check':
                #         await bot.send_message(message.from_user.id, "Нет уш, сначала выполни предыдущий заказ, а потом уже берись за новое задание", reply_markup=get_keyboard_teacher("menu_teacher"))
                

                    # else:
        await Teacher.grade.set() #СОХРАНЯЕМ ДАННЫЕ В СЛОВАРЬ
        await message.answer("Выберите класс для поиска🔎", reply_markup=get_keyboard_teacher("grade")) #ВЫВОДИМ КЛАВИАТУРУ КЛАССОВ
        @dp.message_handler(state=Teacher.grade) #ФУНКЦИЯ ХРАНЕНИЯ ДАННЫХ ПОЛЬЗОВАТЕЛЯ
        async def load_class(message: types.Message, state: FSMContext):
            async with state.proxy() as data:
                data['grade'] = message.text
                await Teacher.next() #УСПЕШНО СОХРАНИЛИ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ И ИДЕМ ДАЛЬШЕ
                await message.reply("Выберите предмет для поиска🔎", reply_markup=get_keyboard_teacher("subject", message.text)) #ВЫВОДИМ КЛАВИАТУРУ ПРЕДМЕТОВ


        @dp.message_handler(state=Teacher.subject) #ФУНКЦИЯ ХРАНЕНИЯ ДАННЫХ ПОЛЬЗОВАТЕЛЯ, А ИМЕННО ПРЕДМЕТА
        async def save_subject(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    data['subject'] = message.text
                data_result = await state.get_data()
                #ИЗ ПЕРЕМЕННОЙ SUBJECT СДЕЛАЕМ ГЛОБАЛЬНУЮ ПЕРЕМЕННУЮ 
                global subject
                

                subject = data_result.get('subject')
            
                

                random_subject = requests.get(f'{http_api}/random-order/{subject}/') #ЗАПРОС НА СЕРВЕР ПО УКАЗАННЫМ ДАННЫМ
                                


                if random_subject.status_code == 200: #ПРОВЕРЯЕМ ЕСТЬ ЛИ ЗАКАЗЫ В БАЗЕ
                    random_subject = random_subject.json()
                    print(random_subject)
                    capt = f"Номер заказа: {random_subject['id']} \nПредмет: {random_subject['subject']['subject']} класс. \nЦена: {random_subject['price']}"
                    

                    await bot.send_photo(message.chat.id, random_subject['photo'], caption=capt, reply_markup=get_keyboard_teacher("orders"))
                elif random_subject.status_code == 404: # ЕСЛИ ЗАКАЗОВ НЕТ ВЫВОДИМ ЭТОТ ТЕКСТ
                    await message.answer("Заказов нет",reply_markup=get_keyboard_teacher("menu_teacher") )
                    print('----')

                await state.finish()


    async def solve(self, message: types.Message):
        print('fds')
        random_subject = requests.get(f'{http_api}/random-order/{subject}/')
        random_subject = random_subject.json()
        random_subject_id = random_subject['id']
        data_to = {
                    'doer': message.from_user.id, #СОХРАНЯЕМ АЙДИ РЕШАТЕЛЯ
                    'order': random_subject_id, #СОХРАНЯЕМ АЙДИ ЗАКАЗА
                    'status': 'in_progress', #МЕНЯЕМ СТАТУС НА ПРОВЕРКЕ
                    
                }
        res_go = requests.post(f'{http_api}/order-process/', data=data_to)  #ОТПРАВЛЯЕМ ЗАПРОС НА СЕРВЕР

        print(res_go)

        if res_go.status_code == 201: #УСЛОВИЕ УСПЕШНО ЛИ ОТПРАВИЛИ ЗАПРОС НА СЕРВЕР
            res_go = res_go.json()

            await message.answer("Вы успешно взяли заказ👍\nЗайдите в Ожидают оплату чтобы подтвердить заказ", reply_markup=get_keyboard_teacher("menu_teacher"))
            message_student = requests.get(f'{http_api}/order-process/').json()

            for trages in message_student:
                student_id = trages['order']['user']['user_id']
                phone_number = trages['order']['user']['phone_number']

            await bot.send_message(chat_id=student_id, text= f'Учитель: {message.from_user.first_name} взял ваш заказ\nОплатите заказ по номеру: {phone_number}\nПодтвердите заказ написав команду /payment')

        else:
            await message.answer("Не удалось сделать заказ", reply_markup=get_keyboard_teacher("menu_teacher"))

    

        



            
                    
    async def my_solutions(self, message: types.Message):
        await bot.send_message(message.from_user.id, f"Что хотите сделать {message.from_user.first_name}?", reply_markup=get_keyboard_teacher("my_solutions"))


    async def solved_problems(self, message: types.Message):

        my_orders = requests.get(f"{http_api}/order-process/").json()

        for order in my_orders:
            msg_task = f"Номер заказа: {order['order']['id']}\nЗаказчик: {order['order']['user']['first_name']}\nТелефон заказчика: {order['order']['user']['phone_number']}"
            if order['doer']['user_id']  == message.from_user.id and order['status'] == 'done':
                await bot.send_photo(message.from_user.id, order['order']['photo'], caption= msg_task, reply_markup=get_keyboard_teacher("my_solutions"))
                    # else:
                    #     await bot.send_message(message.from_user.id, "У вас нет решенных задач", reply_markup=get_keyboard_teacher("my_solutions"))



    async def await_payment(self, message: types.Message): #ЗДЕСЬ МЫ ВЫВОДИМ ЗАКАЗ КОТОРЫЙ ВЗЯЛИ , НО ЕГО ЕЩЕ НЕ ОПЛАТИЛИ
        my_orders = requests.get(f"{http_api}/order-process/").json()

        for orders_payment in my_orders:
            print(orders_payment)
            if orders_payment ['doer']['user_id'] == message.from_user.id and orders_payment['payment'] == 'not_paid' and orders_payment['status'] == 'in_progress':
                msg_payment = f"Номер заказа: {orders_payment['order']['id']}\nЗаказчик: {orders_payment['order']['user']['first_name']}\nТелефон заказчика:{orders_payment['order']['user']['phone_number']}"
                await bot.send_photo(message.from_user.id, orders_payment['order']['photo'], caption= msg_payment, reply_markup=get_keyboard_teacher("payment"))
            # else:
            #     await bot.send_message(message.from_user.id, "Вы еще не взяли ни одного заказа.\nНовый заказ можете взять в 'Заказы📚'", reply_markup=get_keyboard_teacher("my_solutions"))

            
                    



            





    async def await_problems(self, message:types.Message): # ПРИ НАЖАТИИ НА КНОПКУ ОИЖДАЮТ РЕШЕНИЯ ВЫВОДИМ КЛАВИАТУРУ ЗАГРУЗИТЬ РЕШЕНИЕ

        my_order = requests.get(f'{http_api}/order-process/').json()

        for my_orders_status_in_progress in my_order:
            print(my_orders_status_in_progress)
            if my_orders_status_in_progress ['doer']['user_id'] == message.from_user.id and my_orders_status_in_progress ['payment'] == 'paid' and my_orders_status_in_progress['status'] == 'in_progress': #ПРОВЕРЯЕМ ПО АЙДИ ЕСТЬ ЛИ У РЕШАТЕЛЯ ОПЛАЧЕННЫЕ ЗАДАЧИ
                msg = f"Номер заказа: {my_orders_status_in_progress ['order']['id']}\nЗаказчик: {my_orders_status_in_progress['order']['user']['first_name']}\nТелефон заказчика: {my_orders_status_in_progress['order']['user']['phone_number']}"
                await bot.send_photo(message.from_user.id, my_orders_status_in_progress['order']['photo'],  caption= msg,reply_markup=get_keyboard_teacher("download")) #ВЫВОДИМ НУЖНЫЕ ДАННЫЕ О ЗАКАЗЕ

    


                    
    async def statistic(self, message:types.Message): #ЗДЕСЬ МЫ ВЫВОДИМ ВСЮ СТАТИСТИКУ УЧИТЕЛЯ ВСЕ ЗАРАБОТАННЫЕ ДЕНЬГИ, СКОЛЬКО ЗАДАНИЙ ОН РЕШИЛ И Т.Д
        my_stat = requests.get(f'{http_api}/order-statistics/{11}/')
        if my_stat.status_code == 200:
            my_stat = my_stat.json()
            await bot.send_message(message.from_user.id, f"Ваша статистика:\n\nЗаработано: {my_stat['total_earned']}\nВыполнено заказов: {my_stat['total_orders']}\nВыполнено заданий: {my_stat['total_tasks']}\nСредняя оценка: {my_stat['average_rating']}", reply_markup=get_keyboard_teacher("menu_teacher"))
        else:
            await bot.send_message(message.from_user.id, "Ваша статистика пуста!\nВы еще не сделали ни одного заказа!", reply_markup=get_keyboard_teacher("menu_teacher"))




                    
                    
        


    async def back(self, message:types.Message):# ОТПРАВЛЯЕМ В МЕНЮ ПРИ НАЖАТИИ НА НАЗАД
        await bot.send_message(message.from_user.id, "Вы вернулись в меню", reply_markup=get_keyboard_teacher("menu_teacher"))

    async def post_task(self, message:types.Message): # ПРИ НАЖАТИИ НА КНОПКУ ЗАГРУЗИТЬ РЕШЕНИЕ ВЫВОДИМ КЛАВИАТУРУ С ФОТОГРАФИЕЙ

        class PostTask(StatesGroup):
            photo = State()


        post_order = requests.get(f"{http_api}/order-process/").json()

        for post_orders in post_order:
            if post_orders['doer']['user_id'] == message.from_user.id and post_orders['payment'] == 'paid' and post_orders['status'] == 'in_progress':
                order_post_id = post_orders['order']['id']

                
                await PostTask.photo.set() #СОЗДАЕМ СЛОВАРЬ
                await message.answer("Загрузите решение:", reply_markup=ReplyKeyboardRemove()) 
                
                @dp.message_handler(content_types=['photo'], state=PostTask.photo) #СОХРАНЯЕМ РЕШЕНИЕ ЗАКАЗА
                async def load_photo(message: types.Message, state: FSMContext):
                    async with state.proxy() as data:
                        data['photo'] = message.photo[0].file_id
                    data_result = await state.get_data()
                    photo = data_result.get('photo')

                    
                    my_order = requests.patch(f'{http_api}/order-process/{11}/', {'order_id': order_post_id, 'photo': photo, 'status':'on_check'}) #ОТПРАВЛЯЕМ ПАТЧ ЗАПРОС НА СЕРВЕР

                    if my_order.status_code == 202: #ПРОВЕРЯЕМ НЕТ ЛИ ОШИБОК ПРИ ОТПРАВКЕ ЗАПРОСА
                        await message.answer("Вы успешно загрузили решение👍", reply_markup=get_keyboard_teacher("menu_teacher"))
                        await state.finish()
                        

                    else:
                        await message.answer("Что-то пошло не так😕", reply_markup=get_keyboard_teacher("menu_teacher"))
                        await state.finish()
                    my_order = my_order.json()
                    print(my_order)
                    await bot.send_photo(my_order['order_user_id'], photo, caption='Учитель выполнил ваш заказ\nМожете посмотреть в Мои заказы📊') #ОТПРАВЯЛЕМ УВЕДОМЛЕНИЕ УЧЕНИКУ О ТОМ ЧТО ЗАКАЗ ВЫПОЛНЕН
                    await state.finish() #ОЧИЩАЕМ СЛОВАРЬ

            else:
                await message.answer("Вы не можете загрузить решение, так как у вас нет активных заказов🤷‍♂️", reply_markup=get_keyboard_teacher("menu_teacher"))
                                
            
    async def can_not_tasks(self, message:types.Message): #ПРИ НАЖАТИИ НА КНОПКУ ПОДАТЬ ЖАЛОБУ ВЫВОДИМ КНОПКУ ПОДТВЕРЖДЕНИЯ
        post_order_dispute = requests.get(f"{http_api}/order-process/").json()

        for post_orders in post_order_dispute:
            if post_orders['doer']['user_id'] == message.from_user.id and post_orders['payment'] == 'paid' and post_orders['status'] == 'in_progress':
                order_id_dispute= post_orders['order']['id']


            order_status_arbitrage = requests.patch(f'{http_api}/order-process/{11}/', {'order_id': order_id_dispute, 'status':'dispute'}) #ПО АЙДИ ЗАКАЗА МЕНЯЕМ ЕГО СТАТУС


            if order_status_arbitrage.status_code == 202:
                await message.answer("Спасибо, что попытались. Нас Арбитражник попробует решить проблему ", reply_markup=get_keyboard_teacher("menu_teacher"))

            else:
                await bot.send_message(message.from_user.id, "Упс, что-то пошло не так\nПопробуйте еще раз", reply_markup=get_keyboard_teacher("my_solutions_2"))



                
            
    async def pay_order(self, message:types.Message):
        my_payment_orders = requests.get(f'{http_api}/order-process/').json()

        for order_payment in my_payment_orders:
            if order_payment['doer']['user_id'] == message.from_user.id and order_payment['payment'] == 'not_paid' and order_payment['status'] == 'in_progress':
                order_payment_id = order_payment['order']['id']

                res = requests.patch(f'{http_api}/order-process/{11}/', {'order_id': order_payment_id, 'payment':'paid'}) #ПО АЙДИ ЗАКАЗА МЕНЯЕМ ЕГО СТАТУС

                if res.status_code == 200 or res.status_code == 202:
                        await message.answer("Заказ оплачен.\nПриступайте к работе", reply_markup=get_keyboard_teacher("menu_teacher"))
            

                else:
                    await message.answer("Упс, что-то пошло не так\nПопробуйте еще раз", reply_markup=get_keyboard_teacher("menu_teacher"))

            else:
                await message.answer("У вас нет заказов для оплаты", reply_markup=get_keyboard_teacher("menu_teacher"))
    async def not_pay_order(self, message:types.Message):
        await message.answer("Подождите пока оплатят заказ.\nЕсли прошло больше одного дня и оплата до сих пор не пришла нажмите на кнопку Тех поддержка", reply_markup=get_keyboard_teacher("menu_teacher"))


    async def backs(self, message:types.Message):
        await message.answer("Вы вернулись в меню", reply_markup=get_keyboard_teacher("menu_teacher"))