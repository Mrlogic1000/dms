from . import api
from ..extensions import mysql
from flask import jsonify,request
from . mydb import MySQLCRUD
import json


@api.route('/devices', methods=["GET","POST"])
def devices():
    try:
        db = MySQLCRUD()
        if request.method == "GET":             
            devices = db.read('devices')
            datas = []
            for device in devices:
                datas.append(device)            
            db.close()            
            return jsonify(datas)
        
        if request.method == "POST": 
            data = request.get_json()           
            db.create('devices',data)                
            db.close()                
            return "device is updated successfully"
        
    except Exception as error:
        return jsonify({'error':'error'})
            
    return "The method is not suppot"

@api.route('/device/<int:id>', methods=["GET","POST"])
def device(id):
    try:
        db = MySQLCRUD()
        if request.method == "GET":
            if id:
                device = db.read('devices',{'id':id})           
                db.close()
                if device:
                    return jsonify(device)
                return jsonify({'error':'No record found'})
            else:
                return jsonify({'error':'No record found'})
            
        if request.method == "POST" and request.is_json:           
            data = request.get_json()
            action = data.pop('action')
            if action == "update":
                print(data) 
                db.update('devices',data,{'id':id})                
                db.close()                
                return "Device is created successfully"
            
            if data['action'] == 'delete':
                db.delete('devices',{'id':int(id)})
                db.close()                                
                return jsonify({"message":"Object is deleted successfully"})    
             
       
    except Exception as error:
        return jsonify({'error':'error'})


@api.route('/delete_device/<int:id>', methods=["GET","POST"])
def delete(id):
    try:
        if request.method == "GET":
           
            return jsonify({"message":"The device deleted successfully"})
        return jsonify({"message":"The method is not supported"})
    except Exception as error:
       return jsonify({'error':error})
       

@api.route('/locations')
def locaction():
    
   try:
     db = MySQLCRUD()
     locactions = db.read('locations')     
     datas = []
     for location in locactions:       
        datas.append(location)   
     db.close() 
   except Exception as e:
    return jsonify({f"message":"testing{e}"})
    
   return jsonify({"message":"testing"})



        