import datetime

import jwt

KEY = 'ingDLMRuGe9UKHRNjs7cYckS2yul4lc3';
ALGORITHM ='HS256';
        
def generate_token(data):
    exp = datetime.datetime.now() + datetime.timedelta(days=1)
    payload = {
        'exp': exp,
        'iat' : datetime.datetime.now()
    }
    payload.update(data)
    return {
        'token': jwt.encode(payload, KEY, ALGORITHM),
        'expires_in': int(exp.timestamp())
        }

def get_payload(token):
    try:
        return jwt.decode(token, KEY, [ALGORITHM] , options={'verify_exp': False})
    except Exception as e:
        return None

