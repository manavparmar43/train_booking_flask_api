from flask import  Blueprint, Response, jsonify, request,render_template
from flask_restful import Resource, Api
from .model import User
from flask_mail import Message
from .serializer import UserSerializer
from app import mail
from .token import *
user_bp=Blueprint('user',__name__,template_folder='templates')


class RegisterApi(Resource):
    def post(self):
        user=User.objects.filter(username=request.json['username'])
        if user:
            return jsonify({"Error-info": "your username  is already taken "})
        else:    
            first_name=request.json['first_name']
            last_name=request.json['last_name']
            username=request.json['username']
            email=request.json['email']
            password=request.json['password']
            
            user=User(first_name=first_name,last_name=last_name,username=username,email=email)
            user.get_password(password)
            user.save()

            token = encode_token(str(user.id))


            msg = Message(
                    'Verify Mail',
                    sender='manav.p@latitudetechnolabs.com',
                    recipients = [str(email),]
                )
            context = {
                'username': username,
                'token':token,
                'url': request.url_root
            }
    
            msg.html=render_template('Mail.html', context=context)
            mail.send(msg)    
            return jsonify("done")

class LoginView(Resource):
    def post(self):
        username=request.json['username']
        password=request.json['password']
        user=User.objects.get(username=username)
        if user and user.verify_password(password):
            if user.active is True:
                token = encode_token(str(user.id))

                data = {
                    'token': token,
                    'username': user.username,
                }

                return jsonify(data)
            else: 
                return jsonify({"Mail-info":"Verfiy account"})
        else:
            return jsonify({'Error-info':'Invalid input'})

@user_bp.route('/verify-mail', methods=['GET'])
def VerifyMail():
    token = request.args.get('token')


    user = decode_token(token)

    user = User.objects.get(id=user['user'])
    user.active = True 
    user.save()
    return jsonify({"Verified":"Your acc is verified"})


user_bp.add_url_rule('/register',view_func=RegisterApi.as_view('register'))
user_bp.add_url_rule('/login',view_func=LoginView.as_view('login'))
