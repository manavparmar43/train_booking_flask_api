from app import db
from datetime import datetime
from user.model import User

class TrainManagement(db.Document):
    
    meta={'collection':'Train_Management'}

    train_class_choice = (
        ('AC-SEATER', 'AC-SEATER'),
        ('AC-SLEEPER', 'AC-SLEEPER'),
        ('NON-AC-SEATER', 'NON-AC-SEATER'),
        ('NON-AC-SLEEPER', 'NON-AC-SLEEPER'),
    )
    train_type_choice = (
        ('EXPRESS', 'EXPRESS'),
        ('LOCAL', 'LOCAL'),
    )
    train_number=db.StringField(required=True)
    departure_date=db.DateField(required=True)
    departure_time=db.StringField(required=True)
    drop_date=db.DateField(required=True)
    drop_time=db.StringField(required=True)
    duration_hours=db.StringField(required=True)
    seat=db.StringField(required=True)
    available=db.BooleanField(default=True)
    price=db.StringField(required=True)
    train_class=db.StringField(max_length=15, choices=train_class_choice, nullable=True)
    train_type=db.StringField(max_length=15, choices=train_type_choice, nullable=True)
    is_deleted=db.BooleanField(default=False)



class Routes(db.Document):
    meta={'collection':'Route'}
    pick_up_point=db.StringField(required=True)
    droping_point=db.StringField(required=True)
    routes=db.ListField(db.StringField())
class TrainRoutes(db.Document):
    meta={'collection':'Train_route'}
    routes=db.ReferenceField(Routes, nullabel=True)
    train=db.ReferenceField(TrainManagement, nullabel=True)


class BookTickets(db.Document):
    meta={'collection':'Book_Ticket'}
    book_seat=db.StringField(required=True)
    payment=db.StringField(required=True)
    book=db.BooleanField(default=True)
    cancle_ticket=db.BooleanField(default=False)
    user = db.ReferenceField(User, nullabel=True)
    book_detail=db.ReferenceField(TrainRoutes, nullabel=True)

class CancleTickets(db.Document):
    meta={'collection':'Cancle_Ticket'}
    user = db.ReferenceField(User, nullabel=True)
    book_detail=db.ReferenceField(TrainManagement, nullabel=True)
    cancle_ticket_price=db.StringField(required=True)
    return_payment_time=db.StringField(required=True)
