from flask import Flask
from mongoengine import *
from flask_mongoengine import MongoEngine
from flask_marshmallow import Marshmallow
from flask_mail import Mail
db=MongoEngine()

app=Flask(__name__)


app.config['MONGODB_SETTINGS'] = {
    'db': 'Train_management_system',
    'host': 'mongodb+srv://dhruvanshu1775:17753690d@cluster0.u8vtird.mongodb.net/Train_management_system'
}



db.init_app(app)

ma = Marshmallow(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'manav.p@latitudetechnolabs.com'
app.config['MAIL_PASSWORD'] = 'parmar@96'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


from user.view import user_bp
from train_book.view import train_blueprint

app.register_blueprint(user_bp)
app.register_blueprint(train_blueprint)
