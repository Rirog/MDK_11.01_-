import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

API_BASE_URL = "http://localhost:8000"

class CarTradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AvtoLimonchik")
        self.root.geometry("500x700")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Центрирование окна на экране
        self.center_window()
        
        self.auth_token = None
        self.current_user = None
        
        self.setup_styles()
        self.show_auth_frame()
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    def setup_styles(self):
        """Настройка стилей приложения"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2c3e50',
            'success': '#2ecc71',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#34495e',
            'background': '#2c3e50',
            'accent': '#e67e22'
        }
        
        self.style.configure('TFrame', background=self.colors['background'])
        self.style.configure('TLabel', background=self.colors['background'], 
                           foreground=self.colors['light'], font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'))
        self.style.configure('Header.TLabel', font=('Arial', 20, 'bold'), 
                           foreground=self.colors['light'])
        self.style.configure('Accent.TButton', background=self.colors['accent'],
                           foreground='white', focuscolor='none')
        self.style.configure('Secondary.TButton', background=self.colors['dark'],
                           foreground=self.colors['light'], focuscolor='none')
        self.style.configure('Success.TButton', background=self.colors['success'],
                           foreground='white', focuscolor='none')
        self.style.configure('Danger.TButton', background=self.colors['danger'],
                           foreground='white', focuscolor='none')
        
        self.style.map('Accent.TButton', 
                      background=[('active', '#d35400'),
                                 ('pressed', '#ba4a00')])
        self.style.map('Secondary.TButton',
                      background=[('active', '#2c3e50'),
                                 ('pressed', '#1a252f')])
        self.style.map('Success.TButton',
                      background=[('active', '#27ae60'),
                                 ('pressed', '#219955')])
        self.style.map('Danger.TButton',
                      background=[('active', '#c0392b'),
                                 ('pressed', '#a93226')])
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_card_frame(self, parent):
        """Создать карточку для контента"""
        card = tk.Frame(parent, bg=self.colors['light'], relief='raised', 
                       bd=1, padx=20, pady=20)
        return card
    
    def show_auth_frame(self):
        """Показать фрейм авторизации"""
        self.clear_window()
        
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Верхняя часть с логотипом и заголовком
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(10, 20))
        
        # Иконка автомобиля как эмодзи
        car_icon = tk.Label(header_frame, text="🚗", font=('Arial', 40), 
                           bg=self.colors['background'], fg=self.colors['light'])
        car_icon.pack(pady=(0, 10))
        
        # Основной заголовок
        header_label = ttk.Label(header_frame, text="AvtoLimonchik", 
                               style='Header.TLabel')
        header_label.pack(pady=(0, 5))
        
        # Подзаголовок
        sub_label = ttk.Label(header_frame, text="Платформа для покупки и продажи автомобилей", 
                            font=('Arial', 12), foreground='#bdc3c7')
        sub_label.pack(pady=(0, 10))
        
        # Разделитель
        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # Карточка с приветствием
        card = self.create_card_frame(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Приветственный текст
        welcome_text = (
            "Добро пожаловать в AvtoLimonchik!\n\n"
            "Здесь вы можете:\n"
            "• Продать свой автомобиль\n" 
            "• Купить автомобиль у фирмы\n"
            "• Просматривать доступные автомобили\n\n"
            "Выберите действие для продолжения:"
        )
        
        welcome_label = tk.Label(card, text=welcome_text, 
                               bg=self.colors['light'], fg=self.colors['dark'],
                               font=('Arial', 11), justify=tk.LEFT)
        welcome_label.pack(pady=20, anchor='w')
        
        # Контейнер для кнопок
        btn_frame = tk.Frame(card, bg=self.colors['light'])
        btn_frame.pack(fill=tk.X, pady=20)
        
        # Кнопка входа
        login_btn = ttk.Button(btn_frame, text="Вход в систему", 
                              style='Accent.TButton', 
                              command=self.show_login)
        login_btn.pack(fill=tk.X, pady=8, ipady=10)
        
        # Кнопка регистрации
        register_btn = ttk.Button(btn_frame, text="Создать аккаунт", 
                                 style='Success.TButton', 
                                 command=self.show_register)
        register_btn.pack(fill=tk.X, pady=8, ipady=10)
        
        # Нижний колонтитул
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(18, 10))
        
        footer_label = ttk.Label(footer_frame, text="© 2025 AvtoLimonchik. Все права защищены.", 
                               font=('Arial', 9), foreground='#95a5a6')
        footer_label.pack()
    
    def show_login(self):
        """Показать форму входа"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Вход в систему", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        sub_label = ttk.Label(header_frame, text="Введите ваши учетные данные", 
                            font=('Arial', 12), foreground='#bdc3c7')
        sub_label.pack(pady=(0, 10))
        
        # Карточка с формой
        card = self.create_card_frame(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        form_frame = tk.Frame(card, bg=self.colors['light'])
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Поля формы
        fields = [
            ("Электронная почта или телефон", "login_email_phone"),
            ("Пароль", "login_password")
        ]
        
        self.login_entries = {}
        
        for i, (label, field_name) in enumerate(fields):
            # Контейнер для поля
            field_container = tk.Frame(form_frame, bg=self.colors['light'])
            field_container.pack(fill=tk.X, pady=12)
            
            # Метка
            lbl = tk.Label(field_container, text=label, bg=self.colors['light'], 
                         fg=self.colors['dark'], font=('Arial', 10, 'bold'),
                         anchor='w')
            lbl.pack(fill=tk.X, pady=(0, 5))
            
            # Поле ввода
            entry = ttk.Entry(field_container, font=('Arial', 11))
            if "password" in field_name:
                entry.config(show="•")
            entry.pack(fill=tk.X, pady=2, ipady=6)
            self.login_entries[field_name] = entry
        
        # Контейнер для кнопок
        btn_frame = tk.Frame(card, bg=self.colors['light'])
        btn_frame.pack(fill=tk.X, pady=(10, 10))
        
        # Кнопка входа
        login_btn = ttk.Button(btn_frame, text="Войти", 
                              style='Accent.TButton', 
                              command=self.perform_login)
        login_btn.pack(fill=tk.X, pady=6, ipady=8)
        
        # Кнопка возврата
        back_btn = ttk.Button(btn_frame, text="Назад", 
                             style='Secondary.TButton', 
                             command=self.show_auth_frame)
        back_btn.pack(fill=tk.X, pady=6, ipady=6)
    
    def show_register(self):
        """Показать форму регистрации"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Регистрация", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        sub_label = ttk.Label(header_frame, text="Создайте новый аккаунт", 
                            font=('Arial', 12), foreground='#bdc3c7')
        sub_label.pack(pady=(0, 10))
        
        # Карточка с формой
        card = self.create_card_frame(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        form_container = tk.Frame(card, bg=self.colors['light'])
        form_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Поля формы
        fields = [
            ("Электронная почта", "register_email"),
            ("Телефон", "register_phone"), 
            ("Полное имя", "register_full_name"),
            ("Пароль", "register_password")
        ]

        self.register_entries = {}
        
        for i, (label, field_name) in enumerate(fields):
            # Контейнер для поля
            field_frame = tk.Frame(form_container, bg=self.colors['light'])
            field_frame.pack(fill=tk.X, pady=10)
            
            # Метка
            lbl = tk.Label(field_frame, text=label, 
                         bg=self.colors['light'], fg=self.colors['dark'],
                         font=('Arial', 10, 'bold'), anchor='w')
            lbl.pack(fill=tk.X, pady=(0, 5))
            
            # Поле ввода
            entry = ttk.Entry(field_frame, font=('Arial', 11))
            if "password" in field_name:
                entry.config(show="•")
            entry.pack(fill=tk.X, ipady=5)
            self.register_entries[field_name] = entry
        
        # Разделитель
        separator = ttk.Separator(form_container, orient='horizontal')
        separator.pack(fill=tk.X, pady=20)
        
        # Контейнер для кнопок
        btn_frame = tk.Frame(form_container, bg=self.colors['light'])
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Кнопка регистрации
        register_btn = ttk.Button(btn_frame, text="Зарегистрироваться", 
                                 style='Success.TButton', 
                                 command=self.perform_register)
        register_btn.pack(fill=tk.X, pady=4, ipady=5)
        
        # Кнопка возврата
        back_btn = ttk.Button(btn_frame, text="Назад", 
                             style='Secondary.TButton', 
                             command=self.show_auth_frame)
        back_btn.pack(fill=tk.X, pady=1, ipady=1)
        
        # Подсказка
        hint_label = tk.Label(form_container, 
                             text="После регистрации вы сможете войти в систему",
                             bg=self.colors['light'], fg='#7f8c8d',
                             font=('Arial', 9))
        hint_label.pack(pady=10)
    
    def perform_login(self):
        """Выполнить вход"""
        email_phone = self.login_entries["login_email_phone"].get().strip()
        password = self.login_entries["login_password"].get()
        
        if not email_phone or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        # Определяем, email это или телефон
        login_data = {"password": password}
        if "@" in email_phone:
            login_data["email"] = email_phone
        else:
            login_data["phone"] = email_phone
        
        try:
            response = requests.post(f"{API_BASE_URL}/users/auth/", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data["token"]
                messagebox.showinfo("Успех", "Вход выполнен успешно!")
                self.get_user_profile()
            else:
                error_msg = response.json().get("detail", "Ошибка авторизации")
                messagebox.showerror("Ошибка", error_msg)
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")
    
    def perform_register(self):
        """Выполнить регистрацию"""
        data = {
            "email": self.register_entries["register_email"].get().strip(),
            "phone": self.register_entries["register_phone"].get().strip(),
            "full_name": self.register_entries["register_full_name"].get().strip(),
            "password": self.register_entries["register_password"].get()
        }
        
        # Проверка заполненности полей
        for field, value in data.items():
            if not value:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return
        
        try:
            response = requests.post(f"{API_BASE_URL}/users/register/", json=data)
            
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Регистрация выполнена успешно!")
                # Очистка полей после успешной регистрации
                for entry in self.register_entries.values():
                    entry.delete(0, tk.END)
                self.show_login()
            else:
                error_msg = response.json().get("detail", "Ошибка регистрации")
                messagebox.showerror("Ошибка", error_msg)
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")

    def get_user_profile(self):
        """Получить профиль пользователя"""
        if not self.auth_token:
            messagebox.showerror("Ошибка", "Токен авторизации отсутствует")
            return
        
        try:
            headers = {"token": self.auth_token}
            response = requests.get(f"{API_BASE_URL}/users/me/", headers=headers)
            
            if response.status_code == 200:
                self.current_user = response.json()
                self.show_main_menu()
            else:
                error_msg = response.json().get("detail", "Ошибка получения профиля")
                messagebox.showerror("Ошибка", error_msg)
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")

    def show_main_menu(self):
        """Показать главное меню"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Главное меню", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        sub_label = ttk.Label(header_frame, text="Добро пожаловать в AvtoLimonchik", 
                            font=('Arial', 12), foreground='#bdc3c7')
        sub_label.pack(pady=(0, 10))
        
        # Карточка с профилем
        card = self.create_card_frame(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Заголовок профиля
        profile_header = tk.Label(card, text="👤 Мой профиль", 
                                bg=self.colors['light'], fg=self.colors['dark'],
                                font=('Arial', 14, 'bold'), anchor='w')
        profile_header.pack(fill=tk.X, pady=(0, 15))
        
        # Информация о пользователе
        user_info_frame = tk.Frame(card, bg=self.colors['light'])
        user_info_frame.pack(fill=tk.X, pady=10)
        
        # Отображаем информацию о пользователе
        user_fields = [
            ("Имя:", self.current_user.get('name', '')),
            ("Email:", self.current_user.get('email', '')),
            ("Телефон:", self.current_user.get('phone', ''))
        ]
        
        for label, value in user_fields:
            field_frame = tk.Frame(user_info_frame, bg=self.colors['light'])
            field_frame.pack(fill=tk.X, pady=8)
            
            lbl = tk.Label(field_frame, text=label, bg=self.colors['light'], 
                         fg=self.colors['dark'], font=('Arial', 10, 'bold'),
                         width=10, anchor='w')
            lbl.pack(side=tk.LEFT)
            
            value_lbl = tk.Label(field_frame, text=value, bg=self.colors['light'], 
                               fg='#2c3e50', font=('Arial', 10),
                               anchor='w')
            value_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Разделитель
        separator = ttk.Separator(card, orient='horizontal')
        separator.pack(fill=tk.X, pady=20)
        
        # Контейнер для кнопок управления профилем
        profile_actions_frame = tk.Frame(card, bg=self.colors['light'])
        profile_actions_frame.pack(fill=tk.X, pady=10)
        
        # Кнопка изменения профиля
        edit_profile_btn = ttk.Button(profile_actions_frame, text="✏️ Изменить профиль", 
                                     style='Accent.TButton', 
                                     command=self.show_edit_profile)
        edit_profile_btn.pack(fill=tk.X, pady=6, ipady=6)
        
        # Кнопка изменения пароля
        change_password_btn = ttk.Button(profile_actions_frame, text="🔒 Сменить пароль", 
                                       style='Secondary.TButton', 
                                       command=self.show_change_password)
        change_password_btn.pack(fill=tk.X, pady=6, ipady=6)
        
        # Кнопка удаления аккаунта (только для пользователей)
        delete_account_btn = ttk.Button(profile_actions_frame, text="🗑️ Удалить аккаунт", 
                                      style='Danger.TButton', 
                                      command=self.confirm_delete_account)
        delete_account_btn.pack(fill=tk.X, pady=6, ipady=6)
        
        # Разделитель
        separator2 = ttk.Separator(card, orient='horizontal')
        separator2.pack(fill=tk.X, pady=20)
        
        # Кнопка выхода
        logout_btn = ttk.Button(card, text="🚪 Выйти из системы", 
                              style='Secondary.TButton', 
                              command=self.confirm_logout)
        logout_btn.pack(fill=tk.X, pady=10, ipady=8)
        
        # Нижний колонтитул
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(18, 10))
        
        footer_label = ttk.Label(footer_frame, text="© 2025 AvtoLimonchik. Все права защищены.", 
                               font=('Arial', 9), foreground='#95a5a6')
        footer_label.pack()

    def show_edit_profile(self):
        """Показать форму редактирования профиля"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Редактирование профиля", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        sub_label = ttk.Label(header_frame, text="Измените данные вашего профиля", 
                            font=('Arial', 12), foreground='#bdc3c7')
        sub_label.pack(pady=(0, 10))
        
        # Карточка с формой
        card = self.create_card_frame(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        form_frame = tk.Frame(card, bg=self.colors['light'])
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Поля формы с текущими значениями
        fields = [
            ("Полное имя", "edit_full_name", self.current_user.get('name', '')),
            ("Телефон", "edit_phone", self.current_user.get('phone', ''))
        ]
        
        self.edit_entries = {}
        
        for i, (label, field_name, current_value) in enumerate(fields):
            # Контейнер для поля
            field_container = tk.Frame(form_frame, bg=self.colors['light'])
            field_container.pack(fill=tk.X, pady=12)
            
            # Метка
            lbl = tk.Label(field_container, text=label, bg=self.colors['light'], 
                         fg=self.colors['dark'], font=('Arial', 10, 'bold'),
                         anchor='w')
            lbl.pack(fill=tk.X, pady=(0, 5))
            
            # Поле ввода
            entry = ttk.Entry(field_container, font=('Arial', 11))
            entry.insert(0, current_value)
            entry.pack(fill=tk.X, pady=2, ipady=6)
            self.edit_entries[field_name] = entry
        
        # Контейнер для кнопок
        btn_frame = tk.Frame(card, bg=self.colors['light'])
        btn_frame.pack(fill=tk.X, pady=(20, 10))
        
        # Кнопка сохранения
        save_btn = ttk.Button(btn_frame, text="💾 Сохранить изменения", 
                             style='Success.TButton', 
                             command=self.perform_edit_profile)
        save_btn.pack(fill=tk.X, pady=6, ipady=8)
        
        # Кнопка отмены
        cancel_btn = ttk.Button(btn_frame, text="❌ Отмена", 
                              style='Secondary.TButton', 
                              command=self.show_main_menu)
        cancel_btn.pack(fill=tk.X, pady=6, ipady=6)

    def show_change_password(self):
        """Показать форму смены пароля"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Смена пароля", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        sub_label = ttk.Label(header_frame, text="Введите новый пароль", 
                            font=('Arial', 12), foreground='#bdc3c7')
        sub_label.pack(pady=(0, 10))
        
        # Карточка с формой
        card = self.create_card_frame(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        form_frame = tk.Frame(card, bg=self.colors['light'])
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Поля формы
        fields = [
            ("Новый пароль", "new_password"),
            ("Подтвердите пароль", "confirm_password")
        ]
        
        self.password_entries = {}
        
        for i, (label, field_name) in enumerate(fields):
            # Контейнер для поля
            field_container = tk.Frame(form_frame, bg=self.colors['light'])
            field_container.pack(fill=tk.X, pady=12)
            
            # Метка
            lbl = tk.Label(field_container, text=label, bg=self.colors['light'], 
                         fg=self.colors['dark'], font=('Arial', 10, 'bold'),
                         anchor='w')
            lbl.pack(fill=tk.X, pady=(0, 5))
            
            # Поле ввода
            entry = ttk.Entry(field_container, font=('Arial', 11), show="•")
            entry.pack(fill=tk.X, pady=2, ipady=6)
            self.password_entries[field_name] = entry
        
        # Контейнер для кнопок
        btn_frame = tk.Frame(card, bg=self.colors['light'])
        btn_frame.pack(fill=tk.X, pady=(20, 10))
        
        # Кнопка сохранения
        save_btn = ttk.Button(btn_frame, text="🔒 Сменить пароль", 
                             style='Success.TButton', 
                             command=self.perform_change_password)
        save_btn.pack(fill=tk.X, pady=6, ipady=8)
        
        # Кнопка отмены
        cancel_btn = ttk.Button(btn_frame, text="❌ Отмена", 
                              style='Secondary.TButton', 
                              command=self.show_main_menu)
        cancel_btn.pack(fill=tk.X, pady=6, ipady=6)

    def perform_edit_profile(self):
        """Выполнить обновление профиля"""
        full_name = self.edit_entries["edit_full_name"].get().strip()
        phone = self.edit_entries["edit_phone"].get().strip()
        
        if not full_name or not phone:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        try:
            headers = {"token": self.auth_token}
            data = {
                "full_name": full_name,
                "phone": phone
            }
            
            response = requests.put(f"{API_BASE_URL}/users/me/", json=data, headers=headers)
            
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Профиль успешно обновлен!")
                self.get_user_profile()  # Обновляем данные профиля
            else:
                error_msg = response.json().get("detail", "Ошибка обновления профиля")
                messagebox.showerror("Ошибка", error_msg)
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")

    def perform_change_password(self):
        """Выполнить смену пароля"""
        new_password = self.password_entries["new_password"].get()
        confirm_password = self.password_entries["confirm_password"].get()
        
        if not new_password or not confirm_password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        if new_password != confirm_password:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return
        
        try:
            headers = {"token": self.auth_token}
            # Исправлено: отправляем объект с полем password вместо просто строки
            data = {"password": new_password}
            
            response = requests.put(f"{API_BASE_URL}/users/me/password", json=data, headers=headers)
            
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Пароль успешно изменен!")
                self.show_main_menu()
            else:
                error_msg = response.json().get("detail", "Ошибка смены пароля")
                messagebox.showerror("Ошибка", error_msg)
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")

    def confirm_delete_account(self):
        """Подтверждение удаления аккаунта"""
        result = messagebox.askyesno(
            "Подтверждение удаления", 
            "Вы уверены, что хотите удалить свой аккаунт?\n\nЭто действие нельзя отменить!",
            icon='warning'
        )
        
        if result:
            self.perform_delete_account()

    def perform_delete_account(self):
        """Выполнить удаление аккаунта"""
        try:
            headers = {"token": self.auth_token}
            response = requests.delete(f"{API_BASE_URL}/users/delete_me/", headers=headers)
            
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Аккаунт успешно удален!")
                self.auth_token = None
                self.current_user = None
                self.show_auth_frame()
            else:
                error_msg = response.json().get("detail", "Ошибка удаления аккаунта")
                messagebox.showerror("Ошибка", error_msg)
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")

    def confirm_logout(self):
        """Подтверждение выхода из системы"""
        result = messagebox.askyesno(
            "Подтверждение выхода", 
            "Вы уверены, что хотите выйти из системы?",
            icon='question'
        )
        
        if result:
            self.perform_logout()

    def perform_logout(self):
        """Выполнить выход из системы"""
        try:
            headers = {"token": self.auth_token}
            response = requests.post(f"{API_BASE_URL}/users/logout/", headers=headers)
            
            # Выход выполняется в любом случае, даже если запрос не удался
            self.auth_token = None
            self.current_user = None
            self.show_auth_frame()
            
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Вы успешно вышли из системы!")
            else:
                # Не показываем ошибку, так как выход все равно выполнен локально
                pass
                
        except requests.exceptions.RequestException:
            # Выход выполняется локально даже при ошибке соединения
            self.auth_token = None
            self.current_user = None
            self.show_auth_frame()


if __name__ == "__main__":
    root = tk.Tk()
    app = CarTradingApp(root)
    root.mainloop()
