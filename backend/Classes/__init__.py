from datetime import datetime
from datetime import timedelta
from datetime import date
from sqlalchemy.dialects.mysql import VARCHAR, DATETIME, TIME, DATE, CHAR, BIT, BIGINT, FLOAT, TINYINT, DOUBLE
from sqlalchemy import Column
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from json import JSONEncoder
import copy
Base = declarative_base()


class PUser(Base):
    __tablename__ = 'PUser'
    userName = Column(VARCHAR(100), primary_key=True)
    eMail = Column(VARCHAR(100), nullable=False)
    passWD = Column(VARCHAR(256), nullable=False)
    isAdministrator = Column(TINYINT, nullable=False)

    def __init__(self, username, email, passwd, isadministrator):
        self.userName = username
        self.eMail = email
        self.passWD = passwd
        self.isAdministrator = isadministrator


class Device(Base):
    __tablename__ = 'Device'
    alert = Column(TINYINT, nullable=False)
    id = Column(CHAR(10), nullable=False)
    info = Column(VARCHAR(50), nullable=False)
    lat = Column(DOUBLE, nullable=False)
    lng = Column(DOUBLE, nullable=False)
    timestamp = Column(BIGINT, primary_key=True)
    value = Column(TINYINT, nullable=False)

    def __init__(self, alert, id, info, lat, lng, timestamp, value):
        self.alert = alert
        self.id = id
        self.info = info
        self.lat = lat
        self.lng = lng
        self.timestamp = timestamp
        self.value = value


class MyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PUser):
            return {'userName': obj.userName}
        elif isinstance(obj, Device):
            # return {obj.id,obj.userName,obj.firstName,obj.lastName,obj.department}
            temp = copy.deepcopy(obj.__dict__)
            temp.pop('_sa_instance_state')
            return temp
        elif isinstance(obj, date):
            return str(obj)
        elif isinstance(obj, datetime):
            return str(obj)
        elif isinstance(obj, timedelta):
            return str(obj)
        else:
            pass


# Base.metadata.drop_all(Engine)
# Base.metadata.create_all(Engine)
Engine = create_engine("mysql+pymysql://root:Yang654321@127.0.0.1:3306/miniiot", encoding="utf-8")
Session = sessionmaker(bind=Engine)
session = Session()
