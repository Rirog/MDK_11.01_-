"""Модуль API"""

import re
from datetime import datetime, timedelta
from passlib.hash import bcrypt
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import database_connection
from models import (
    Users,
    UserToken,
    Roles,
    UserRoles,
    Stamp,
    ModelCar,
    Cars,
    Shopping,
    Sales,
)


app = FastAPI()


EMAIL_REGEX = r'^[A-Za-zА-Яа-яЁё0-9._%+-]+@[A-Za-zА-Яа-яЁё-]+\.[A-Za-zА-Яа-яЁё-]{2,10}$'
PHONE_REGEX = r'^[0-9+()\-#]{10,15}$'


class Registration(BaseModel):
    email: str
    phone: str
    password: str


class AuthRequest(BaseModel):
    email: str | None = None
    phone: str | None = None
    password: str



@app.post('/users/register/', tags=['Users'])
async def register_users(email: str, password: str, full_name: str, number_phone: str):
    """"Регистрация нового пользователя"""
    if not re.fullmatch(EMAIL_REGEX, email) or not re.fullmatch(PHONE_REGEX, number_phone):
        raise HTTPException(400, 'Неверный формат данных email/номера телефона')
    try:
        existing_user = Users.select().where((Users.email==email) | (Users.phone==number_phone)).first()
        if existing_user:
            raise HTTPException(403, 'Пользователь с таким email/номером телефона уже существует.')

        hashed_password = bcrypt.hash(password)
        with database_connection.atomic():
            user_role = Roles.get(Roles.name=='Пользователь')
            user, _ = Users.get_or_create(
                email=email,
                phone=number_phone,
                full_name=full_name,
                password=hashed_password,
            )
            UserRoles.create(
                user_id=user.id,
                role_id=user_role.id)

        return {'message': 'Вы успешно зарегистрировались!'}
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(500, f'Произошла ошибка при регистрации: {e}')


@app.post('/users/auth/', tags=['Users'])
async def auth_user(data: AuthRequest):
    """Аутентификация пользователя"""

    email = data.email
    phone = data.phone
    password = data.password

    if not email and not phone:
        raise HTTPException(400, 'Введите email, либо номер телефона!')
    if email is not None:
        if not isinstance(email, str) or not re.fullmatch(EMAIL_REGEX, email):
            raise HTTPException(400, 'Неверный формат данных email.')
    if phone is not None:
        if not isinstance(phone, str) or not re.fullmatch(PHONE_REGEX, phone):
            raise HTTPException(400, 'Неверный формат данных номера телефона.')
    try:
        query = None
        if email:
            query = Users.select().where(Users.email==email)
        elif phone:
            query = Users.select().where(Users.phone==phone)
        existing_user = query.first() if query else None
        if not existing_user:
            raise HTTPException(404, 'Пользователя с таким email/номером телефона не  существует.')
        
        if not bcrypt.verify(password, existing_user.password):
            raise HTTPException(401, 'Вы ввели неправильный пароль! Попробуйте еще раз.')
        
        token = str(uuid4())
        expires_at = datetime.now() + timedelta(hours=1)
        
        UserToken.create(
            user_id=existing_user.id,
            token=token,
            expires_at=expires_at
        )
        
        return {'message': 'Успешная авторизация!',
                'token': token,
                'expires_at': expires_at.isoformat()}
        
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(500, f'Произошла ошибка при авторизации: {e}')

