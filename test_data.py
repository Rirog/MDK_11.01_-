from database import database_connection
from models import Users, Roles, UserRoles, Stamp, ModelCar, Status, Cars, Anketa, Shopping, Sales
from argon2 import PasswordHasher
import re
from datetime import datetime, timedelta

ph = PasswordHasher()

def seed_database():
    """Функция для заполнения базы данных тестовыми данными (минимум 15 записей)"""
    
    try:
        database_connection.connect()
        
        print("🚀 Начинаем заполнение базы данных тестовыми записями...")
        
        # 1. Проверка и добавление ролей
        print("\n1. Проверка ролей...")
        roles_data = [
            {"name": "Администратор"},
            {"name": "Пользователь"},
            {"name": "Менеджер"}
        ]
        
        for role_data in roles_data:
            role, created = Roles.get_or_create(name=role_data["name"])
            if created:
                print(f"   ✅ Роль '{role.name}' создана")
            else:
                print(f"   ℹ️  Роль '{role.name}' уже существует")
        
        # 2. Проверка и добавление статусов
        print("\n2. Проверка статусов...")
        statuses_data = [
            {"status": "Доступен"},
            {"status": "Продан"},
        ]
        
        for status_data in statuses_data:
            status, created = Status.get_or_create(status=status_data["status"])
            if created:
                print(f"   ✅ Статус '{status.status}' создан")
            else:
                print(f"   ℹ️  Статус '{status.status}' уже существует")
        
        # 3. Проверка и добавление марок автомобилей (10+ записей)
        print("\n3. Проверка марок автомобилей...")
        stamps_data = [
            {"stamp": "Toyota"}, {"stamp": "Honda"}, {"stamp": "BMW"}, 
            {"stamp": "Mercedes-Benz"}, {"stamp": "Audi"}, {"stamp": "Ford"},
            {"stamp": "Volkswagen"}, {"stamp": "Nissan"}, {"stamp": "Hyundai"},
            {"stamp": "Kia"}, {"stamp": "Lexus"}, {"stamp": "Mazda"},
            {"stamp": "Subaru"}, {"stamp": "Volvo"}, {"stamp": "Chevrolet"}
        ]
        
        for stamp_data in stamps_data:
            stamp, created = Stamp.get_or_create(stamp=stamp_data["stamp"])
            if created:
                print(f"   ✅ Марка '{stamp.stamp}' создана")
            else:
                print(f"   ℹ️  Марка '{stamp.stamp}' уже существует")
        
        print("\n4. Проверка моделей автомобилей...")
        models_data = [
            {"model_car": "Camry"}, {"model_car": "Civic"}, {"model_car": "X5"},
            {"model_car": "E-Class"}, {"model_car": "A4"}, {"model_car": "Focus"},
            {"model_car": "Golf"}, {"model_car": "Altima"}, {"model_car": "Elantra"},
            {"model_car": "Rio"}, {"model_car": "RX"}, {"model_car": "CX-5"},
            {"model_car": "Outback"}, {"model_car": "XC60"}, {"model_car": "Cruze"},
            {"model_car": "Corolla"}, {"model_car": "Accord"}, {"model_car": "3 Series"},
            {"model_car": "C-Class"}, {"model_car": "Q5"}
        ]
        
        for model_data in models_data:
            model, created = ModelCar.get_or_create(model_car=model_data["model_car"])
            if created:
                print(f"   ✅ Модель '{model.model_car}' создана")
            else:
                print(f"   ℹ️  Модель '{model.model_car}' уже существует")
        
        # 5. Проверка и добавление администраторов (3 записи)
        print("\n5. Проверка администраторов...")
        admins_data = [
            {
                "email": "limon@gmail.com",
                "phone": "+79991234567",
                "full_name": "Главный Администратор",
                "password": "root"
            }
        ]
        
        admin_role = Roles.get(Roles.name == "Администратор")
        
        for admin_data in admins_data:
            if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', admin_data["email"]):
                print(f"   ❌ Неверный формат email: {admin_data['email']}")
                continue
                
            if not re.match(r'^\+7\d{10}$', admin_data["phone"]):
                print(f"   ❌ Неверный формат телефона: {admin_data['phone']}")
                continue
            
            admin, created = Users.get_or_create(
                email=admin_data["email"],
                defaults={
                    'phone': admin_data["phone"],
                    'full_name': admin_data["full_name"],
                    'password': ph.hash(admin_data["password"])
                }
            )
            
            if created:
                UserRoles.create(user_id=admin.id, role_id=admin_role.id)
                print(f"   ✅ Администратор '{admin.full_name}' создан")
            else:
                print(f"   ℹ️  Администратор '{admin.full_name}' уже существует")
        
        # 6. Проверка и добавление тестовых пользователей (10+ записей)
        print("\n6. Проверка тестовых пользователей...")
        users_data = [
            {"email": "user1@example.com", "phone": "+79992345678", "full_name": "Иван Петров", "password": "user123"},
            {"email": "user2@example.com", "phone": "+79993456789", "full_name": "Мария Сидорова", "password": "user123"},
            {"email": "user3@example.com", "phone": "+79994567890", "full_name": "Алексей Козлов", "password": "user123"},
            {"email": "user4@example.com", "phone": "+79995678901", "full_name": "Екатерина Новикова", "password": "user123"},
            {"email": "user5@example.com", "phone": "+79996789012", "full_name": "Дмитрий Васильев", "password": "user123"},
            {"email": "user6@example.com", "phone": "+79997890123", "full_name": "Ольга Михайлова", "password": "user123"},
            {"email": "user7@example.com", "phone": "+79998901234", "full_name": "Сергей Федоров", "password": "user123"},
            {"email": "user8@example.com", "phone": "+79999012345", "full_name": "Анна Смирнова", "password": "user123"},
            {"email": "user9@example.com", "phone": "+79990123456", "full_name": "Павел Морозов", "password": "user123"},
            {"email": "user10@example.com", "phone": "+79991234560", "full_name": "Наталья Воробьева", "password": "user123"},
            {"email": "user11@example.com", "phone": "+79992234561", "full_name": "Виктор Орлов", "password": "user123"},
            {"email": "user12@example.com", "phone": "+79993234562", "full_name": "Юлия Зайцева", "password": "user123"}
        ]
        
        user_role = Roles.get(Roles.name == "Пользователь")
        
        for user_data in users_data:
            if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', user_data["email"]):
                print(f"   ❌ Неверный формат email: {user_data['email']}")
                continue
                
            if not re.match(r'^\+7\d{10}$', user_data["phone"]):
                print(f"   ❌ Неверный формат телефона: {user_data['phone']}")
                continue
            
            user, created = Users.get_or_create(
                email=user_data["email"],
                defaults={
                    'phone': user_data["phone"],
                    'full_name': user_data["full_name"],
                    'password': ph.hash(user_data["password"])
                }
            )
            
            if created:
                UserRoles.create(user_id=user.id, role_id=user_role.id)
                print(f"   ✅ Пользователь '{user.full_name}' создан")
            else:
                print(f"   ℹ️  Пользователь '{user.full_name}' уже существует")
        
        # 7. Проверка и добавление тестовых автомобилей (15+ записей)
        print("\n7. Проверка тестовых автомобилей...")
        
        # Получаем необходимые данные
        available_status = Status.get(Status.status == "Доступен")
        sold_status = Status.get(Status.status == "Продан")
        
        # Получаем марки и модели
        toyota_stamp = Stamp.get(Stamp.stamp == "Toyota")
        honda_stamp = Stamp.get(Stamp.stamp == "Honda") 
        bmw_stamp = Stamp.get(Stamp.stamp == "BMW")
        mercedes_stamp = Stamp.get(Stamp.stamp == "Mercedes-Benz")
        audi_stamp = Stamp.get(Stamp.stamp == "Audi")
        ford_stamp = Stamp.get(Stamp.stamp == "Ford")
        vw_stamp = Stamp.get(Stamp.stamp == "Volkswagen")
        nissan_stamp = Stamp.get(Stamp.stamp == "Nissan")
        hyundai_stamp = Stamp.get(Stamp.stamp == "Hyundai")
        kia_stamp = Stamp.get(Stamp.stamp == "Kia")
        lexus_stamp = Stamp.get(Stamp.stamp == "Lexus")
        mazda_stamp = Stamp.get(Stamp.stamp == "Mazda")
        subaru_stamp = Stamp.get(Stamp.stamp == "Subaru")
        volvo_stamp = Stamp.get(Stamp.stamp == "Volvo")
        chevrolet_stamp = Stamp.get(Stamp.stamp == "Chevrolet")
        
        camry_model = ModelCar.get(ModelCar.model_car == "Camry")
        civic_model = ModelCar.get(ModelCar.model_car == "Civic")
        x5_model = ModelCar.get(ModelCar.model_car == "X5")
        eclass_model = ModelCar.get(ModelCar.model_car == "E-Class")
        a4_model = ModelCar.get(ModelCar.model_car == "A4")
        focus_model = ModelCar.get(ModelCar.model_car == "Focus")
        golf_model = ModelCar.get(ModelCar.model_car == "Golf")
        altima_model = ModelCar.get(ModelCar.model_car == "Altima")
        elantra_model = ModelCar.get(ModelCar.model_car == "Elantra")
        rio_model = ModelCar.get(ModelCar.model_car == "Rio")
        rx_model = ModelCar.get(ModelCar.model_car == "RX")
        cx5_model = ModelCar.get(ModelCar.model_car == "CX-5")
        outback_model = ModelCar.get(ModelCar.model_car == "Outback")
        xc60_model = ModelCar.get(ModelCar.model_car == "XC60")
        cruze_model = ModelCar.get(ModelCar.model_car == "Cruze")
        corolla_model = ModelCar.get(ModelCar.model_car == "Corolla")
        accord_model = ModelCar.get(ModelCar.model_car == "Accord")
        three_series_model = ModelCar.get(ModelCar.model_car == "3 Series")
        cclass_model = ModelCar.get(ModelCar.model_car == "C-Class")
        q5_model = ModelCar.get(ModelCar.model_car == "Q5")
        
        cars_data = [
            # Доступные автомобили (10+ записей)
            {"stamp_id": toyota_stamp, "model_car_id": camry_model, "run_km": 45000, "vin": "JTDBR32E160123401", "status_id": available_status, "price": 1500000, "description": "Отличное состояние, один владелец, полная сервисная история"},
            {"stamp_id": honda_stamp, "model_car_id": civic_model, "run_km": 32000, "vin": "2HGFA16507H123402", "status_id": available_status, "price": 1200000, "description": "Экономичный и надежный автомобиль, низкий расход"},
            {"stamp_id": bmw_stamp, "model_car_id": x5_model, "run_km": 78000, "vin": "5UXKR0C58K0L123403", "status_id": available_status, "price": 3500000, "description": "Премиум класс, полный комплект, кожаный салон"},
            {"stamp_id": mercedes_stamp, "model_car_id": eclass_model, "run_km": 55000, "vin": "WDDHF5EB7EA123404", "status_id": available_status, "price": 2800000, "description": "Комфорт и роскошь, система помощи водителю"},
            {"stamp_id": audi_stamp, "model_car_id": a4_model, "run_km": 42000, "vin": "WAUFFAFLXFN123405", "status_id": available_status, "price": 2200000, "description": "Немецкое качество, полный привод, климат-контроль"},
            {"stamp_id": ford_stamp, "model_car_id": focus_model, "run_km": 67000, "vin": "1FADP3F2XEL123406", "status_id": available_status, "price": 950000, "description": "Надежный хетчбек, идеален для города"},
            {"stamp_id": vw_stamp, "model_car_id": golf_model, "run_km": 38000, "vin": "3VW467ATXHM123407", "status_id": available_status, "price": 1100000, "description": "Культовый Golf, отличная динамика"},
            {"stamp_id": nissan_stamp, "model_car_id": altima_model, "run_km": 51000, "vin": "1N4AL3AP6JC123408", "status_id": available_status, "price": 1300000, "description": "Просторный салон, комфортная подвеска"},
            {"stamp_id": hyundai_stamp, "model_car_id": elantra_model, "run_km": 29000, "vin": "5NPDH4AE6FH123409", "status_id": available_status, "price": 1050000, "description": "Современный дизайн, богатая комплектация"},
            {"stamp_id": kia_stamp, "model_car_id": rio_model, "run_km": 23000, "vin": "KNAFU5A20E5123410", "status_id": available_status, "price": 890000, "description": "Экономичный седан, малый расход"},
            {"stamp_id": lexus_stamp, "model_car_id": rx_model, "run_km": 34000, "vin": "2T2ZZMCA5JC123411", "status_id": available_status, "price": 4200000, "description": "Премиум кроссовер, тихая работа"},
            {"stamp_id": mazda_stamp, "model_car_id": cx5_model, "run_km": 41000, "vin": "JM3KFBDL0H0123412", "status_id": available_status, "price": 1850000, "description": "Стильный дизайн, отличная управляемость"},
            {"stamp_id": subaru_stamp, "model_car_id": outback_model, "run_km": 62000, "vin": "4S4BSANC1H3123413", "status_id": available_status, "price": 1950000, "description": "Полный привод, универсал для любых дорог"},
            
            # Проданные автомобили (5+ записей)
            {"stamp_id": volvo_stamp, "model_car_id": xc60_model, "run_km": 47000, "vin": "YV4A22PK5J1123414", "status_id": sold_status, "price": 2400000, "description": "Безопасность и комфорт, продан 01.01.2024"},
            {"stamp_id": chevrolet_stamp, "model_car_id": cruze_model, "run_km": 58000, "vin": "1G1PE5SB3G7123415", "status_id": sold_status, "price": 850000, "description": "Надежный американский седан, продан"},
            {"stamp_id": toyota_stamp, "model_car_id": corolla_model, "run_km": 25000, "vin": "2T1BURHE9JC123416", "status_id": sold_status, "price": 1150000, "description": "Классическая надежность, продан"},
            {"stamp_id": honda_stamp, "model_car_id": accord_model, "run_km": 36000, "vin": "1HGCR2F73HA123417", "status_id": sold_status, "price": 1650000, "description": "Просторный седан бизнес-класса, продан"},
            {"stamp_id": bmw_stamp, "model_car_id": three_series_model, "run_km": 44000, "vin": "WBA8E9C58J8123418", "status_id": sold_status, "price": 2650000, "description": "Спортивный седан, задний привод, продан"}
        ]
        
        for car_data in cars_data:
            car, created = Cars.get_or_create(
                vin=car_data["vin"],
                defaults=car_data
            )
            
            if created:
                print(f"   ✅ Автомобиль {car_data['stamp_id'].stamp} {car_data['model_car_id'].model_car} создан")
            else:
                print(f"   ℹ️  Автомобиль с VIN {car_data['vin']} уже существует")
        
        # 8. Проверка и добавление тестовых анкет (10+ записей)
        print("\n8. Проверка тестовых анкет...")
        
        # Получаем пользователей
        user1 = Users.get(Users.email == "user1@example.com")
        user2 = Users.get(Users.email == "user2@example.com")
        user3 = Users.get(Users.email == "user3@example.com")
        user4 = Users.get(Users.email == "user4@example.com")
        user5 = Users.get(Users.email == "user5@example.com")
        
        anketa_data = [
            {"user_id": user1, "stamp": "Toyota", "model_car": "Camry", "run": 65000, "price": 800000, "vin": "JTDBR32E160123501", "description": "Требуется замена масла, в остальном хорошее состояние"},
            {"user_id": user2, "stamp": "Nissan", "model_car": "Altima", "run": 89000, "price": 950000, "vin": "1N4AL3AP6JC123502", "description": "Комфортный семейный автомобиль, регулярное ТО"},
            {"user_id": user3, "stamp": "Ford", "model_car": "Focus", "run": 72000, "price": 650000, "vin": "1FADP3F2XEL123503", "description": "Городской хетчбек, не бит, не крашен"},
            {"user_id": user4, "stamp": "Honda", "model_car": "Civic", "run": 45000, "price": 1100000, "vin": "2HGFA16507H123504", "description": "Экономичный, малый расход, полная история"},
            {"user_id": user5, "stamp": "BMW", "model_car": "3 Series", "run": 112000, "price": 1800000, "vin": "WBA8E9C58J8123505", "description": "Немецкая надежность, требует небольшого ремонта"},
            {"user_id": user1, "stamp": "Volkswagen", "model_car": "Golf", "run": 58000, "price": 850000, "vin": "3VW467ATXHM123506", "description": "Отличное состояние, один хозяин"},
            {"user_id": user2, "stamp": "Audi", "model_car": "A4", "run": 67000, "price": 1900000, "vin": "WAUFFAFLXFN123507", "description": "Премиум седан, полный привод"},
            {"user_id": user3, "stamp": "Mercedes-Benz", "model_car": "C-Class", "run": 49000, "price": 2200000, "vin": "WDDHF5EB7EA123508", "description": "Роскошный автомобиль, ухоженный"},
            {"user_id": user4, "stamp": "Hyundai", "model_car": "Elantra", "run": 31000, "price": 950000, "vin": "5NPDH4AE6FH123509", "description": "Современный дизайн, малый пробег"},
            {"user_id": user5, "stamp": "Kia", "model_car": "Rio", "run": 28000, "price": 750000, "vin": "KNAFU5A20E5123510", "description": "Экономичный, идеален для города"},
            {"user_id": user1, "stamp": "Mazda", "model_car": "CX-5", "run": 53000, "price": 1650000, "vin": "JM3KFBDL0H0123511", "description": "Кроссовер в отличном состоянии"}
        ]
        
        for anketa_item in anketa_data:
            anketa, created = Anketa.get_or_create(
                vin=anketa_item["vin"],
                defaults=anketa_item
            )
            
            if created:
                print(f"   ✅ Анкета для {anketa_item['stamp']} {anketa_item['model_car']} создана")
            else:
                print(f"   ℹ️  Анкета с VIN {anketa_item['vin']} уже существует")
        
        # 9. Создание тестовых покупок (5+ записей)
        print("\n9. Создание тестовых покупок...")
        
        # Получаем несколько автомобилей и пользователей для покупок
        sold_cars = Cars.select().where(Cars.status_id == sold_status).limit(5)
        buyers = Users.select().where(Users.email.contains('user')).limit(5)
        
        for i, (car, buyer) in enumerate(zip(sold_cars, buyers)):
            shopping, created = Shopping.get_or_create(
                car_id=car.id,
                buyer_id=buyer.id,
                defaults={
                    'price': car.price,
                    'date_buy': datetime.now() - timedelta(days=30+i*5)
                }
            )
            
            if created:
                print(f"   ✅ Покупка автомобиля {car.stamp_id.stamp} {car.model_car_id.model_car} пользователем {buyer.full_name}")
            else:
                print(f"   ℹ️  Покупка для автомобиля {car.id} уже существует")
        
        # 10. Создание тестовых продаж (5+ записей)
        print("\n10. Создание тестовых продаж...")
        
        admin = Users.get(Users.email == "limon@gmail.com")
        
        for i, car in enumerate(sold_cars):
            sale, created = Sales.get_or_create(
                car_id=car.id,
                buyer_id=admin.id,
                defaults={
                    'price': car.price - 100000,  # Продажа дешевле покупки
                    'date_sale': datetime.now() - timedelta(days=60+i*5)
                }
            )
            
            if created:
                print(f"   ✅ Продажа автомобиля {car.stamp_id.stamp} {car.model_car_id.model_car}")
            else:
                print(f"   ℹ️  Продажа для автомобиля {car.id} уже существует")
        
        print("\n🎉 Заполнение базы данных завершено успешно!")
        print("📊 Статистика созданных записей:")
        print(f"   👥 Пользователи: {Users.select().count()} записей")
        print(f"   🚗 Марки автомобилей: {Stamp.select().count()} записей") 
        print(f"   🚙 Модели автомобилей: {ModelCar.select().count()} записей")
        print(f"   🏎️  Автомобили: {Cars.select().count()} записей")
        print(f"   📝 Анкеты: {Anketa.select().count()} записей")
        print(f"   💰 Покупки: {Shopping.select().count()} записей")
        print(f"   💸 Продажи: {Sales.select().count()} записей")
        
    except Exception as e:
        print(f"\n❌ Ошибка при заполнении базы данных: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if not database_connection.is_closed():
            database_connection.close()

if __name__ == "__main__":
    seed_database()