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
        
        self.style.map('Accent.TButton', 
                      background=[('active', '#d35400'),
                                 ('pressed', '#ba4a00')])
        self.style.map('Secondary.TButton',
                      background=[('active', '#2c3e50'),
                                 ('pressed', '#1a252f')])
        self.style.map('Success.TButton',
                      background=[('active', '#27ae60'),
                                 ('pressed', '#219955')])
    
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
                self.show_main_menu()
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




    def show_main_menu(self):
        """Показать главное меню - УЛУЧШЕННАЯ ВЕРСИЯ"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        car_icon = tk.Label(header_frame, text="🚗", font=('Arial', 30), 
                           bg=self.colors['background'], fg=self.colors['light'])
        car_icon.pack(pady=(0, 5))
        
        header_label = ttk.Label(header_frame, text="AvtoLimonchik", 
                               style='Header.TLabel')
        header_label.pack(pady=(0, 5))
        
        sub_label = ttk.Label(header_frame, text="Главное меню", 
                            font=('Arial', 12), foreground='#bdc3c7')
        sub_label.pack(pady=(0, 10))
        
        # Карточка с меню
        card = self.create_card_frame(main_frame)
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        welcome_label = tk.Label(card, text="Добро пожаловать в личный кабинет!", 
                               bg=self.colors['light'], fg=self.colors['dark'],
                               font=('Arial', 14, 'bold'))
        welcome_label.pack(pady=20)
        
        # Кнопки меню
        menu_buttons = [
            ("Мои анкеты", self.show_anketi),
            ("Доступные автомобили", self.show_cars),
            ("Мои покупки", self.show_purchases),
            ("Профиль", self.show_profile)
        ]
        
        for text, command in menu_buttons:
            btn = ttk.Button(card, text=text, style='Secondary.TButton',
                           command=command)
            btn.pack(fill=tk.X, pady=8, ipady=8)
        
        # Кнопка выхода
        logout_btn = ttk.Button(card, text="Выйти из системы", 
                               style='Accent.TButton', command=self.logout)
        logout_btn.pack(fill=tk.X, pady=(20, 10), ipady=8)
    
    def show_anketi(self):
        messagebox.showinfo("Инфо", "Функционал в разработке")
    
    def show_cars(self):
        messagebox.showinfo("Инфо", "Функционал в разработке")
    
    def show_purchases(self):
        messagebox.showinfo("Инфо", "Функционал в разработке")
    
    def show_profile(self):
        messagebox.showinfo("Инфо", "Функционал в разработке")

    def logout(self):
        """Выход из системы"""
        if self.auth_token:
            try:
                requests.post(f"{API_BASE_URL}/users/logout/", 
                             headers={"token": self.auth_token})
            except:
                pass
        self.auth_token = None
        self.show_auth_frame()

if __name__ == "__main__":
    root = tk.Tk()
    app = CarTradingApp(root)
    root.mainloop()
