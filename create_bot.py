################################################################################
#                                                                              #
#                        ТОКЕН И САМ БОТ ХРАНИТСЯ ЗДЕСЬ                        #
#                                                                              #
#                                                                              #
################################################################################


from aiogram import Bot
from aiogram.dispatcher import  Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()
TOKEN= 'Ваш токен'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

http_api = 'Ваш айпи'


