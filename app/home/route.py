from . import home
from flask import render_template
from ..extensions import mysql



@home.route('/')
def home():
    datas = []
    cur = mysql.connection.cursor()
    cur.execute("select * from devices")
    devices = cur.fetchall()
    for device in devices:
        d = {}
        d['id'] = device[0]
        d['name'] = device[1]
        d['model'] = device[2]
        d['mac'] = device[3]
        d['ip'] = device[4]
        d['username'] = device[5]
        d['password'] = device[6]
        d['location'] = device[7]
        datas.append(d)    

    cur.close()
    return render_template('index.html', datas = datas)