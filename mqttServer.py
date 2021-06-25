import paho.mqtt.client as mqtt
import re
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:Yang654321@localhost:3306/miniIOT", encoding="utf-8")
Session = sessionmaker(bind=engine)
session = Session()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("testapp")


def on_message(client, userdata, msg):
    print(msg.topic+" " + ":" + str(msg.payload))
    var = str(msg.payload)
    n = re.findall(r":(.+?),", var)
    # print(n)
    # print(eval(n[1]))
    print(str(msg.qos) + " " + ":" + str(msg.retain))
    stmt = f'insert into device values ("{int(n[0])}", "{eval(n[1])}", "{eval(n[2])}", "{float(n[3])}", "{float(n[4])}", "{float(n[5])}","{random.randint(0,99)}")'
    session.execute(stmt)
    session.commit()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)
client.loop_forever()
