#Extended.py
'''
    输入参数均为字符串
    输出也为字符串
'''

import requests
def add(x, y):
    return str(int(x)+int(y))

def weather(location):
    response=requests.get(f'https://wttr.in/{location}')
    if response.status_code==404:
        return 'City not found...'
    else:
        return response.text



