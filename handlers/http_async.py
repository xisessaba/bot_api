import requests

from create_bot import http_api

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}



async def user_save(data):
    b = requests.post(f'{http_api}/telegram-user/', headers=HEADERS, json=data)
    return b

async def student_save(data):
    b = requests.post(f'{http_api}/student/', headers=HEADERS, json=data)
    return b

async def teacher_save(data):
    b = requests.post(f'{http_api}/teacher/', headers=HEADERS, json=data)
    return b
    


async def order_save(data_result):
    b = requests.post(f'{http_api}/order/', headers=HEADERS, json=data_result)
    return b


        