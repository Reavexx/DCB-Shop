import random

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == "hallo":
        return 'Guten Tag!'
    
    if message == 'roll':
        return str(random.randint(1, 6))

    if message.startswith('?front '):
        name = message.split('?front ')[1]
        return f'{name} du luschtige'

    if p_message == '?help':
        return '`Das ist eine Hilfestellung.`'

    return ''
