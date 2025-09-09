"""Модуль для базы данных"""
from peewee import (
    Model,
    CharField,
    IntegerField,
    DateTimeField,
    ForeignKeyField,
    AutoField,
)
from hashlib import sha512
from database import database_connection
from datetime import datetime

def hashing(password: str) -> str:
    return sha512(password.encode("UTF-8")).hexdigest()


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
    token = CharField(unique=True, null=True)
    token_expires_at = DateTimeField(null=True)

class Stamp(Table):
    id = AutoField()
    stamp = CharField(unique=True, null=False, max_length=20) 

class ModelCar(Table):
    id = AutoField()
    model_car = CharField(unique=True, null=False, max_length=50)


class Cars(Table):
    """Модель с информацией об автомобиле"""

    id = AutoField()
    stamp = ForeignKeyField(Stamp, on_delete="CASCADE", on_update="CASCADE")
    model_car = ForeignKeyField(ModelCar, on_delete="CASCADE", on_update="CASCADE")
    run_km = IntegerField()




tables = [
    Users
]



def initialize_database():
    try:
        database_connection.connect()
        database_connection.create_tables(
            tables,
            safe=True
        )
        print('Tables is initialized')


    except Exception as e:
        print(f'Error initializing tables: {e}')
    finally:
        database_connection.close()