# test_data.py
"""Скрипт для заполнения базы тестовыми данными"""

from api import ph
from models import *
from datetime import datetime, timedelta

def create_test_data():
    """Создание тестовых данных"""
    
    # Очистка существующих данных (опционально)
    # UserToken.delete().execute()
    # UserRoles.delete().execute()
    # Shopping.delete().execute()
    # Sales.delete().execute()
    # Anketa.delete().execute()
    # Cars.delete().execute()
    # Users.delete().execute()
    # Stamp.delete().execute()
    # ModelCar.delete().execute()
    
    try:
        with database_connection.atomic():
            # 1. Создание пользователей
            users_data = [
                {
                    'email': 'admin@example.com',
                    'phone': '+79101234567',
                    'full_name': 'Иванов Алексей Петрович',
                    'password': ph.hash('admin123')
                },
                {
                    'email': 'user1@example.com', 
                    'phone': '+79101234568',
                    'full_name': 'Петров Сергей Иванович',
                    'password': ph.hash('user123')
                },
                {
                    'email': 'user2@example.com',
                    'phone': '+79101234569', 
                    'full_name': 'Сидорова Мария Владимировна',
                    'password': ph.hash('user123')
                }
            ]
            
            users = []
            for user_data in users_data:
                user = Users.create(**user_data)
                users.append(user)
            
            # 2. Назначение ролей
            admin_role = Roles.get(Roles.name == 'Администратор')
            user_role = Roles.get(Roles.name == 'Пользователь')
            
            UserRoles.create(user_id=users[0], role_id=admin_role)  # Админ
            UserRoles.create(user_id=users[1], role_id=user_role)   # Обычный пользователь
            UserRoles.create(user_id=users[2], role_id=user_role)   # Обычный пользователь
            
            # 4. Создание марок автомобилей
            stamps_data = ['Toyota', 'BMW', 'Mercedes', 'Audi', 'Honda']
            stamps = []
            for stamp_name in stamps_data:
                stamp = Stamp.create(stamp=stamp_name)
                stamps.append(stamp)
            
            # 5. Создание моделей автомобилей
            models_data = [
                'Camry', 'X5', 'E-Class', 'A4', 'Civic', 'Corolla', '3 Series'
            ]
            models = []
            for model_name in models_data:
                model = ModelCar.create(model_car=model_name)
                models.append(model)
            
            # 6. Получение статусов
            status_available = Status.get(Status.status == 'Доступен')
            status_sold = Status.get(Status.status == 'Продан')
            
            # 7. Создание автомобилей
            cars_data = [
                {
                    'stamp_id': stamps[0],  # Toyota
                    'model_car_id': models[0],  # Camry
                    'run_km': 45000,
                    'vin': 'JTDBT123456789012',
                    'status_id': status_available,
                    'price': 1850000,
                    'description': 'Отличное состояние, один владелец'
                },
                {
                    'stamp_id': stamps[1],  # BMW
                    'model_car_id': models[1],  # X5
                    'run_km': 78000,
                    'vin': 'WBA12345678901234',
                    'status_id': status_available,
                    'price': 3200000,
                    'description': 'Полный комплект, сервисная история'
                },
                {
                    'stamp_id': stamps[2],  # Mercedes
                    'model_car_id': models[2],  # E-Class
                    'run_km': 120000,
                    'vin': 'WDD12345678901234',
                    'status_id': status_sold,
                    'price': 2800000,
                    'description': 'Требуется замена масла'
                },
                {
                    'stamp_id': stamps[3],  # Audi
                    'model_car_id': models[3],  # A4
                    'run_km': 65000,
                    'vin': 'WAU12345678901234',
                    'status_id': status_available,
                    'price': 2100000,
                    'description': 'Идеальное состояние'
                },
                {
                    'stamp_id': stamps[0],  # Toyota
                    'model_car_id': models[5],  # Corolla
                    'run_km': 34000,
                    'vin': 'JTDBT123456789013',
                    'status_id': status_available,
                    'price': 1650000,
                    'description': 'Экономичный вариант'
                }
            ]
            
            cars = []
            for car_data in cars_data:
                car = Cars.create(**car_data)
                cars.append(car)
            
            # 8. Создание анкет
            anketa_data = [
                {
                    'user_id': users[1],  # user1
                    'stamp': 'Toyota',
                    'model_car': 'Camry', 
                    'run': 60000,
                    'price': 1500000,
                    'vin': 'JTDBT123456789014'
                },
                {
                    'user_id': users[2],  # user2
                    'stamp': 'BMW',
                    'model_car': '3 Series',
                    'run': 85000,
                    'price': 1800000,
                    'vin': 'WBA12345678901235'
                },
                {
                    'user_id': users[1],  # user1
                    'stamp': 'Honda',
                    'model_car': 'Civic',
                    'run': 45000,
                    'price': 1200000,
                    'vin': 'JHMBT123456789012'
                }
            ]
            
            for anketa_item in anketa_data:
                Anketa.create(**anketa_item)
            
            # 9. Создание записей о покупках
            shopping_data = [
                {
                    'car_id': cars[2],  # Mercedes (продан)
                    'buyer_id': users[1],  # user1
                    'price': 2800000
                },
                {
                    'car_id': cars[4],  # Toyota Corolla
                    'buyer_id': users[2],  # user2  
                    'price': 1650000
                }
            ]
            
            for shop_item in shopping_data:
                Shopping.create(**shop_item)
            
            # 10. Создание записей о продажах
            sales_data = [
                {
                    'car_id': cars[0],  # Toyota Camry
                    'buyer_id': users[1],  # user1
                    'price': 1850000
                },
                {
                    'car_id': cars[3],  # Audi A4
                    'buyer_id': users[2],  # user2
                    'price': 2100000
                }
            ]
            
            for sale_item in sales_data:
                Sales.create(**sale_item)
            
            print("Тестовые данные успешно созданы!")
            print(f"Создано: {len(users)} пользователей, {len(stamps)} марок, {len(models)} моделей, {len(cars)} автомобилей")
            
    except Exception as e:
        print(f"Ошибка при создании тестовых данных: {e}")
        database_connection.rollback()

if __name__ == "__main__":
    create_test_data()