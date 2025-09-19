"""Модуль API"""

import re
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
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

ph = PasswordHasher()

EMAIL_REGEX = r'^[A-Za-zА-Яа-яЁё0-9._%+-]+@[A-Za-zА-Яа-яЁё-]+\.[A-Za-zА-Яа-яЁё-]{2,10}$'
PHONE_REGEX = r'^[0-9+()\-#]{10,15}$'


def get_user_by_token(token: str, role: Optional[str] = None) -> Users:
    try:
        user_token = (UserToken.select().join(Users).where(
            (UserToken.token==token) &
            (UserToken.expires_at > datetime.now()) 
        ).first())
        
        if not user_token:
            raise HTTPException(401, 'Недействительный или просроченный токен.')
               
        user = user_token.user_id
        user_role = (UserRoles
                    .select(Roles.name)
                    .join(Roles, on=(UserRoles.role_id == Roles.id))
                    .where(UserRoles.user_id == user)
                    .first())
        if role:
            if user_role != 'Администратор':
                if user_role != role:
                    raise HTTPException(403, 'Недостаточно прав для выполнения этого действия.')
        
        user_token.expires_at = datetime.now() + timedelta(hours=1)
        user_token.save()
        
        return user
    
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(500, f'Ошибка при проверке токена: {e}')


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

        hashed_password = ph.hash(password)
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
        try:
            ph.verify(existing_user.password, password)
        except:
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


@app.delete('/users/delete_me/', tags=['Users'])
async def delete_profile(token: str = Header(...)):
    """Удаления аккаунта"""
    user = get_user_by_token(token, "Пользователь")
    if not user:
        raise HTTPException(401, 'Не удалось найти пользователя.')
    user.delete_instance()
    return {'message': 'Пользователь успешно удален.'}


@app.get('/users/me/', tags=['Users'])
async def get_profile(token: str = Header(...)):
    """Получение своей информации пользователем"""
    try:
        user = get_user_by_token(token)
        if not user:
            raise HTTPException(401, 'Не удалось найти пользователя.')
        return {
            'id': user.id,
            'name': user.full_name,
            'email': user.email,
            'phone': user.phone,
        }
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(500, f'Непредвиденая ошибка: {e}')
    

@app.put("/users/me/password")
async def reboot_password(password: str, token: str = Header(...)):
    """Изменение пользовательского пароля"""
    current_user = get_user_by_token(token)
    try:
        if not current_user:
            raise HTTPException(404, 'Пользователь не найден ')

        user = Users.get(Users.id==current_user.id)
        hash_password = ph.hash(password)
        user.password = hash_password
        user.save()

        ph.verify(hash_password, password)

        return {"message": "пароль успешно изменен"}
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(500, f'Непредвиденая ошибка: {e}')


@app.post("/users/anketa/create")
async def create 
# @app.get("/usesr/list_users/", tags=["Admin"])
# async def get_list_users(token: str = Header(...)):
#     """Получение список всех пользователей"""
#     current_user = get_user_by_token(token, "Администратор")

#     if not current_user:
#         raise HTTPException(404, 'Пользователь не найден ')
    
#     users = Users.select().where(Users.id!=current_user.id)

#     return [
#         {
#             "id": user.id,
#             "name": user.full_name,
#             "email": user.email,
#             "phone": user.phone,
#         } for user in users
#     ]

# @app.delete("/usesr/delete_profile/", tags=["Admin"])
# async def delete_profile_user(user_id: int, token: str = Header(...)):
#     """Удаления профиля пользователя"""

#     current_user = get_user_by_token(token, "Администратор")
    
#     user = Users.select().where(Users.id==user_id).first()
#     if user.id == current_user.id:
#          raise HTTPException(419, 'Аккаунт данного пользователя нельзя удалить.')
#     if not user:
#         raise HTTPException(404, 'Пользователь с указанным ID не найден.')
#     user.delete_instance()
#     return {'message': 'Пользователь успешно удален.'}
