from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
    meta={'collection':'user'}
    first_name=db.StringField(required=True)
    last_name=db.StringField(required=True)
    username=db.StringField(required=True,unique=True)
    email=db.StringField(required=True)
    active=db.BooleanField(default=False)
    is_superuser=db.BooleanField(default=False)
    password=db.StringField(required=True)

    def __repr__(self):
        return self.username
    
    def get_password(self,password):
        self.password = generate_password_hash(password)
        super(User, self).save()
    
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)