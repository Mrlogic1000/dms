from . import api
from ..extensions import mysql
from flask import jsonify,request
from . mydb import MySQLCRUD
import json
from . functions import gen_ip,generate_random_string
from . schema import DeviceSchema
from marshmallow import ValidationError
import re



@api.route('/devices', methods=["GET","POST"])
def devices():
    try:
        db = MySQLCRUD()
        if request.method == "GET":             
            devices = db.read('devices')                           
            db.close()            
            return jsonify(devices)
        
        if request.method == "POST": 
            values = request.get_json()
            values['user_id'] = 1
            
            schema = DeviceSchema()
            data = schema.load(request.get_json())
            cur =mysql.connection.cursor()
            cur.execute("select * from devices where ip = %s or mac = %s",[data['ip'],data['mac']])
            device = cur.fetchone()
            if device: 
                return jsonify({"message":f'device with {data['ip']} already exist'})
            print(data)
            db.create('devices',data)                      
            db.close()                
            return "device is updated successfully"                       
        
    
    except ValidationError as error:   
        print(error.messages)    
        return jsonify(error.messages)
   
            
    

@api.route('/device/<int:id>', methods=["GET","POST"])
def device(id):
    try:
        db = MySQLCRUD()
        if request.method == "GET":
            if id:
                device = db.read('devices',{'id':id})
                maintenance = db.read("maintenance",{"id":id})
                device["maintenance"]  = maintenance
                print(maintenance)                               
                db.close()

                if device:
                    return jsonify(device)
                return jsonify({'error':'No record found'})        
            
        if request.method == "POST" and request.is_json:           
            data = request.get_json()
            print(data)
            action = data.pop('action')
            id = data.pop('id')
            print(id)

            if action == "update":               
               schema = DeviceSchema()
               data = schema.load(request.get_json())               
               db.update('devices',data,{'id':int(id)})                         
               db.close()
               return jsonify({"message":"data updated successfully"})             
                      
            if action== 'delete':
                db.delete('devices',{'id':int(id)})
                db.close()                                
                return jsonify({"message":"Object is deleted successfully"})    
    except Exception as error:
        print(error)
        return jsonify({'error':'error'})


@api.route('/delete_device/<int:id>', methods=["GET","POST"])
def delete(id):
    try:
        if request.method == "GET":           
            return jsonify({"message":"The device deleted successfully"})
        return jsonify({"message":"The method is not supported"})
    except Exception as error:
       return jsonify({'error':error})
       



@api.route("/maintenance",methods = ["GET","POST"])
def maintenance():
    if request.method == "POST" and request.is_json:
        data = request.get_json()
        db = MySQLCRUD()
        db.create("maintenance",data)
    return jsonify({"maintenance link"})




@api.route('parameters')
def params(): 
    cur = mysql.connection.cursor()
    cur.execute("select ip from devices")
    db_ip = cur.fetchall() 
    ip2 = [j  for i in db_ip for j in i.values() if j is not None]   
   
    ip = []    
    ips = gen_ip("172.3.100.0/24")
    for i in ips:
        d= {}
        if i not in ip2:
            d['value'] = i
            d['label'] = i
            ip.append(d)       
    
    return jsonify(ip)


