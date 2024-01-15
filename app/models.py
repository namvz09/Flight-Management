import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Enum, DateTime, Time, Float
from enum import Enum as UserEnum
from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
import hashlib

default_password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())

class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    STAFF = 3

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class User(BaseModel, UserMixin):
    fullname = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), default=default_password)
    image = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.fullname

class Airport(BaseModel):
    name = Column(String(50), nullable=False)
    code = Column(String(10), nullable=False)

    def __str__(self):
        return self.name

class FlightSchedule(BaseModel):
    __tablename__ = 'flight_sche'

    airport_from = Column(Integer, ForeignKey(Airport.id))
    airport_to = Column(Integer, ForeignKey(Airport.id))

    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    time_start = Column(DateTime, nullable=False)
    time_end = Column(DateTime, nullable=False)
    quantity_ticket_1st = Column(Integer, nullable=False)
    quantity_ticket_1st_booked = Column(Integer, default=0)
    quantity_ticket_2nd = Column(Integer, nullable=False)
    quantity_ticket_2nd_booked = Column(Integer, default=0)
    price = Column(Integer, default=0)

    bw_airports = relationship('BetweenAirport', backref='flight_sche', lazy=False)

    comments = relationship('Comment', backref='flight_sche', lazy=True)

    def __str__(self):
        return str(self.id)

class BetweenAirport(BaseModel):
    __tablename__ = 'between_airport'

    airport_id = Column(Integer, ForeignKey(Airport.id))
    flight_sche_id = Column(Integer, ForeignKey(FlightSchedule.id))
    time_stay = Column(Float, nullable=False)
    note = Column(String(100))

    is_deleted = Column(Boolean, default=False)

class Comment(BaseModel):
    __tablename__ = 'comments'
    flight_sche_id = Column(Integer, ForeignKey(FlightSchedule.id))
    author_id = Column(Integer, ForeignKey(User.id))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())

class Customer(BaseModel):
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(10), nullable=False)
    customer_id = Column(String(10), nullable=False)

class Ticket(BaseModel):
    author_id = Column(Integer, ForeignKey(User.id), nullable=True)
    customer_id = Column(Integer, ForeignKey(Customer.id))
    flight_sche_id = Column(Integer, ForeignKey(FlightSchedule.id))
    ticket_price = Column(Integer, nullable=False)
    ticket_type = Column(Integer, nullable=False)
    ticket_package_price = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.now())

class ADMINRules(BaseModel):
    min_time_flight_sche = Column(Float, default=0.5)
    max_between_airport_quantity = Column(Float, default=2)
    min_time_stay_airport = Column(Float, default=0.33)
    max_time_stay_airport = Column(Float, default=0.5)
    customer_time_ticket = Column(Float, default=12)
    staff_time_ticket = Column(Float, default=4)
    created_at = Column(DateTime, default=datetime.datetime.now())


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        a = User(fullname='Quản trị viên', username='admin', user_role=UserRole.ADMIN)
        s = User(fullname='Nhân viên', username='staff', user_role=UserRole.STAFF)
        u = User(fullname='Người dùng', username='user', user_role=UserRole.USER)
        db.session.add_all([a, s, u])
        db.session.commit()

        a1 = Airport(name="Tân Sơn Nhất (SGN)", code= "SGN")
        a2 = Airport(name="Nội Bài (HAN)", code= "HAN")
        a3 = Airport(name="Côn Đảo (VCS)", code= "VCS")
        a4 = Airport(name="Cà Mau (CAH)", code= "CAH")
        a5 = Airport(name="Cần Thơ (VCA)", code= "VCA")
        a6 = Airport(name="Phú Bài (HUI)", code= "HUI")
        a7 = Airport(name="Vân Đồn (VDO)", code= "VDO")
        a8 = Airport(name="Đà Nẵng (DAD)", code= "DAD")
        a9 = Airport(name="Phú Quốc (PQC)", code= "PQC")
        a10 = Airport(name="Vinh (VII)", code= "VII")

        db.session.add_all([a1, a2, a3, a4, a5, a6, a7, a8, a9, a10])
        db.session.commit()

        a = ADMINRules()
        db.session.add(a)
        db.session.commit()
