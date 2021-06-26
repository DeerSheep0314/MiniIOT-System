import hashlib
from flask import Flask, request, make_response, send_from_directory, url_for, flash, redirect
from flask_cors import CORS
from sqlalchemy import text
from werkzeug.utils import secure_filename

from Classes import Base, Engine, select, PUser, Device, session, MyJSONEncoder
import json
import os
from flask import render_template

app = Flask(__name__)
CORS(app)
# filePath = './static'


# app.debug = True


# @app.route('/', methods=['GET'])
# def welcome():
#     return render_template('test.html')


# 登陆验证
@app.route('/loginValidness', methods=['GET'])
def loginValidness():
    userName = request.args.get('userName')
    passWD = request.args.get('passWD')
    type = request.args.get('type')
    stmt = f'select * from puser where userName = "{userName}" and passWD = "{passWD}"'
    resultSet = session.execute(stmt)
    match = 1 if resultSet.rowcount else 0
    identity = 0
    if (match == 1):
        if type == 'admin':
            stmt = f'select * from puser where userName = "{userName}"'
            resultSet = session.execute(stmt)
            identity = 1 if resultSet.rowcount else 0
        elif type == 'normal':
            stmt = f'select * from puser where userName = "{userName}"'
            resultSet = session.execute(stmt)
            identity = 1 if resultSet.rowcount else 0
        else:
            pass
    return json.dumps({'match': match, 'identity': identity}, indent=2, ensure_ascii=False)


'''
after login :
'''


# 获取某个用户信息
@app.route('/userInfo', methods=['GET'])
def userInfo():
    userName = request.args.get('userName')
    type = request.args.get('type')
    if type == 'admin':
        res = session.query(PUser).filter(PUser.userName == userName).all()
        stu = res[0]
        return json.dumps(stu, cls=MyJSONEncoder, indent=2, ensure_ascii=False)
    elif type == 'normal':
        res = session.query(PUser).filter(PUser.userName == userName).all()
        ins = res[0]
        return json.dumps(ins, cls=MyJSONEncoder, indent=2, ensure_ascii=False)
    else:
        return json.dumps({'state': 404}, indent=2, ensure_ascii=False)


@app.route('userPortrait', methods=['GET'])
def userPortrait():
    userName = request.args.get('userName')
    url = userName + '.' + session.query(PUser.portrait).filter(PUser.userName == userName).all()[0][0]
    return json.dumps({'url': url})


# 修改某个用户个人信息
@app.route('/modifyInfo', methods=['POST'])
def modifyInfo():
    userName = request.form['userName']
    nickName = request.form['nickName']
    passWD = request.form['passWD']
    try:
        stmt = f'update puser set puser.nickName = "{nickName}" where puser.userName = "{userName}"'
        # session.query(PUser).filter(PUser.userName == userName).update({'nickName':nickName})
        session.execute(stmt)
        session.commit()
        if passWD != '':
            stmt = f'update puser set puser.passWD = "{passWD}" where puser.userName = "{userName}"'
            session.execute(stmt)
            session.commit()
        return json.dumps({'state': 200}, indent=2, ensure_ascii=False)
    except:
        return json.dumps({'state': 404}, indent=2, ensure_ascii=False)


# 管理员管理设备信息
@app.route('/manageInfo', methods=['GET'])
def manageInfo():
    deviceName = request.args.get('deviceName')
    stmt = f'SELECT deviceName FROM device NATURAL JOIN manage WHERE manage.deviceName = "{deviceName}"'
    res = session.execute(stmt)
    device_list = [
        {'设备标识符': i[0], '设备名称': i[1]} for i in
        res]
    return json.dumps(device_list, cls=MyJSONEncoder, indent=2, ensure_ascii=False)


# 查看在线的设备
@app.route('/workDevice', methods=['GET'])
def studyCourse():
    deviceName = request.args.get('deviceName')
    stmt = f'SELECT id,info FROM device NATURAL JOIN value WHERE device.id = "{deviceName}"'
    res = session.execute(stmt)
    device_list = [
        {'设备ID': i[0], '设备名称': i[1]} for i in
        res]
    return json.dumps(device_list, cls=MyJSONEncoder, indent=2, ensure_ascii=False)

# 获取设备信息列表
@app.route('/workList', methods=['GET'])
def workList():
    deviceInfo = request.args.get('info')
    res = session.query(Device.info, Device.value, Device.lat, Device.lng).filter(
        Device.id == deviceInfo).all()
    res_list = [{'deviceInfo': i[0], 'deviceValue': i[1], 'deviceLat': i[2], 'deviceLng': i[3]} for i in res]
    return json.dumps(res_list, cls=MyJSONEncoder, indent=2, ensure_ascii=False)


# 获取时间戳
@app.route('/timestamp', methods=['GET'])
def hotCourse():
    ts = int(request.args.get('timestamp'))
    # 从0开始编号
    num = int(request.args.get('num'))
    stmt = 'SELECT distinct  device.timestamp from device WHERE device.timestamp > 0'
    res = session.execute(stmt)
    time_list = []
    for i, each in enumerate(res):
        if (ts + 1) * num > i:
            hotCourse.append(
                {'deviceTimestamp': each[0]})
        elif (ts + 1) * num == i:
            return json.dumps(time_list, cls=MyJSONEncoder, indent=2, ensure_ascii=False)
    return json.dumps(time_list, cls=MyJSONEncoder, indent=2, ensure_ascii=False)


# 信息修改
@app.route('/modify', methods=['POST'])
def modify():
    info = request.form['info']
    id = request.form['id']
    value = request.form['value']
    stmt = f'update Device set device.info = "{info}", device.id = "{id}" where device.value = "{value}"'
    res = session.execute(stmt)
    session.commit()
    if res:
        return json.dumps({'state': 200})
    else:
        return json.dumps({'state': 404})


# 设备图标信息
@app.route('/charts')
def getChartsData():
    sum = session.query(Device).filter(text("timestamp>0")).order_by(text("info")).all()
    res = session.query(Device).filter(text("value<100")).order_by(text("id")).all()
    resp = ['device0001', 'device0002', 'device0003', 'device0004', 'device0005']
    return json.dumps(resp, cls=MyJSONEncoder, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)