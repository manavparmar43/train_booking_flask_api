from app import ma
from .model import User



class UserSerializer(ma.Schema):
    class Meta:
        fields = ('id','first_name','last_name','username','email','password','is_superuser') 