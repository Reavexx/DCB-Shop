import random 

def get_response(message: str) -> str:
    p_message = message.lower() 

    if p_message == "hallo":
        return 'Guten Tag!'
    
    if message == 'roll':
        return str(random.randint(1, 6))
    
    if p_message == '?help':
        return '`Das ist eine Hilfestellung.`'
    
    
    return ''