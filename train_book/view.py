from flask import  Blueprint, Response, jsonify, request,render_template
from .model import *
from .serializer import *
from flask_restful import Resource, Api
from datetime import datetime
from user.decorator import token_required
from app import mail
from flask_mail import Message
train_blueprint = Blueprint('train',__name__,template_folder='templates/')
api = Api(train_blueprint)
class TrainManagementApi(Resource):
    def get(self):
        train_data=TrainManagement.objects.filter(is_deleted=False)
        if train_data:
            train_management_schema=TrainSerializer(many=True)
            data=train_management_schema.dumps(train_data)
            return Response(data)
        else:
            return jsonify({"Error":"No Train Recordes"})
    def post(self):    
        departure_time=datetime.strftime(datetime.strptime(request.json['departure_time'], "%H:%M"),"%I:%M %p")
        drop_time=datetime.strftime(datetime.strptime(request.json['drop_time'], "%H:%M"),"%I:%M %p")
        departure_time_obj= datetime.strptime(request.json['departure_time'], '%H:%M').time()
        departure_date_obj=datetime.strptime(str(request.json['departure_date']), "%Y/%m/%d")
        drop_time_obj= datetime.strptime(request.json['drop_time'], '%H:%M').time()
        drop_date_obj=datetime.strptime(str(request.json['drop_date']), '%Y/%m/%d')
        com_deperture_date_time=datetime.combine(departure_date_obj, departure_time_obj)
        com_drop_date_time=datetime.combine(drop_date_obj, drop_time_obj)
        duration_hours=str(com_drop_date_time - com_deperture_date_time)

        train_data=TrainManagement(train_number=request.json['train_number'],
        departure_date=departure_date_obj,duration_hours=duration_hours,departure_time=departure_time,drop_date=drop_date_obj,
        drop_time=drop_time,seat=request.json['seat'],price=request.json['price'],train_class=request.json['train_class'],train_type=request.json['train_type'])
        train_data.save()
        return jsonify({"Success":"Train Added Succesfully...."})

class RoutesApi(Resource):
    def get(self):
        routes=Routes.objects.all()
        if routes:
            routes_schema=RoutesSerializer.dumps(routes)
            return Response(routes_schema)  
        else:
            return jsonify({"Error-list:No Record found"}) 
    def post(self):
            pick_up_point=request.json['pick_up_point']
            droping_point=request.json['droping_point']
            routes=request.json['routes']
            data=Routes.objects.filter(pick_up_point=pick_up_point,droping_point=droping_point)
            if data:
 
                return jsonify({"Error-list":"This Route already added"})      
            else:
                
                routes_data=Routes(pick_up_point=pick_up_point,droping_point=droping_point,routes=routes)
                routes_data.save()
                return jsonify({"Success":"Record added successfully"})    




class TrainRouteApi(Resource):
    def post(self):
        routes=TrainRoutes.objects.filter(train=request.json['train'])
        if routes:
            return jsonify({"Error-info":"Train already added..."})
        else:
            train=request.json['train']
            route=request.json['routes']
            traveling_routes=TrainRoutes(routes=route,train=train)
            traveling_routes.save()
            return jsonify({"Success":"Train and route added successfully..."})


class BookTicketApi(Resource):
    method_decorators = [token_required]
    def post(self):
        travel_route=TrainRoutes.objects.get(train=request.json['train'])
        user=User.objects.get(id=request.user['user'])
        if user and travel_route :
            train_data=TrainManagement.objects.get(id=request.json['train'])
            print(train_data)
            if int(train_data.seat) >= int(request.json['book_seat']):
                seat=int(train_data.seat)-int(request.json['book_seat'])
                if seat == 0:
                    train_data.available=False
                train_data.seat=str(seat)
                train_data.save()    
                book_seat=request.json['book_seat']
                payment=str(int(request.json['book_seat']) * (int(travel_route.train.price)/int(travel_route.train.seat)))
                book_ticket=BookTickets(book_seat=book_seat,payment=payment,user=user,book_detail=travel_route)
                book_ticket.save()
                msg = Message(
                        'Verify Mail',
                        sender='manav.p@latitudetechnolabs.com',
                        recipients = [str(user.email),]
                    )
                context = {
                    'username': user.username,
                    'email':user.email,
                    'routes':travel_route.routes.routes,
                    'pickup_point':travel_route.routes.pick_up_point,
                    'drop_point':travel_route.routes.droping_point,
                    'pickup_time':travel_route.train.departure_time,
                    'pickup_date':travel_route.train.departure_date,
                    'drop_time':travel_route.train.drop_time,
                    'drop_date':travel_route.train.drop_date,
                    'train_number':travel_route.train.train_number,
                    'seat':book_seat,
                    'payment':payment,
                    'duration_hours':travel_route.train.duration_hours,
                }
    
                msg.html=render_template('book_ticket.html', context=context)
                mail.send(msg)  
                return jsonify({"success":"Your ticket will be confirmed and booking info send on your mail id"})     
            else:
                return jsonify({"Error-info":f"Seats is only {train_data.seat}"})
        else:
            if user is False:
                return jsonify({"Error-info":"User not found"})     
            else:
                return jsonify({"Error-info":"Something went wrong please try to another routes"})            
                 
api.add_resource(TrainManagementApi, '/train')
api.add_resource(BookTicketApi, '/book-ticket')
api.add_resource(RoutesApi,'/routes')
api.add_resource(TrainRouteApi,'/train-routes')
        

