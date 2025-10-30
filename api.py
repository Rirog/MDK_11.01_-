"""Модуль API"""

import re
from datetime import datetime, timedelta

from fastapi.responses import JSONResponse
from argon2 import PasswordHasher
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Header, Request
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
    Anketa,
    Status
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
        user_role = (Roles
                    .select()
                    .join(UserRoles, on=(UserRoles.role_id == Roles.id))
                    .where(UserRoles.user_id == user)
                    .first())
        if role:
           if user_role.name != role:
                raise HTTPException(status_code=403, detail='Недостаточно прав для выполнения этого действия.')
        
        user_token.expires_at = datetime.now() + timedelta(hours=1)
        user_token.save()
        
        return user
    
    except HTTPException as http_exc:
        raise http_exc


class PasswordChange(BaseModel):
    password: str


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
    description: Optional[str] = None

class AnketaUpdate(BaseModel):
    stamp: Optional[str] = None
    model_car: Optional[str] = None
    run: Optional[int] = None
    price: Optional[int] = None
    vin: Optional[str] = None
    description: Optional[str] = None


class CarsCreated(BaseModel):
    stamp: str 
    model_car: str 
    run: int
    price: int 
    vin: str
    description: Optional[str] = None

class CarsUpdate(BaseModel):
    run: Optional[int] = None
    price: Optional[int] = None
    status_id: Optional[int] = None
    description: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


class StampCreate(BaseModel):
    stamp: str

class ModelCarCreate(BaseModel):
    model_car: str

class ShoppingCreate(BaseModel):
    car_id: int
    buyer_id: int
    price: int

class SalesCreate(BaseModel):
    car_id: int
    buyer_id: int
    price: int


@app.exception_handler(Exception)
async def global_exception_handler(req: Request, exc: Exception):
    """Глобальный обработчик всех необработанных исключений в приложении"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Внутренняя ошибка сервера.",
            "error": str(exc)
        }
    )


@app.post('/users/register/', tags=['Users'])
async def register_users(user: Registration):
    """"Регистрация нового пользователя"""
    if not re.fullmatch(EMAIL_REGEX, user.email) or not re.fullmatch(PHONE_REGEX, user.phone):
        raise HTTPException(400, 'Неверный формат данных email/номера телефона')
    try:
        email = user.email.lower()
        existing_user = Users.select().where((Users.email==email) | (Users.phone==user.phone)).first()
        if existing_user:
            raise HTTPException(403, 'Пользователь с таким email/номером телефона уже существует.')

        hashed_password = ph.hash(user.password)
        with database_connection.atomic():
            user_role = Roles.get(Roles.name=='Пользователь')
            user, _ = Users.get_or_create(
                email=email,
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


@app.post('/users/auth/', tags=['Users'])
async def auth_user(data: AuthRequest):
    """Аутентификация пользователя"""

    email = data.email.lower()
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
    

@app.put("/users/me/", tags=["Users"])
async def update_profile(user_data: UserUpdate, token: str = Header(...)):
    """Обновление профиля пользователя"""
    current_user = get_user_by_token(token)
    
    try:
        if user_data.phone and not re.fullmatch(PHONE_REGEX, user_data.phone):
            raise HTTPException(400, 'Неверный формат номера телефона')
            
        if user_data.phone:
            existing_phone = Users.get_or_none(Users.phone == user_data.phone)
            if existing_phone and existing_phone.id != current_user.id:
                raise HTTPException(400, 'Номер телефона уже используется')
        
        if user_data.full_name:
            current_user.full_name = user_data.full_name
        if user_data.phone:
            current_user.phone = user_data.phone
            
        current_user.save()
        return {"message": "Профиль успешно обновлен"}
    except HTTPException as http_exc:
        raise http_exc


@app.put("/users/me/password", tags=["Users"])
async def reboot_password(password: PasswordChange, token: str = Header(...)):
    """Endpoint для изменение пользовательского пароля"""
    current_user = get_user_by_token(token)
    try:
    
        user = Users.get(Users.id==current_user.id)
        hash_password = ph.hash(password.password)
        user.password = hash_password
        user.save()

        ph.verify(hash_password, password.password)

        return {"message": "пароль успешно изменен"}
    except HTTPException as http_exc:
        raise http_exc


@app.post("/users/anketa/create", tags=["Users"])
async def create_anket(anketa: AnketaUsersSales, token: str = Header(...)):
    """ Endpoint для создания анкеты на продажу авто фирме"""

    current_user = get_user_by_token(token)

    try:
        if not current_user:
            raise HTTPException(404, 'Пользователь не найден ')
        vin_number = Anketa.select().where(Anketa.vin == anketa.vin).first()
        if vin_number:
            raise HTTPException(402, 'Анкета для этого автомобиля уже существует')


        existing_car = Cars.select().where(Cars.vin == anketa.vin).first()
        if existing_car:
            raise HTTPException(402, 'Автомобиль с таким VIN уже существует в базе')
        Anketa.create(
            user_id = current_user.id,
            stamp = anketa.stamp,
            model_car = anketa.model_car,
            run = anketa.run,
            price = anketa.price,
            vin = anketa.vin,
            description = anketa.description
        )
        return {'message': 'Анкета успешно создана'}
    except HTTPException as http_exc:
        raise http_exc


@app.delete("/users/anketa/delete", tags=["Users"])
async def delete_anketa(anketa_id: int , token: str = Header(...)):
    """Endpoint для удаления пользовательской анкеты"""
    current_user = get_user_by_token(token)
    try:
        if not current_user:
            raise HTTPException(404, 'Пользователь не найден ')
        anketa =(Anketa
               .select()
               .where(
                   (Anketa.user_id == current_user.id) &
                   (Anketa.id == anketa_id))
                .first())
        if not anketa:
            raise HTTPException(404, 'Анкета не найдена')
        anketa.delete_instance()
        return {'message': "Анкета успешно удалена"}
    except HTTPException as http_exc:
        raise http_exc
    

@app.put("/users/anketa/update", tags=["Users"])
async def update_anketa(data: AnketaUpdate, anketa_id: int , token: str = Header(...)):
    """Endpoint для изменения анкеты"""
    current_user = get_user_by_token(token)
    try:
        anketa =(Anketa
                .select()
                .where(
                    (Anketa.user_id == current_user.id) &
                    (Anketa.id == anketa_id))
                .first())
        if not anketa:
            raise HTTPException(404, 'Анкета не найдена')
        if not data:
            raise HTTPException(401, "Введите данные для обновления информации анкеты")
        if data.stamp:
            anketa.stamp = data.stamp
        
        if data.model_car:
            anketa.model_car = data.model_car

        if data.run:
            anketa.run = data.run

        if data.price:
            anketa.price = data.price

        if data.vin:
            vin_number = Anketa.select().where(
                (Anketa.vin == data.vin) & 
                (Anketa.id != anketa_id)
            ).first()

            if vin_number:
                raise HTTPException(402, "Анкета для этого автомобиля уже существует")
            
            existing_car = Cars.select().where(Cars.vin == data.vin).first()

            if existing_car:
                raise HTTPException(402, "Автомобиль с таким VIN уже существует в базе автомобилей")
            anketa.vin = data.vin

        if data.description:
            anketa.description = data.description

        anketa.save()
        return {"message": "Анкета успешно обновлена"}
    except HTTPException as http_exc:
        raise http_exc
    

@app.get("/users/anketi/", tags=["Users"])
async def list_user_anketi(token: str = Header(...)):
    """Endpoint для просмотра анкет пользователя"""
    current_user = get_user_by_token(token)

    try:
        if not current_user:
            raise HTTPException(401, "Пользователь не найден")
        anketi = Anketa.select().where(Anketa.user_id == current_user.id)
        if not anketi:
            return {"message": "Анкеты отсутствуют"}
        return [{
            "id": anketa.id,
            "stamp": anketa.stamp,
            "model_car": anketa.model_car,
            "run": anketa.run,
            "price": anketa.price,
            "vin": anketa.vin,
            "description": anketa.description
        } for anketa in anketi]
    except HTTPException as http_exc:
        raise http_exc
    

@app.post("/users/cars/buy", tags=["Users"])
async def buy_car(car_id: int, token: str = Header(...)):
    """Endpoint для покупки авто пользователем"""
    current_user = get_user_by_token(token)

    try:
        if not current_user:
            raise HTTPException(401, 'Не удалось найти пользователя.')
        car = Cars.select().where(Cars.id == car_id).first()
        if not car:
            raise HTTPException(404, "Автомобиль не найден")
        available_status = Status.get(Status.status == "Доступен")
        
        if car.status_id != available_status:
            raise HTTPException(400, "Этот автомобиль недоступен для покупки")

        with database_connection.atomic():
            Shopping.create(
                car_id=car.id,
                buyer_id=current_user.id,
                price=car.price 
            )

            sold_status = Status.get(Status.status == "Продан")
            car.status_id = sold_status
            car.save()

        return {"message": "Автомобиль успешно куплен"}

    except HTTPException as http_exc:
        raise http_exc

@app.get("/users/cars/available", tags=["Users"])
async def get_available_cars(token: str = Header(...)):
    """Получение списка доступных автомобилей"""
    current_user = get_user_by_token(token)
    
    try:
        available_status = Status.get(Status.status == "Доступен")
        if not available_status:
            return []
        cars = (Cars
                .select(Cars, Stamp, ModelCar)
                .join(Stamp, on=(Cars.stamp_id == Stamp.id))
                .join(ModelCar, on=(Cars.model_car_id == ModelCar.id))
                .where(Cars.status_id == available_status.id))
                
        return [{
            "id": car.id,
            "stamp": car.stamp_id.stamp,
            "model": car.model_car_id.model_car,
            "run_km": car.run_km,
            "vin": car.vin,
            "price": car.price
        } for car in cars]
    except HTTPException as http_exc:
        raise http_exc


@app.get("/users/my_purchases", tags=["Users"])
async def get_my_purchases(token: str = Header(...)):
    """Получение истории покупок пользователя"""
    current_user = get_user_by_token(token)
    
    try:
        purchases = (Shopping
                    .select(Shopping, Cars, Stamp, ModelCar)
                    .join(Cars, on=(Shopping.car_id == Cars.id))
                    .join(Stamp, on=(Cars.stamp_id == Stamp.id))
                    .join(ModelCar, on=(Cars.model_car_id == ModelCar.id))
                    .where(Shopping.buyer_id == current_user.id))
        if not purchases:
            raise HTTPException(404, "Истории покупок пуста")
        return [{
            "id": purchase.id,
            "car": {
                "stamp": purchase.car_id.stamp_id.stamp,
                "model": purchase.car_id.model_car_id.model_car,
                "vin": purchase.car_id.vin,
                "run_km": purchase.car_id.run_km
            },
            "price": purchase.price,
            "date_buy": purchase.date_buy.isoformat()
        } for purchase in purchases]
    except HTTPException as http_exc:
        raise http_exc


@app.get("/users/list_users/", tags=["Admin"])
async def get_list_users(token: str = Header(...)):
    """Получение список всех пользователей"""
    current_user = get_user_by_token(token, "Администратор")

    users = Users.select().where(Users.id!=current_user.id)
    if not users:
        raise HTTPException(404, "Пользователи не найдены")
    try:
        return [
            {
                "id": user.id,
                "name": user.full_name,
                "email": user.email,
                "phone": user.phone,
            } for user in users
        ]
    except HTTPException as http_exc:
        raise http_exc
    

@app.get("/users/cars/{car_id}", tags=["Users"])
async def get_car_details(car_id: int, token: str = Header(...)):
    """Получение детальной информации об автомобиле"""
    current_user = get_user_by_token(token)
    try:
        car = (Cars
               .select(Cars, Stamp, ModelCar, Status)
               .join(Stamp)
               .join(ModelCar)
               .join(Status)
               .where(Cars.id == car_id)
               .first())
        
        if not car:
            raise HTTPException(404, "Автомобиль не найден")
        
        return {
            "id": car.id,
            "stamp": car.stamp_id.stamp,
            "model": car.model_car_id.model_car,
            "run_km": car.run_km,
            "vin": car.vin,
            "status": car.status_id.status,
            "price": car.price,
            "description": car.description
        }
    except HTTPException as http_exc:
        raise http_exc


                    # Функционал Администратора

@app.delete("/admin/users/delete_profile/", tags=["Admin"])
async def delete_profile_user(user_id: int, token: str = Header(...)):
    """Удаления профиля пользователя"""

    current_user = get_user_by_token(token, "Администратор")
    try:
        if not current_user:
            raise HTTPException(401, 'Недействительный токен.')
        
        user = Users.select().where(Users.id==user_id).first()
        if not user:
            raise HTTPException(404, 'Пользователь с указанным ID не найден.')
        
        if user.id == current_user.id:
            raise HTTPException(400, 'Аккаунт данного пользователя нельзя удалить.')
        
        user.delete_instance()
        return {'message': 'Пользователь успешно удален.'}
    except HTTPException as http_exc:
        raise http_exc


@app.get("/admin/anketi/", tags=["Admin"])
async def get_all_anketi(token: str = Header(...)):
    """Получение всех анкет для администратора"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        if not current_user:
            raise HTTPException(401, 'Недействительный токен.')
        anketi = (Anketa
                .select(Anketa, Users)
                .join(Users))
        
        return [{
            "id": anketa.id,
            "user_name": anketa.user_id.full_name,
            "user_phone": anketa.user_id.phone,
            "stamp": anketa.stamp,
            "model_car": anketa.model_car,
            "run": anketa.run,
            "price": anketa.price,
            "vin": anketa.vin,
            "description": anketa.description
        } for anketa in anketi]
    except HTTPException as http_exc:
        raise http_exc


@app.post("/admin/anketi/{anketa_id}/accept", tags=["Admin"])
async def accept_anketa(anketa_id: int, token: str = Header(...)):
    """Принятие анкеты администратором (покупка автомобиля у пользователя)"""
    current_user = get_user_by_token(token, "Администратор")

    try:
        anketa = Anketa.select().where(Anketa.id == anketa_id).first()
        if not anketa:
            raise HTTPException(404, "Анкета не найдена")

        existing_car = Cars.select().where(Cars.vin == anketa.vin).first()
        if existing_car:
            raise HTTPException(400, "Автомобиль с таким VIN уже существует в базе")

        stamp, _ = Stamp.get_or_create(
            stamp=anketa.stamp,
            defaults={'stamp': anketa.stamp}
        )

        model_car, _ = ModelCar.get_or_create(
            model_car=anketa.model_car,
            defaults={'model_car': anketa.model_car}
        )

        available_status = Status.get(Status.status == "Доступен")

        car = Cars.create(
            stamp_id=stamp.id,
            model_car_id=model_car.id,
            run_km=anketa.run,
            vin=anketa.vin,
            status_id=available_status.id,
            price=anketa.price,
            description=anketa.description
        )

        Sales.create(
            car_id=car.id,
            buyer_id=current_user.id,
            price=anketa.price
        )

        anketa.delete_instance()

        return {"message": "Анкета принята, автомобиль добавлен в базу"}
    except HTTPException as http_exc:
        raise http_exc


@app.post("/admin/cars/", tags=["Admin"])
async def add_car(car_data: CarsCreated, token: str = Header(...)):
    """Добавление автомобиля администратором"""
    current_user = get_user_by_token(token, "Администратор")

    try:
        if not current_user:
            raise HTTPException(401, 'Недействительный токен.')
        vin = Cars.select().where(Cars.vin == car_data.vin)
        if vin:
            raise HTTPException(400, "Данный автомобиль уже есть в базе")
        available_status = Status.get(Status.status == "Доступен")
        stamp, _ = Stamp.get_or_create(
            stamp=car_data.stamp,
            defaults={'stamp': car_data.stamp}
        )

        model_car, _ = ModelCar.get_or_create(
            model_car=car_data.model_car,
            defaults={'model_car': car_data.model_car}
        )

        car = Cars.create(
            stamp_id=stamp.id,
            model_car_id=model_car.id,
            run_km=car_data.run,
            vin=car_data.vin,
            status_id=available_status.id,
            price=car_data.price,
            description=car_data.description
        )
        
        return {"message": "Автомобиль успешно добавлен", "car_id": car.id}
    except HTTPException as http_exc:
        raise http_exc


@app.put("/admin/cars/{car_id}", tags=["Admin"])
async def update_car(car_id: int, car_data: CarsUpdate, token: str = Header(...)):
    """Обновление информации об автомобиле"""
    current_user = get_user_by_token(token, "Администратор")

    try:
        car = Cars.select().where(Cars.id == car_id).first()
        if not car:
            raise HTTPException(404, "Автомобиль не найден")

        if car_data.price:
            car.price = car_data.price
        if car_data.run:
            car.run_km = car_data.run
        if car_data.status_id:
            status_exists = Status.get_or_none(Status.id == car_data.status_id)
            if not status_exists:
                raise HTTPException(404, "Указанный статус не найден")
            car.status_id = car_data.status_id
        if car_data.description:
            car.description = car_data.description
        
        car.save()
        
        return {"message": "Информация об автомобиле обновлена"}
    except HTTPException as http_exc:
        raise http_exc


@app.get("/admin/stamps/", tags=["Users"])
async def get_all_stamps(token: str = Header(...)):
    """Получение всех марок автомобилей"""
    get_user_by_token(token)
    try:
        stamps = Stamp.select()
        return [{
            "id": stamp.id,
            "stamp": stamp.stamp
        } for stamp in stamps]
    except HTTPException as http_exc:
        raise http_exc


@app.post("/admin/stamps/", tags=["Admin"])
async def create_stamp(stamp_data: StampCreate, token: str = Header(...)):
    """Создание новой марки автомобиля"""
    get_user_by_token(token, "Администратор")
    try:
        existing_stamp = Stamp.select().where(Stamp.stamp == stamp_data.stamp).first()
        if existing_stamp:
            raise HTTPException(400, "Марка с таким названием уже существует")
        
        stamp = Stamp.create(stamp=stamp_data.stamp)
        return {"message": "Марка успешно создана", "stamp_id": stamp.id}
    except HTTPException as http_exc:
        raise http_exc

@app.put("/admin/stamps/{stamp_id}", tags=["Admin"])
async def update_stamp(stamp_id: int, stamp_data: StampCreate, token: str = Header(...)):
    """Обновление марки автомобиля"""
    get_user_by_token(token, "Администратор")
    try:
        stamp = Stamp.select().where(Stamp.id == stamp_id).first()
        if not stamp:
            raise HTTPException(404, "Марка не найдена")
        
        existing_stamp = Stamp.select().where((Stamp.stamp == stamp_data.stamp) & (Stamp.id != stamp_id)).first()
        if existing_stamp:
            raise HTTPException(400, "Марка с таким названием уже существует")
        
        stamp.stamp = stamp_data.stamp
        stamp.save()
        return {"message": "Марка успешно обновлена"}
    except HTTPException as http_exc:
        raise http_exc

@app.delete("/admin/stamps/{stamp_id}", tags=["Admin"])
async def delete_stamp(stamp_id: int, token: str = Header(...)):
    """Удаление марки автомобиля"""
    get_user_by_token(token, "Администратор")
    try:
        stamp = Stamp.select().where(Stamp.id == stamp_id).first()
        if not stamp:
            raise HTTPException(404, "Марка не найдена")
        
        cars_with_stamp = Cars.select().where(Cars.stamp_id == stamp_id).first()
        if cars_with_stamp:
            raise HTTPException(400, "Невозможно удалить марку, так как она используется в автомобилях")
        
        stamp.delete_instance()
        return {"message": "Марка успешно удалена"}
    except HTTPException as http_exc:
        raise http_exc


@app.get("/admin/models/", tags=["Users"])
async def get_all_models(token: str = Header(...)):
    """Получение всех моделей автомобилей"""
    get_user_by_token(token)
    try:
        models = ModelCar.select()
        return [{
            "id": model.id,
            "model_car": model.model_car
        } for model in models]
    except HTTPException as http_exc:
        raise http_exc


@app.post("/admin/models/", tags=["Admin"])
async def create_model(model_data: ModelCarCreate, token: str = Header(...)):
    """Создание новой модели автомобиля"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        existing_model = ModelCar.select().where(ModelCar.model_car == model_data.model_car).first()
        if existing_model:
            raise HTTPException(400, "Модель с таким названием уже существует")
        
        model = ModelCar.create(model_car=model_data.model_car)
        return {"message": "Модель успешно создана", "model_id": model.id}
    except HTTPException as http_exc:
        raise http_exc


@app.put("/admin/models/{model_id}", tags=["Admin"])
async def update_model(model_id: int, model_data: ModelCarCreate, token: str = Header(...)):
    """Обновление модели автомобиля"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        model = ModelCar.select().where(ModelCar.id == model_id).first()
        if not model:
            raise HTTPException(404, "Модель не найдена")
        
        existing_model = ModelCar.select().where((ModelCar.model_car == model_data.model_car) & (ModelCar.id != model_id)).first()
        if existing_model:
            raise HTTPException(400, "Модель с таким названием уже существует")
        
        model.model_car = model_data.model_car
        model.save()
        return {"message": "Модель успешно обновлена"}
    except HTTPException as http_exc:
        raise http_exc


@app.delete("/admin/models/{model_id}", tags=["Admin"])
async def delete_model(model_id: int, token: str = Header(...)):
    """Удаление модели автомобиля"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        model = ModelCar.select().where(ModelCar.id == model_id).first()
        if not model:
            raise HTTPException(404, "Модель не найдена")
        
        cars_with_model = Cars.select().where(Cars.model_car_id == model_id).first()
        if cars_with_model:
            raise HTTPException(400, "Невозможно удалить модель, так как она используется в автомобилях")
        
        model.delete_instance()
        return {"message": "Модель успешно удалена"}
    except HTTPException as http_exc:
        raise http_exc


@app.get("/admin/cars/", tags=["Admin"])
async def get_all_cars(token: str = Header(...)):
    """Получение всех автомобилей"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        cars = (Cars
                .select(Cars, Stamp, ModelCar, Status)
                .join(Stamp, on=(Cars.stamp_id == Stamp.id))
                .join(ModelCar, on=(Cars.model_car_id == ModelCar.id))
                .join(Status, on=(Cars.status_id == Status.id)))
        
        return [{
            "id": car.id,
            "stamp": car.stamp_id.stamp,
            "model": car.model_car_id.model_car,
            "run_km": car.run_km,
            "vin": car.vin,
            "status": car.status_id.status,
            "price": car.price,
            "description": car.description
        } for car in cars]
    except HTTPException as http_exc:
        raise http_exc


@app.get("/admin/cars/{car_id}", tags=["Admin"])
async def get_car(car_id: int, token: str = Header(...)):
    """Получение информации об автомобиле по ID"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        car = (Cars
               .select(Cars, Stamp, ModelCar, Status)
               .join(Stamp, on=(Cars.stamp_id == Stamp.id))
               .join(ModelCar, on=(Cars.model_car_id == ModelCar.id))
               .join(Status, on=(Cars.status_id == Status.id))
               .where(Cars.id == car_id)
               .first())
        
        if not car:
            raise HTTPException(404, "Автомобиль не найден")
        
        return {
            "id": car.id,
            "stamp": car.stamp_id.stamp,
            "model": car.model_car_id.model_car,
            "run_km": car.run_km,
            "vin": car.vin,
            "status": car.status_id.status,
            "price": car.price,
            "description": car.description
        }
    except HTTPException as http_exc:
        raise http_exc


@app.delete("/admin/cars/{car_id}", tags=["Admin"])
async def delete_car(car_id: int, token: str = Header(...)):
    """Удаление автомобиля"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        car = Cars.select().where(Cars.id == car_id).first()
        if not car:
            raise HTTPException(404, "Автомобиль не найден")
        
        shopping_records = Shopping.select().where(Shopping.car_id == car_id).first()
        if shopping_records:
            raise HTTPException(400, "Невозможно удалить автомобиль, так как есть связанные покупки")
        
        sales_records = Sales.select().where(Sales.car_id == car_id).first()
        if sales_records:
            raise HTTPException(400, "Невозможно удалить автомобиль, так как есть связанные продажи")
        
        car.delete_instance()
        return {"message": "Автомобиль успешно удален"}
    except HTTPException as http_exc:
        raise http_exc


@app.get("/admin/shopping/", tags=["Admin"])
async def get_all_shopping(token: str = Header(...)):
    """Получение всех записей о покупках"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        shopping = (Shopping
                    .select(Shopping, Cars, Users)
                    .join(Cars)
                    .join(Users, on=(Shopping.buyer_id == Users.id)))
        
        return [{
            "id": shop.id,
            "car": {
                "id": shop.car_id.id,
                "stamp": shop.car_id.stamp_id.stamp,
                "model": shop.car_id.model_car_id.model_car,
                "vin": shop.car_id.vin
            },
            "buyer": {
                "id": shop.buyer_id.id,
                "name": shop.buyer_id.full_name,
                "email": shop.buyer_id.email
            },
            "date_buy": shop.date_buy.isoformat(),
            "price": shop.price
        } for shop in shopping]
    except HTTPException as http_exc:
        raise http_exc

@app.post("/admin/shopping/", tags=["Admin"])
async def create_shopping(shopping_data: ShoppingCreate, token: str = Header(...)):
    """Создание записи о покупке"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        car = Cars.select().where(Cars.id == shopping_data.car_id).first()
        if not car:
            raise HTTPException(404, "Автомобиль не найден")

        user = Users.select().where(Users.id == shopping_data.buyer_id).first()
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        
        shopping = Shopping.create(
            car_id=shopping_data.car_id,
            buyer_id=shopping_data.buyer_id,
            price=shopping_data.price
        )
        
        return {"message": "Запись о покупке создана", "shopping_id": shopping.id}
    except HTTPException as http_exc:
        raise http_exc

@app.delete("/admin/shopping/{shopping_id}", tags=["Admin"])
async def delete_shopping(shopping_id: int, token: str = Header(...)):
    """Удаление записи о покупке"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        shopping = Shopping.select().where(Shopping.id == shopping_id).first()
        if not shopping:
            raise HTTPException(404, "Запись о покупке не найдена")
        
        shopping.delete_instance()
        return {"message": "Запись о покупке удалена"}
    except HTTPException as http_exc:
        raise http_exc


@app.get("/admin/sales/", tags=["Admin"])
async def get_all_sales(token: str = Header(...)):
    """Получение всех записей о продажах"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        sales = (Sales
                 .select(Sales, Cars, Users)
                 .join(Cars)
                 .join(Users, on=(Sales.buyer_id == Users.id)))
        
        return [{
            "id": sale.id,
            "car": {
                "id": sale.car_id.id,
                "stamp": sale.car_id.stamp_id.stamp,
                "model": sale.car_id.model_car_id.model_car,
                "vin": sale.car_id.vin
            },
            "buyer": {
                "id": sale.buyer_id.id,
                "name": sale.buyer_id.full_name,
                "email": sale.buyer_id.email
            },
            "date_sale": sale.date_sale.isoformat(),
            "price": sale.price
        } for sale in sales]
    except HTTPException as http_exc:
        raise http_exc

@app.post("/admin/sales/", tags=["Admin"])
async def create_sale(sale_data: SalesCreate, token: str = Header(...)):
    """Создание записи о продаже"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        car = Cars.select().where(Cars.id == sale_data.car_id).first()
        if not car:
            raise HTTPException(404, "Автомобиль не найден")
        
        user = Users.select().where(Users.id == sale_data.buyer_id).first()
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        
        sale = Sales.create(
            car_id=sale_data.car_id,
            buyer_id=sale_data.buyer_id,
            price=sale_data.price
        )
        
        return {"message": "Запись о продаже создана", "sale_id": sale.id}
    except HTTPException as http_exc:
        raise http_exc


@app.delete("/admin/sales/{sale_id}", tags=["Admin"])
async def delete_sale(sale_id: int, token: str = Header(...)):
    """Удаление записи о продаже"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        sale = Sales.select().where(Sales.id == sale_id).first()
        if not sale:
            raise HTTPException(404, "Запись о продаже не найдена")
        
        sale.delete_instance()
        return {"message": "Запись о продаже удалена"}
    except HTTPException as http_exc:
        raise http_exc


@app.post("/admin/users/", tags=["Admin"])
async def create_user(user: Registration, token: str = Header(...)):
    """Создание нового пользователя администратором"""
    current_user = get_user_by_token(token, "Администратор")
    if not re.fullmatch(EMAIL_REGEX, user.email) or not re.fullmatch(PHONE_REGEX, user.phone):
        raise HTTPException(400, 'Неверный формат данных email/номера телефона')
    try:
        email = user.email.lower()
        existing_user = Users.select().where((Users.email==email) | (Users.phone==user.phone)).first()
        if existing_user:
            raise HTTPException(403, 'Пользователь с таким email/номером телефона уже существует.')

        hashed_password = ph.hash(user.password)
        with database_connection.atomic():
            user_role = Roles.get(Roles.name=='Пользователь')
            new_user = Users.create(
                email=email,
                phone=user.phone,
                full_name=user.full_name,
                password=hashed_password,
            )
            UserRoles.create(
                user_id=new_user.id,
                role_id=user_role.id)

        return {'message': 'Пользователь успешно создан!', 'user_id': new_user.id}
    except HTTPException as http_exc:
        raise http_exc


@app.put("/admin/users/{user_id}", tags=["Admin"])
async def update_user(user_id: int, user_data: UserUpdate, token: str = Header(...)):
    """Обновление профиля пользователя администратором"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        user = Users.select().where(Users.id == user_id).first()
        if not user:
            raise HTTPException(404, "Пользователь не найден")
            
        if user_data.phone and not re.fullmatch(PHONE_REGEX, user_data.phone):
            raise HTTPException(400, 'Неверный формат номера телефона')
            
        if user_data.phone:
            existing_phone = Users.get_or_none(Users.phone == user_data.phone)
            if existing_phone and existing_phone.id != user_id:
                raise HTTPException(400, 'Номер телефона уже используется')
        
        if user_data.full_name:
            user.full_name = user_data.full_name
        if user_data.phone:
            user.phone = user_data.phone
            
        user.save()
        return {"message": "Профиль пользователя успешно обновлен"}
    except HTTPException as http_exc:
        raise http_exc


@app.get("/admin/users/{user_id}", tags=["Admin"])
async def get_user(user_id: int, token: str = Header(...)):
    """Получение информации о пользователе по ID"""
    current_user = get_user_by_token(token, "Администратор")
    try:
        user = Users.select().where(Users.id == user_id).first()
        if not user:
            raise HTTPException(404, "Пользователь не найден")
        
        user_role = (Roles
                    .select()
                    .join(UserRoles, on=(UserRoles.role_id == Roles.id))
                    .where(UserRoles.user_id == user)
                    .first())
        
        
        return {
            "id": user.id,
            "name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "role": user_role.name
        }
    except HTTPException as http_exc:
        raise http_exc


@app.post('/users/logout/', tags=['Users'])
async def logout_user(token: str = Header(...)):
    """Выход пользователя из системы"""
    try:
        user_token = UserToken.select().where(UserToken.token == token).first()
        if user_token:
            user_token.delete_instance()
        return {'message': 'Вы успешно вышли из системы'}
    except HTTPException as http_exc:
        raise http_exc
    

