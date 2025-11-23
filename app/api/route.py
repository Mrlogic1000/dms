from . import api
from ..extensions import mysql
from flask import jsonify,request
from . mydb import MySQLCRUD
import json
from . functions import gen_ip


@api.route('/devices', methods=["GET","POST"])
def devices():
    try:
        db = MySQLCRUD()
        if request.method == "GET":             
            devices = db.read('devices')
            datas = []
            for device in devices:
                cur = mysql.connection.cursor()
                cur.execute("select ip, create_at from installed where device_id = %s",[device['id']])
                installed= cur.fetchone()
                
                device['installed'] = installed
                datas.append(device)            
            db.close()            
            return jsonify(datas)
        
        if request.method == "POST": 
            data = request.get_json()           
            db.create('devices',data)                
            db.close()                
            return "device is updated successfully"
        
    except Exception as error:
        print(error)
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
                old_device = db.read("devices",{"id":id}) 
                if old_device:
                    db.update('devices',data,{'id':id}) 
                    devicehistory = {} 
                    devicehistory['change_type'] = "update"
                    devicehistory['old_value'] = ' '.join(data.value())
                    print(devicehistory["old_value"])

                db.create("devicehistory")              
                db.close()                
                return "Device is created successfully"
           
            if action== 'delete':
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



@api.route('/installed', methods=["GET","POST"])
def installed():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("select devices.id, name,device_type,model,location_name from devices join installed on devices.id=device_id join locations" \
        " on location_id = locations.id ")
        installed= cur.fetchall()
        cur.close()
        return jsonify(installed)
    if request.method == "POST":
        db = MySQLCRUD()        
        data = request.get_json()             
        data['user_id'] = 1        
        device = db.read("installed",{"device_id":data["device_id"]})
        if device:
            return jsonify({"error":"The device is already installed"})
        db.create("installed",data)          
        
        return jsonify({"message":"post datas"})  
    
   
    return jsonify({"error":"The method is not support"})

@api.route('/installed/<int:id>', methods=["GET","POST"])
def installed_id(id):
    if request.method == "POST":
        db = MySQLCRUD()        
        data = request.get_json()
        if data['action']== 'delete':
            db.delete("installed",{'device_id':data['id']})
            return jsonify({"message":"The device is uninstalled"}) 


@api.route('parameters')
def params():
    cur = mysql.connection.cursor()
    cur.execute("select id, name from devices")
    devices= cur.fetchall()

    cur.execute("select id, location_name as name from locations")
    locations= cur.fetchall()
    cur.close()
    
    ip = gen_ip("172.3.100.0/24")
    parameters = {}
    parameters['locations'] = locations
    parameters['devices'] = devices
    parameters['ip'] = ip
    return jsonify(parameters)


@api.route('/ipaddress')
def ip():
    ip = gen_ip("172.3.100.0/24")
    return jsonify(ip)
