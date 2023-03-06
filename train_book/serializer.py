from app import ma
from user.model import User
from .model import *
from user.serializer import *
from marshmallow import *


class TrainSerializer(ma.Schema):
    id=ma.String()
    class Meta:
        model = TrainManagement
        fields = ('id','pick_up_point','droping_point','departure_date','departure_time','drop_date','drop_time','duration_hours',
        'seat','available','price','train_class','train_type','is_deleted')
 
class BookTicketSerializer(ma.Schema):
    id=ma.String()
    book_detail=ma.Nested(TrainSerializer(only=('pick_up_point','droping_point','departure_date','departure_time','drop_date','drop_time','duration_hours',
        'seat','available','price','train_class','train_type')))
    user=ma.Nested(UserSerializer())
    class Meta:
        model=BookTickets
        fields = ('id','pick_up_point','droping_point','book_seat','payment','book','user','book_detail') 

class RoutesSerializer(ma.Schema):
    class meta:
        model=Routes
        fields=('id','pick_up_point','droping_point','routes')  

  

class CancleTicketSerializer(ma.Schema):
    id=ma.String()
    book_detail=ma.Nested(TrainSerializer())
    user=ma.Nested(UserSerializer())
    class Meta:
        model=CancleTickets
        fields = ('id','book_detail','user','cancle_ticket_price','return_payment_time')