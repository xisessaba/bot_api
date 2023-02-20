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
TOKEN= '5987242833:AAFB28GqCnOKZaOScPAyTCKA-kEWd6_eYzQ'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

http_api = 'http://192.168.31.161:8000'


