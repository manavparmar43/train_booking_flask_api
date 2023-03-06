from flask import Flask, request, jsonify, make_response, Response
from functools import wraps
from .model import User
from .token import *


def token_required(f):


    @wraps(f)
    def decorated( *args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return Response('Token is Missing', status=401)
  
        try:
            user = decode_token(token)

            request.user = user

            if user is False:
                return Response('Token is Expire',401)
        
        except:
            return Response('Token is Invalid',401)

        return f( *args, **kwargs)
  
    return decorated