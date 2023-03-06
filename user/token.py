import jwt
from flask import Response, jsonify
from flask import request
import datetime 
from datetime import timezone


def encode_token(id):
    token = jwt.encode(
        {'user':id,"exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(hours=24)}, "secret", algorithm="HS256")
    return token
   


def decode_token(token):
    try:
        token = jwt.decode(token, "secret", algorithms=["HS256"])    
        return token
    except:
        return False



        