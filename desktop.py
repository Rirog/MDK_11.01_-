import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

API_BASE_URL = "http://localhost:8000"

class CarTradingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AvtoLimonchik")
        self.root.geometry("1920x1080")
        self.root.configure(bg='#355c7d')
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
            'primary': '#6c5b7b',
            'secondary': '#355c7d',
            'success': '#355c7d',
            'danger': '#e86375',
            'warning': '#ffd022',
            'light': "#f5e1d9",
            'dark': '#355c7d',
            'background': '#355c7d',
            'accent': '#355c7d'
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
                      background=[('active', '#6c5b7b'),
                                 ('pressed', '#355c7d')])
        self.style.map('Secondary.TButton',
                      background=[('active', '#6c5b7b'),
                                 ('pressed', '#355c7d')])
        self.style.map('Success.TButton',
                      background=[('active', '#6c5b7b'),
                                 ('pressed', '#355c7d')])
        self.style.map('Danger.TButton',
                      background=[('active', '#6c5b7b'),
                                 ('pressed', '#355c7d')])
    
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
        main_frame.pack(expand=True)
        
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
        card.pack(expand=True, padx=20, pady=10)
        
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
        main_frame.pack(expand=True)
        
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
        card.pack(expand=True, padx=20, pady=10)
        
        form_frame = tk.Frame(card, bg=self.colors['light'])
        form_frame.pack(expand=True, pady=10)
        
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
        main_frame.pack(expand=True)
        
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
        card.pack(expand=True, padx=20, pady=10)
        
        form_container = tk.Frame(card, bg=self.colors['light'])
        form_container.pack(expand=True, pady=10)
        
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
                self.show_main_menu()  # Изменено на новый главное меню
            else:
                error_msg = response.json().get("detail", "Ошибка получения профиля")
                messagebox.showerror("Ошибка", error_msg)
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")


    def show_main_menu(self):
        """Показать главное меню"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Главное меню", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        sub_label = ttk.Label(header_frame, text="Добро пожаловать в AvtoLimonchik", 
                            font=('Arial', 12), foreground='#bdc3c7')
        sub_label.pack(pady=(0, 10))
        
        # Карточка с меню
        card = self.create_card_frame(main_frame)
        card.pack(expand=True, padx=20, pady=10)
        
        # Приветствие пользователя
        welcome_text = f"👋 Приветствуем, {self.current_user.get('name', 'Пользователь')}!"
        welcome_label = tk.Label(card, text=welcome_text,
                               bg=self.colors['light'], fg=self.colors['dark'],
                               font=('Arial', 14, 'bold'), anchor='w')
        welcome_label.pack(fill=tk.X, pady=(0, 20))
        
        # Контейнер для кнопок меню
        menu_frame = tk.Frame(card, bg=self.colors['light'])
        menu_frame.pack(expand=True, pady=10)
        
        # Список кнопок меню (можно расширять в будущем)
        menu_buttons = [
            ("👤 Управление профилем", self.show_profile_management, 'Accent.TButton'),
            ("🚗 Доступные автомобили", self.show_available_cars, 'Success.TButton'),
            ("📝 Мои анкеты", self.show_my_anketi, 'Secondary.TButton'),
            ("🛒 Мои покупки", self.show_my_purchases, 'Secondary.TButton'),
        ]
        
        # Создаем кнопки меню - теперь они центрированы и больше
        self.menu_buttons = {}
        for i, (text, command, style) in enumerate(menu_buttons):
            btn_frame = tk.Frame(menu_frame, bg=self.colors['light'])
            btn_frame.pack(fill=tk.X, pady=8)
            
            btn = ttk.Button(btn_frame, text=text, style=style, command=command, width=30)
            btn.pack(ipady=12, anchor='center')  # Увеличиваем внутренние отступы и центрируем
            self.menu_buttons[text] = btn
        
        # Разделитель
        separator = ttk.Separator(card, orient='horizontal')
        separator.pack(fill=tk.X, pady=20)
        
        # Кнопка выхода - также центрирована и больше
        logout_frame = tk.Frame(card, bg=self.colors['light'])
        logout_frame.pack(fill=tk.X, pady=10)
        
        logout_btn = ttk.Button(logout_frame, text="🚪 Выйти из системы", 
                              style='Danger.TButton', 
                              command=self.confirm_logout,
                              width=30)
        logout_btn.pack(ipady=12, anchor='center')
        
        # Нижний колонтитул
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(18, 10))
        
        footer_label = ttk.Label(footer_frame, text="© 2025 AvtoLimonchik. Все права защищены.", 
                               font=('Arial', 9), foreground='#95a5a6')
        footer_label.pack()

    def show_profile_management(self):
        """Показать управление профилем"""
        # Используем существующий метод показа профиля
        self.show_main_menu_old_style()

    def show_main_menu_old_style(self):
        """Старый стиль главного меню (профиль)"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Управление профилем", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        # Кнопка возврата в главное меню - центрирована и больше
        back_frame = tk.Frame(header_frame, bg=self.colors['background'])
        back_frame.pack(fill=tk.X, pady=(0, 10))
        
        back_btn = ttk.Button(back_frame, text="← Назад в главное меню",
                             style='Secondary.TButton',
                             command=self.show_main_menu,
                             width=25)
        back_btn.pack(ipady=8, anchor='center')
        
        # Карточка с профилем
        card = self.create_card_frame(main_frame)
        card.pack(expand=True, padx=20, pady=10)
        
        # Заголовок профиля
        profile_header = tk.Label(card, text="👤 Мой профиль", 
                                bg=self.colors['light'], fg=self.colors['dark'],
                                font=('Arial', 14, 'bold'), anchor='w')
        profile_header.pack(fill=tk.X, pady=(0, 15))
        
        # Информация о пользователе
        user_info_frame = tk.Frame(card, bg=self.colors['light'])
        user_info_frame.pack(fill=tk.X, pady=10)
        
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
        
        # Кнопки управления профилем - центрированы и больше
        profile_buttons = [
            ("✏️ Изменить профиль", self.show_edit_profile, 'Accent.TButton'),
            ("🔒 Сменить пароль", self.show_change_password, 'Secondary.TButton'),
            ("🗑️ Удалить аккаунт", self.confirm_delete_account, 'Danger.TButton')
        ]
        
        for text, command, style in profile_buttons:
            btn_frame = tk.Frame(profile_actions_frame, bg=self.colors['light'])
            btn_frame.pack(fill=tk.X, pady=6)
            
            btn = ttk.Button(btn_frame, text=text, style=style, command=command, width=25)
            btn.pack(ipady=8, anchor='center')
    

    def show_edit_profile(self):
        """Показать форму редактирования профиля"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True)
        
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
        card.pack(expand=True, padx=20, pady=10)
        
        form_frame = tk.Frame(card, bg=self.colors['light'])
        form_frame.pack(expand=True, pady=10)
        
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
        main_frame.pack(expand=True)
        
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
        card.pack(expand=True, padx=20, pady=10)
        
        form_frame = tk.Frame(card, bg=self.colors['light'])
        form_frame.pack(expand=True, pady=10)
        
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
    def show_available_cars(self):
        """Показать раздел доступных автомобилей"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Доступные автомобили", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        # Кнопка возврата в главное меню
        back_frame = tk.Frame(header_frame, bg=self.colors['background'])
        back_frame.pack(fill=tk.X, pady=(0, 10))
        
        back_btn = ttk.Button(back_frame, text="← Назад в главное меню",
                             style='Secondary.TButton',
                             command=self.show_main_menu,
                             width=25)
        back_btn.pack(ipady=8, anchor='center')
        
        # Карточка с автомобилями
        card = self.create_card_frame(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Заголовок раздела
        cars_header = tk.Label(card, text="🚗 Автомобили в продаже", 
                              bg=self.colors['light'], fg=self.colors['dark'],
                              font=('Arial', 14, 'bold'), anchor='w')
        cars_header.pack(fill=tk.X, pady=(0, 15))
        
        # Область для списка автомобилей
        cars_list_frame = tk.Frame(card, bg=self.colors['light'])
        cars_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Заголовок списка
        list_header = tk.Label(cars_list_frame, text="Доступные для покупки автомобили:",
                              bg=self.colors['light'], fg=self.colors['dark'],
                              font=('Arial', 12, 'bold'), anchor='w')
        list_header.pack(fill=tk.X, pady=(0, 10))
        
        # Получение и отображение автомобилей
        self.load_and_display_available_cars(cars_list_frame)

    def load_and_display_available_cars(self, parent_frame):
        """Загрузить и отобразить список доступных автомобилей со скроллбаром"""
        try:
            headers = {"token": self.auth_token}
            response = requests.get(f"{API_BASE_URL}/users/cars/available", headers=headers)
            
            if response.status_code == 200:
                cars = response.json()
                
                if not cars:
                    # Сообщение об отсутствии автомобилей
                    no_cars_label = tk.Label(parent_frame, 
                                           text="В настоящее время нет доступных автомобилей для покупки",
                                           bg=self.colors['light'], fg='#7f8c8d',
                                           font=('Arial', 11))
                    no_cars_label.pack(pady=20)
                    return
                
                # Создаем фрейм с канвасом и скроллбаром
                container = tk.Frame(parent_frame, bg=self.colors['light'])
                container.pack(fill=tk.BOTH, expand=True)
                
                # Создаем канвас и скроллбар
                canvas = tk.Canvas(container, bg=self.colors['light'], highlightthickness=0)
                scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Добавляем прокрутку колесиком мыши
                def _on_mousewheel(event):
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                
                canvas.bind("<MouseWheel>", _on_mousewheel)
                scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
                
                # Отображаем автомобили в виде сетки
                self.create_cars_grid(scrollable_frame, cars)
                
                # Упаковываем canvas и scrollbar
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
            else:
                error_msg = response.json().get("detail", "Ошибка загрузки автомобилей")
                messagebox.showerror("Ошибка", error_msg)
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")

    def create_cars_grid(self, parent, cars):
        """Создать сетку автомобилей 4xN"""
        columns = 4
        
        for i, car in enumerate(cars):
            row = i // columns
            col = i % columns
            
            # Создаем карточку автомобиля
            card_frame = self.create_car_card(car)
            card_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            
            # Настраиваем веса строк и колонок для равномерного распределения
            parent.grid_rowconfigure(row, weight=1)
            parent.grid_columnconfigure(col, weight=1)


    def create_car_card(self, parent, car):
        """Создать карточку для отображения автомобиля"""
        card_frame = tk.Frame(parent, bg='#ffffff', relief='solid', bd=1, padx=12, pady=12)
        card_frame.config(width=280, height=220)
        card_frame.pack_propagate(False)  # Запрещаем изменение размера
        
        # Основная информация об автомобиле
        info_frame = tk.Frame(card_frame, bg='#ffffff')
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Марка и модель (обрезаем если слишком длинные)
        stamp_model = f"{car.get('stamp', '')} {car.get('model', '')}"
        if len(stamp_model) > 25:
            stamp_model = stamp_model[:25] + "..."
            
        stamp_model_label = tk.Label(info_frame, 
                                    text=f"🚗 {stamp_model}",
                                    bg='#ffffff', fg=self.colors['dark'],
                                    font=('Arial', 11, 'bold'), anchor='w')
        stamp_model_label.pack(fill=tk.X, pady=(0, 5))
        
        # Детали
        details = [
            f"📏 Пробег: {car.get('run_km', 0):,} км".replace(",", " "),
            f"💰 Стоимость: {car.get('price', 0):,} руб".replace(",", " "),
            f"🔢 VIN: {car.get('vin', '')[:12]}..." if len(car.get('vin', '')) > 12 else f"🔢 VIN: {car.get('vin', '')}"
        ]
        
        for detail in details:
            detail_label = tk.Label(info_frame, text=detail,
                                   bg='#ffffff', fg='#2c3e50',
                                   font=('Arial', 9), anchor='w')
            detail_label.pack(fill=tk.X, pady=1)
        
        # Кнопки действий
        actions_frame = tk.Frame(card_frame, bg='#ffffff')
        actions_frame.pack(fill=tk.X, pady=(8, 0))
        
        # Кнопка подробнее
        details_btn = ttk.Button(actions_frame, text="ℹ️ Подробнее",
                                style='Secondary.TButton',
                                command=lambda c=car: self.show_car_details(c),
                                width=12)
        details_btn.pack(side=tk.LEFT, padx=(0, 5), ipady=3, expand=True, fill=tk.X)
        
        # Кнопка покупки
        buy_btn = ttk.Button(actions_frame, text="🛒 Купить",
                            style='Success.TButton',
                            command=lambda c=car: self.confirm_purchase_car(c),
                            width=12)
        buy_btn.pack(side=tk.LEFT, ipady=3, expand=True, fill=tk.X)
        
        return card_frame

    def create_cars_grid(self, parent, cars):
        """Создать сетку автомобилей 4xN"""
        columns = 4
        
        for i, car in enumerate(cars):
            row = i // columns
            col = i % columns
            
            # Создаем карточку автомобиля
            card_frame = self.create_car_card(parent, car)
            card_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            
            # Настраиваем веса строк и колонок для равномерного распределения
            parent.grid_rowconfigure(row, weight=1)
            parent.grid_columnconfigure(col, weight=1)


    def show_car_details(self, car):
        """Показать детальную информацию об автомобиле"""
        # Создаем новое окно с деталями
        details_window = tk.Toplevel(self.root)
        details_window.title("Детали автомобиля")
        details_window.geometry("500x400")
        details_window.configure(bg=self.colors['background'])
        details_window.resizable(False, False)
        
        # Центрируем окно
        details_window.transient(self.root)
        details_window.grab_set()
        
        # Заголовок
        header_frame = ttk.Frame(details_window, padding="10")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        header_label = ttk.Label(header_frame, text="Детали автомобиля", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        # Карточка с информацией
        card = self.create_card_frame(details_window)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Основная информация
        info_frame = tk.Frame(card, bg=self.colors['light'])
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        
        details = [
            ("🚗 Марка:", car.get('stamp', 'Не указана')),
            ("🚙 Модель:", car.get('model', 'Не указана')),
            ("📏 Пробег:", f"{car.get('run_km', 0):,} км".replace(",", " ")),
            ("💰 Цена:", f"{car.get('price', 0):,} руб".replace(",", " ")),
            ("🔢 VIN:", car.get('vin', 'Не указан')),
            ("📋 ID:", str(car.get('id', 'Не указан')))
        ]
        
        for label, value in details:
            field_frame = tk.Frame(info_frame, bg=self.colors['light'])
            field_frame.pack(fill=tk.X, pady=8)
            
            lbl = tk.Label(field_frame, text=label, bg=self.colors['light'], 
                         fg=self.colors['dark'], font=('Arial', 11, 'bold'),
                         width=10, anchor='w')
            lbl.pack(side=tk.LEFT)
            
            value_lbl = tk.Label(field_frame, text=value, bg=self.colors['light'], 
                               fg='#2c3e50', font=('Arial', 11),
                               anchor='w')
            value_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Разделитель
        separator = ttk.Separator(info_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=20)
        
        # Кнопка покупки
        buy_btn_frame = tk.Frame(info_frame, bg=self.colors['light'])
        buy_btn_frame.pack(fill=tk.X, pady=10)
        
        buy_btn = ttk.Button(buy_btn_frame, text="🛒 Купить этот автомобиль",
                            style='Success.TButton',
                            command=lambda: [details_window.destroy(), self.confirm_purchase_car(car)])
        buy_btn.pack(fill=tk.X, pady=6, ipady=8)
        
        # Кнопка закрытия
        close_btn = ttk.Button(buy_btn_frame, text="❌ Закрыть",
                              style='Secondary.TButton',
                              command=details_window.destroy)
        close_btn.pack(fill=tk.X, pady=6, ipady=6)

    def confirm_purchase_car(self, car):
        """Подтверждение покупки автомобиля"""
        result = messagebox.askyesno(
            "Подтверждение покупки", 
            f"Вы уверены, что хотите купить этот автомобиль?\n\n"
            f"Марка: {car.get('stamp', '')}\n"
            f"Модель: {car.get('model', '')}\n"
            f"Цена: {car.get('price', 0):,} руб\n"
            f"VIN: {car.get('vin', '')}",
            icon='question'
        )
        
        if result:
            self.perform_purchase_car(car['id'])

    def perform_purchase_car(self, car_id):
        """Выполнить покупку автомобиля"""
        try:
            headers = {"token": self.auth_token}
            response = requests.post(f"{API_BASE_URL}/users/cars/buy?car_id={car_id}", 
                                   headers=headers)
            
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Автомобиль успешно куплен!")
                # Обновляем список автомобилей
                self.show_available_cars()
            else:
                error_msg = response.json().get("detail", "Ошибка покупки автомобиля")
                messagebox.showerror("Ошибка", error_msg)
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")


    def show_my_anketi(self): 
        """Показать раздел моих анкет"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Мои анкеты", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        # Кнопка возврата в главное меню
        back_frame = tk.Frame(header_frame, bg=self.colors['background'])
        back_frame.pack(fill=tk.X, pady=(0, 10))
        
        back_btn = ttk.Button(back_frame, text="← Назад в главное меню",
                             style='Secondary.TButton',
                             command=self.show_main_menu,
                             width=25)
        back_btn.pack(ipady=8, anchor='center')
        
        # Карточка с анкетами
        card = self.create_card_frame(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Заголовок раздела
        anketa_header = tk.Label(card, text="📝 Управление анкетами", 
                                bg=self.colors['light'], fg=self.colors['dark'],
                                font=('Arial', 14, 'bold'), anchor='w')
        anketa_header.pack(fill=tk.X, pady=(0, 15))
        
        # Кнопка создания новой анкеты
        create_btn_frame = tk.Frame(card, bg=self.colors['light'])
        create_btn_frame.pack(fill=tk.X, pady=10)
        
        create_btn = ttk.Button(create_btn_frame, text="➕ Создать новую анкету",
                               style='Success.TButton',
                               command=self.show_create_anketa_form,
                               width=30)
        create_btn.pack(ipady=10, anchor='center')
        
        # Разделитель
        separator = ttk.Separator(card, orient='horizontal')
        separator.pack(fill=tk.X, pady=20)
        
        # Область для списка анкет
        anketa_list_frame = tk.Frame(card, bg=self.colors['light'])
        anketa_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Заголовок списка
        list_header = tk.Label(anketa_list_frame, text="Мои текущие анкеты:",
                              bg=self.colors['light'], fg=self.colors['dark'],
                              font=('Arial', 12, 'bold'), anchor='w')
        list_header.pack(fill=tk.X, pady=(0, 10))
        
        # Получение и отображение анкет
        self.load_and_display_anketi(anketa_list_frame)


    def load_and_display_anketi(self, parent_frame):
        """Загрузить и отобразить список анкет со скроллбаром"""
        try:
            headers = {"token": self.auth_token}
            response = requests.get(f"{API_BASE_URL}/users/anketi/", headers=headers)
            
            if response.status_code == 200:
                anketi = response.json()
                
                if not anketi or (isinstance(anketi, dict) and anketi.get("message") == "Анкеты отсутствуют"):
                    # Сообщение об отсутствии анкет
                    no_anketi_label = tk.Label(parent_frame, 
                                              text="У вас пока нет созданных анкет",
                                              bg=self.colors['light'], fg='#7f8c8d',
                                              font=('Arial', 11))
                    no_anketi_label.pack(pady=20)
                    return
                
                # Создаем фрейм с канвасом и скроллбаром
                container = tk.Frame(parent_frame, bg=self.colors['light'])
                container.pack(fill=tk.BOTH, expand=True)
                
                # Создаем канвас и скроллбар
                canvas = tk.Canvas(container, bg=self.colors['light'], highlightthickness=0)
                scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Добавляем прокрутку колесиком мыши
                def _on_mousewheel(event):
                    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                
                canvas.bind("<MouseWheel>", _on_mousewheel)
                scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
                
                # Отображаем анкеты в виде сетки
                self.create_anketa_grid(scrollable_frame, anketi)
                
                # Упаковываем canvas и scrollbar
                canvas.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")
                
            else:
                error_msg = response.json().get("detail", "Ошибка загрузки анкет")
                messagebox.showerror("Ошибка", error_msg)
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")

    def create_anketa_card(self, parent, anketa):
        """Создать карточку для отображения анкеты"""
        card_frame = tk.Frame(parent, bg='#ffffff', relief='solid', bd=1, padx=12, pady=12)
        card_frame.config(width=280, height=200)
        card_frame.pack_propagate(False)  # Запрещаем изменение размера
        
        # Основная информация об анкете
        info_frame = tk.Frame(card_frame, bg='#ffffff')
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Марка и модель (обрезаем если слишком длинные)
        stamp_model = f"{anketa.get('stamp', '')} {anketa.get('model_car', '')}"
        if len(stamp_model) > 25:
            stamp_model = stamp_model[:25] + "..."
            
        stamp_model_label = tk.Label(info_frame, 
                                    text=f"🚗 {stamp_model}",
                                    bg='#ffffff', fg=self.colors['dark'],
                                    font=('Arial', 11, 'bold'), anchor='w')
        stamp_model_label.pack(fill=tk.X, pady=(0, 5))
        
        # Детали
        vin = anketa.get('vin', '')
        display_vin = f"🔢 {vin[:12]}..." if len(vin) > 12 else f"🔢 {vin}"
        
        details = [
            f"📏 Пробег: {anketa.get('run', 0):,} км".replace(",", " "),
            f"💰 Стоимость: {anketa.get('price', 0):,} руб".replace(",", " "),
            display_vin
        ]
        
        for detail in details:
            detail_label = tk.Label(info_frame, text=detail,
                                   bg='#ffffff', fg='#2c3e50',
                                   font=('Arial', 9), anchor='w')
            detail_label.pack(fill=tk.X, pady=1)
        
        # Описание (если есть)
        description = anketa.get('description', '')
        if description:
            # Обрезаем длинное описание
            if len(description) > 60:
                description = description[:60] + "..."
            
            desc_label = tk.Label(info_frame, text=f"📄 {description}",
                                 bg='#ffffff', fg='#7f8c8d',
                                 font=('Arial', 8), anchor='w', justify=tk.LEFT, wraplength=240)
            desc_label.pack(fill=tk.X, pady=(5, 0))
        
        # Кнопки действий
        actions_frame = tk.Frame(card_frame, bg='#ffffff')
        actions_frame.pack(fill=tk.X, pady=(8, 0))
        
        # Кнопка редактирования
        edit_btn = ttk.Button(actions_frame, text="✏️ Изменить",
                             style='Secondary.TButton',
                             command=lambda a=anketa: self.show_edit_anketa_form(a),
                             width=8)
        edit_btn.pack(side=tk.LEFT, padx=(0, 5), ipady=3, expand=True, fill=tk.X)
        
        # Кнопка удаления
        delete_btn = ttk.Button(actions_frame, text="🗑️ Удалить",
                               style='Danger.TButton',
                               command=lambda a=anketa: self.confirm_delete_anketa(a),
                               width=8)
        delete_btn.pack(side=tk.LEFT, ipady=3, expand=True, fill=tk.X)
        
        return card_frame

    def create_anketa_grid(self, parent, anketi):
        columns = 4
        
        for i, anketa in enumerate(anketi):
            row = i // columns
            col = i % columns
            
            # Создаем карточку анкеты
            card_frame = self.create_anketa_card(parent, anketa)
            card_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            
            # Настраиваем веса строк и колонок для равномерного распределения
            parent.grid_rowconfigure(row, weight=1)
            parent.grid_columnconfigure(col, weight=1)

    def show_create_anketa_form(self):
        """Показать форму создания новой анкеты"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Создание новой анкеты", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        # Кнопка возврата
        back_frame = tk.Frame(header_frame, bg=self.colors['background'])
        back_frame.pack(fill=tk.X, pady=(0, 10))
        
        back_btn = ttk.Button(back_frame, text="← Назад к списку анкет",
                             style='Secondary.TButton',
                             command=self.show_my_anketi,
                             width=25)
        back_btn.pack(ipady=8, anchor='center')
        
        # Карточка с формой
        card = self.create_card_frame(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        form_frame = tk.Frame(card, bg=self.colors['light'])
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Поля формы
        fields = [
            ("Марка автомобиля", "create_stamp"),
            ("Модель автомобиля", "create_model_car"),
            ("Пробег (км)", "create_run"),
            ("Цена (руб)", "create_price"),
            ("VIN номер", "create_vin"),
            ("Описание (необязательно)", "create_description")
        ]
        
        self.create_anketa_entries = {}
        
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
            if field_name == "create_description":
                entry = tk.Text(field_container, font=('Arial', 11), height=4, wrap=tk.WORD)
                entry.pack(fill=tk.X, pady=2)
            else:
                entry = ttk.Entry(field_container, font=('Arial', 11))
                if "run" in field_name or "price" in field_name:
                    entry.config(validate="key", validatecommand=(self.root.register(self.validate_number), '%P'))
                entry.pack(fill=tk.X, pady=2, ipady=6)
            
            self.create_anketa_entries[field_name] = entry
        
        # Контейнер для кнопок
        btn_frame = tk.Frame(card, bg=self.colors['light'])
        btn_frame.pack(fill=tk.X, pady=(20, 10))
        
        # Кнопка сохранения
        save_btn = ttk.Button(btn_frame, text="💾 Создать анкету", 
                             style='Success.TButton', 
                             command=self.perform_create_anketa)
        save_btn.pack(fill=tk.X, pady=6, ipady=8)
        
        # Кнопка отмены
        cancel_btn = ttk.Button(btn_frame, text="❌ Отмена", 
                              style='Secondary.TButton', 
                              command=self.show_my_anketi)
        cancel_btn.pack(fill=tk.X, pady=6, ipady=6)

    def show_edit_anketa_form(self, anketa):
        """Показать форму редактирования анкеты"""
        self.clear_window()
        self.current_editing_anketa = anketa
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_label = ttk.Label(header_frame, text="Редактирование анкеты", 
                               style='Header.TLabel')
        header_label.pack(pady=(10, 5))
        
        # Кнопка возврата
        back_frame = tk.Frame(header_frame, bg=self.colors['background'])
        back_frame.pack(fill=tk.X, pady=(0, 10))
        
        back_btn = ttk.Button(back_frame, text="← Назад к списку анкет",
                             style='Secondary.TButton',
                             command=self.show_my_anketi,
                             width=25)
        back_btn.pack(ipady=8, anchor='center')
        
        # Карточка с формой
        card = self.create_card_frame(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        form_frame = tk.Frame(card, bg=self.colors['light'])
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Поля формы с текущими значениями
        fields = [
            ("Марка автомобиля", "edit_stamp", anketa.get('stamp', '')),
            ("Модель автомобиля", "edit_model_car", anketa.get('model_car', '')),
            ("Пробег (км)", "edit_run", str(anketa.get('run', 0))),
            ("Цена (руб)", "edit_price", str(anketa.get('price', 0))),
            ("VIN номер", "edit_vin", anketa.get('vin', '')),
            ("Описание (необязательно)", "edit_description", anketa.get('description', ''))
        ]
        
        self.edit_anketa_entries = {}
        
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
            if field_name == "edit_description":
                entry = tk.Text(field_container, font=('Arial', 11), height=4, wrap=tk.WORD)
                entry.insert('1.0', current_value)
                entry.pack(fill=tk.X, pady=2)
            else:
                entry = ttk.Entry(field_container, font=('Arial', 11))
                entry.insert(0, current_value)
                if "run" in field_name or "price" in field_name:
                    entry.config(validate="key", validatecommand=(self.root.register(self.validate_number), '%P'))
                entry.pack(fill=tk.X, pady=2, ipady=6)
            
            self.edit_anketa_entries[field_name] = entry
        
        # Контейнер для кнопок
        btn_frame = tk.Frame(card, bg=self.colors['light'])
        btn_frame.pack(fill=tk.X, pady=(20, 10))
        
        # Кнопка сохранения
        save_btn = ttk.Button(btn_frame, text="💾 Сохранить изменения", 
                             style='Success.TButton', 
                             command=self.perform_edit_anketa)
        save_btn.pack(fill=tk.X, pady=6, ipady=8)
        
        # Кнопка отмены
        cancel_btn = ttk.Button(btn_frame, text="❌ Отмена", 
                              style='Secondary.TButton', 
                              command=self.show_my_anketi)
        cancel_btn.pack(fill=tk.X, pady=6, ipady=6)

    def validate_number(self, value):
        """Валидация числовых полей"""
        if value == "":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False

    def perform_create_anketa(self):
        """Создать новую анкету"""
        try:
            data = {
                "stamp": self.get_entry_value("create_stamp"),
                "model_car": self.get_entry_value("create_model_car"),
                "run": int(self.get_entry_value("create_run")),
                "price": int(self.get_entry_value("create_price")),
                "vin": self.get_entry_value("create_vin"),
                "description": self.get_text_value("create_description")
            }
            
            # Проверка обязательных полей
            required_fields = ["stamp", "model_car", "run", "price", "vin"]
            for field in required_fields:
                if not data[field]:
                    messagebox.showerror("Ошибка", f"Заполните поле: {field}")
                    return
            
            headers = {"token": self.auth_token}
            response = requests.post(f"{API_BASE_URL}/users/anketa/create", json=data, headers=headers)
            
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Анкета успешно создана!")
                self.show_my_anketi()
            else:
                error_msg = response.json().get("detail", "Ошибка создания анкеты")
                messagebox.showerror("Ошибка", error_msg)
                
        except ValueError:
            messagebox.showerror("Ошибка", "Пробег и цена должны быть числами")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")

    def perform_edit_anketa(self):
        """Редактировать анкету"""
        try:
            data = {}
            
            # Собираем только измененные поля
            fields_mapping = {
                "edit_stamp": "stamp",
                "edit_model_car": "model_car", 
                "edit_run": "run",
                "edit_price": "price",
                "edit_vin": "vin",
                "edit_description": "description"
            }
            
            for entry_name, field_name in fields_mapping.items():
                if entry_name in ["edit_run", "edit_price"]:
                    value = self.get_entry_value(entry_name)
                    if value and value != str(self.current_editing_anketa.get(field_name, '')):
                        data[field_name] = int(value)
                elif entry_name == "edit_description":
                    value = self.get_text_value(entry_name)
                    if value != self.current_editing_anketa.get(field_name, ''):
                        data[field_name] = value
                else:
                    value = self.get_entry_value(entry_name)
                    if value != self.current_editing_anketa.get(field_name, ''):
                        data[field_name] = value
            
            if not data:
                messagebox.showinfo("Информация", "Нет изменений для сохранения")
                return
            
            headers = {"token": self.auth_token}
            anketa_id = self.current_editing_anketa['id']
            response = requests.put(f"{API_BASE_URL}/users/anketa/update?anketa_id={anketa_id}", 
                                  json=data, headers=headers)
            
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Анкета успешно обновлена!")
                self.show_my_anketi()
            else:
                error_msg = response.json().get("detail", "Ошибка обновления анкеты")
                messagebox.showerror("Ошибка", error_msg)
                
        except ValueError:
            messagebox.showerror("Ошибка", "Пробег и цена должны быть числами")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")

    def confirm_delete_anketa(self, anketa):
        """Подтверждение удаления анкеты"""
        result = messagebox.askyesno(
            "Подтверждение удаления", 
            f"Вы уверены, что хотите удалить анкету?\n\n"
            f"Марка: {anketa.get('stamp', '')}\n"
            f"Модель: {anketa.get('model_car', '')}\n"
            f"VIN: {anketa.get('vin', '')}",
            icon='warning'
        )
        
        if result:
            self.perform_delete_anketa(anketa['id'])

    def perform_delete_anketa(self, anketa_id):
        """Удалить анкету"""
        try:
            headers = {"token": self.auth_token}
            response = requests.delete(f"{API_BASE_URL}/users/anketa/delete?anketa_id={anketa_id}", 
                                     headers=headers)
            
            if response.status_code == 200:
                messagebox.showinfo("Успех", "Анкета успешно удалена!")
                self.show_my_anketi()
            else:
                error_msg = response.json().get("detail", "Ошибка удаления анкеты")
                messagebox.showerror("Ошибка", error_msg)
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения: {str(e)}")

    def get_entry_value(self, entry_name):
        """Получить значение из Entry"""
        entry = self.create_anketa_entries.get(entry_name) or self.edit_anketa_entries.get(entry_name)
        if entry and hasattr(entry, 'get'):
            return entry.get().strip()
        return ""

    def get_text_value(self, text_name):
        """Получить значение из Text"""
        text_widget = self.create_anketa_entries.get(text_name) or self.edit_anketa_entries.get(text_name)
        if text_widget and hasattr(text_widget, 'get'):
            return text_widget.get('1.0', 'end-1c').strip()
        return ""

    def show_my_purchases(self):
        """Показать мои покупки"""
        messagebox.showinfo("В разработке", "Раздел 'Мои покупки' находится в разработке")

if __name__ == "__main__":
    root = tk.Tk()
    app = CarTradingApp(root)
    root.mainloop() 
