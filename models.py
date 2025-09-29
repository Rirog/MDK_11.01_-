"""Модуль для базы данных"""
from peewee import (
    Model,
    CharField,
    IntegerField,
    DateTimeField,
    ForeignKeyField,
    AutoField,
)
from database import database_connection
from datetime import datetime



class Table(Model):
    """Базовая модель"""

    class Meta:
        """Класс мета"""

        database = database_connection


class Users(Table):
    """Модель с информацией о пользователе"""

    id = AutoField()
    email = CharField(unique=True, max_length=255, null=False)
    phone = CharField(unique=True, max_length=12, null=False)
    full_name = CharField(max_length=50, null=False)
    password = CharField(max_length=128, null=False)


class UserToken(Table):
    id = AutoField()
    user_id = ForeignKeyField(Users, on_delete="CASCADE", on_update="CASCADE", null=False)
    token = CharField(max_length=255, null=False)
    created_at = DateTimeField(default=datetime.now(), null=False)
    expires_at = DateTimeField(null=False)


class Roles(Table):

    id = AutoField()
    name = CharField(null=False, unique=True, max_length=20)


class UserRoles(Table):

    user_id = ForeignKeyField(Users, on_delete="CASCADE", on_update="CASCADE")
    role_id = ForeignKeyField(Roles, on_delete="CASCADE", on_update="CASCADE")


class Stamp(Table):
    id = AutoField()
    stamp = CharField(unique=True, null=False, max_length=20) 


class ModelCar(Table):
    id = AutoField()
    model_car = CharField(unique=True, null=False, max_length=50)


class Status(Table):
    """Модель со статусом анкеты"""

    id = AutoField()
    status = CharField(unique=True, null=False, max_length=10)


class Cars(Table):
    """Модель с информацией об автомобиле"""

    id = AutoField()
    stamp_id = ForeignKeyField(Stamp, on_delete="CASCADE", on_update="CASCADE")
    model_car_id = ForeignKeyField(ModelCar, on_delete="CASCADE", on_update="CASCADE")
    run_km = IntegerField()
    vin = CharField(unique=True, null=False)
    status_id = ForeignKeyField(Status, on_delete="CASCADE", on_update="CASCADE")


class Shopping(Table):
    """Модель с информацией о покупках""" 

    id = AutoField()
    car_id = ForeignKeyField(Cars, on_delete="CASCADE", on_update="CASCADE")
    saler_id = ForeignKeyField(Users,on_delete="CASCADE", on_update="CASCADE")
    date_buy = DateTimeField(null=False, default=datetime.now())
    price = IntegerField(null=False)


class Sales(Table):
    """Модель для хранения данных о продаже"""

    id = AutoField()
    car_id = ForeignKeyField(Cars, on_delete="CASCADE", on_update="CASCADE")
    buyer_id = ForeignKeyField(Users, on_delete="CASCADE", on_update="CASCADE")
    date_sale = DateTimeField(null=False, default=datetime.now())
    price = IntegerField(null=False)


class SalesUser(Table):
    """Модель для хранения заявок на продажу пользователями."""

    id = AutoField()
    user_id = ForeignKeyField(Users, on_delete="CASCADE", on_update="CASCADE")
    stamp = CharField(max_length=25)
    model_car = CharField(max_length=25)
    run_km = IntegerField()
    price = IntegerField(null=False)
    vin = CharField(unique=True, null=False)

tables = [
    Users,
    UserToken,
    Roles,
    UserRoles,
    Stamp,
    ModelCar,
    Cars,
    Shopping,
    Sales,
    SalesUser
]

roles = [
    {"name": "Администратор"},
    {"name": "Пользователь"}
]


def initialize_database():
    try:
        database_connection.connect()
        database_connection.create_tables(
            tables,
            safe=True
        )
        print('Tables is initialized')
        Roles.insert_many(roles).execute()
    except Exception as e:
        print(f'Error initializing tables: {e}')
    finally:
        database_connection.close()


initialize_database()