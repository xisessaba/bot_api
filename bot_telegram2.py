################################################################################
#                                                                              #
#                           БОТ ВКЛЮЧАЕТСЯ ЗДЕСЬ!!!!                           #
#                                                                              #
#                                                                              #
################################################################################


from aiogram.utils import executor
from create_bot import dp
from handlers.menu import BotMain

async def on_startup(_):
    print('Бот вышел в онлайн без ошибок')

BotMain(dp)


if __name__ == '__main__':
    
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
