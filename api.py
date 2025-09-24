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
    SalesUser,
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
    full_name: str
    password: str


class AuthRequest(BaseModel):
    email: str | None = None
    phone: str | None = None
    password: str

class AnketaUsersSales(BaseModel):
    stamp: str
    model_car: str
    run: int
    price: int
    vin: str

class AnketaUpdate(BaseModel):
    stamp: str | None = None
    model_car: str | None = None
    run: int | None = None
    price: int | None = None
    vin: str | None = None

@app.post('/users/register/', tags=['Users'])
async def register_users(user: Registration):
    """"Регистрация нового пользователя"""
    if not re.fullmatch(EMAIL_REGEX, user.email) or not re.fullmatch(PHONE_REGEX, user.phone):
        raise HTTPException(400, 'Неверный формат данных email/номера телефона')
    try:
        existing_user = Users.select().where((Users.email==user.email) | (Users.phone==user.phone)).first()
        if existing_user:
            raise HTTPException(403, 'Пользователь с таким email/номером телефона уже существует.')

        hashed_password = ph.hash(user.password)
        with database_connection.atomic():
            user_role = Roles.get(Roles.name=='Пользователь')
            user, _ = Users.get_or_create(
                email=user.email,
                phone=user.phone,
                full_name=user.full_name,
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
    

@app.put("/users/me/password", tags=["Users"])
async def reboot_password(password: str, token: str = Header(...)):
    """Endpoint для изменение пользовательского пароля"""
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


@app.post("/users/anketa/create", tags=["Users"])
async def create_anket(anketa: AnketaUsersSales, token: str = Header(...)):
    """ Endpoint для создания анкеты на продажу авто фирме"""

    current_user = get_user_by_token(token)

    try:
        if not current_user:
            raise HTTPException(404, 'Пользователь не найден ')
        vin_number = SalesUser.select().where(SalesUser.vin == anketa.vin).first()
        if not vin_number:
            SalesUser.create(
                user_id = current_user.id,
                stamp = anketa.stamp,
                model_car = anketa.model_car,
                run = anketa.run,
                price = anketa.price,
                vin = anketa.vin
            )
            return {'message': 'Анкета успешно создана'}
        else:
            raise HTTPException(402, 'Анкета для этого автомобиля уже существует ')
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(500, f'Непредвиденая ошибка: {e}')



@app.delete("/users/anketa/delete", tags=["Users"])
async def delete_anketa(anketa_id: int , token: str = Header(...)):
    """Endpoint для удаления пользователе анкеты"""
    current_user = get_user_by_token(token)
    try:
        if not current_user:
            raise HTTPException(404, 'Пользователь не найден ')
        user =(SalesUser
               .select()
               .where(
                   (SalesUser.user_id == current_user.id) &
                   (SalesUser.id == anketa_id))
                .first())
        if not user:
            raise HTTPException(404, 'Анкета не найдена')
        user.delete_instance()
        return {'messgae': "Анкета успешно удалена"}
    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(500, f'Непредвиденая ошибка: {e}')
    

@app.put("/users/anketa/update", tags=["Users"])
async def update_anketa(data: AnketaUpdate, anketa_id: int , token: str = Header(...)):
    """Endpoint для изменения анкеты"""
    current_user = get_user_by_token(token)
    try:
        anketa = (SalesUser
                    .select()
                    .where(
                        (SalesUser.user_id == current_user.id) &
                        (SalesUser.id == anketa_id))
                    .first())
        if not data:
            raise HTTPException(401, "Введите данны для обновления информации анкеты")
        if data.stamp:
            anketa.stamp = data.stamp
        
        if data.model_car:
            anketa.model_car = data.model_car

        if data.run:
            anketa.run = data.run

        if data.price:
            anketa.price = data.price
        if data.vin:
            vin_number = (SalesUser
                        .select()
                        .where(SalesUser.vin == anketa.vin)
                        .first())
            if vin_number:
                raise HTTPException(402, "Анкета для этого автомобиля уже существует")
            anketa.vin = data.vin
        anketa.save()

    except HTTPException as http_exc:
        raise http_exc
    
@app.get("/users/anketi/", tags=["Users"])
async def list_user_anketi(token: str = Header(...)):
    """Endpoint для просмотра анкет пользователя"""
    current_user = get_user_by_token(token)
    if not current_user:
        raise HTTPException(401, "Пользователь не найден")
    anketi = SalesUser.select().where(SalesUser.user_id == current_user.id)
    if not anketi:
        return {"message": "Анкеты отсутствуют"}
    return [{
        
    } for anketa in anketi]
    



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
