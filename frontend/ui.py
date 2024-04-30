import os
import sys
sys.path.append(os.getcwd())

from abc import ABC, abstractmethod
import tkinter.messagebox as mb
import string
import random
import hashlib
import datetime
import json
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
 
from cryptography.RSA import Rsa
from database.db_utils import *
 
import customtkinter as ctk
from customtkinter import CTkButton, CTkLabel, CTkEntry, CTkTextbox, DISABLED, NORMAL, END
 
 
def randomword(length: int) -> str:
    """
    Функция возвращает рандомный набор символов длины length
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))
 
 
class BaseUI(ABC):
    with open('./configs/socket_config.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
 
    HOST = data["host"]
    PORT = data["port"]
    BUFSIZ = data["bifsiz"]
    ADDR = (HOST, PORT)
 
    def __init__(self, title=None):
        self.root = ctk.CTk()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.root.geometry("900x850")
        self.root.wm_title(title)
 
        self.login_text = CTkEntry(self.root, placeholder_text="Введите логин")
        self.password_text = CTkEntry(self.root, placeholder_text="Введите пароль")
 
    def draw_widgets(self):
        CTkLabel(self.root, text="Логин:", font=('Teja', 20)).grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.login_text.grid(row=0, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
 
        CTkLabel(self.root, text="Пароль:", font=('Teja', 20)).grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        self.password_text.grid(row=1, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
 
    def get_text_text(self, field_name: str) -> str:
        return getattr(self, field_name).get('1.0', END)
 
    def get_text_entry(self, field_name: str) -> str:
        return getattr(self, field_name).get()
 
    def insert_text(self, text: str, field_name: str) -> None:
        getattr(self, field_name).configure(state=NORMAL)
        getattr(self, field_name).delete('1.0', END)
        getattr(self, field_name).insert('1.0', text)
        getattr(self, field_name).configure(state=DISABLED)
 
    @staticmethod
    def show_warning(message: str) -> None:
        mb.showwarning("Ошибка", message)
 
    @staticmethod
    def show_info(message: str) -> None:
        mb.showinfo("Информация", message)
 
    @abstractmethod
    def send(self, mode: str, data=None):
        pass
 
    def run_app(self) -> None:
        self.draw_widgets()
 
 
class Server(BaseUI):
    def __init__(self, title='Сервер'):
        super().__init__(title)
 
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.bind(self.ADDR)
        self.ACCEPT_THREAD = None
        self.addresses = {}
        self.data = []
 
        self.rsa = None
 
        self.bit_length = CTkEntry(self.root, placeholder_text="Введите количество бит")
        self.p_text = CTkTextbox(self.root, state='disabled', width=400, height=75)
        self.q_text = CTkTextbox(self.root, state='disabled', width=400, height=75)
        self.n_text = CTkTextbox(self.root, state='disabled', width=400, height=75)
        self.phi_text = CTkTextbox(self.root, state='disabled', width=400, height=75)
        self.e_text = CTkTextbox(self.root, state='disabled', width=400, height=75)
        self.d_text = CTkTextbox(self.root, state='disabled', width=400, height=75)
 
    def draw_server_widgets(self) -> None:
        CTkLabel(self.root, text="Количество бит:", font=('Teja', 20)).grid(row=4, column=0, padx=20, pady=20,
                                                                            sticky="ew")
        self.bit_length.grid(row=4, column=1, columnspan=3, padx=20, pady=20, sticky="ew")
        CTkButton(self.root, text="Сгенерировать", command=lambda: self.generate_rsa_parameters()).grid(row=4,
                                                                                                        column=4,
                                                                                                        padx=20,
                                                                                                        pady=20)
 
        CTkLabel(self.root, text="p:", font=('Teja', 25)).grid(row=7, column=0, padx=20, pady=5, sticky="ew")
        self.p_text.grid(row=7, column=1, columnspan=3, padx=20, pady=5, sticky="ew")
 
        CTkLabel(self.root, text="q:", font=('Teja', 25)).grid(row=8, column=0, padx=20, pady=5, sticky="ew")
        self.q_text.grid(row=8, column=1, columnspan=3, padx=20, pady=5, sticky="ew")
 
        CTkLabel(self.root, text="n:", font=('Teja', 25)).grid(row=9, column=0, padx=20, pady=5, sticky="ew")
        self.n_text.grid(row=9, column=1, columnspan=3, padx=20, pady=5, sticky="ew")
 
        CTkLabel(self.root, text="φ(n):", font=('Teja', 25)).grid(row=10, column=0, padx=20, pady=5, sticky="ew")
        self.phi_text.grid(row=10, column=1, columnspan=3, padx=20, pady=5, sticky="ew")
 
        CTkLabel(self.root, text="e:", font=('Teja', 25)).grid(row=11, column=0, padx=20, pady=5, sticky="ew")
        self.e_text.grid(row=11, column=1, columnspan=3, padx=20, pady=5, sticky="ew")
 
        CTkLabel(self.root, text="d:", font=('Teja', 25)).grid(row=12, column=0, padx=20, pady=5, sticky="ew")
        self.d_text.grid(row=12, column=1, columnspan=3, padx=20, pady=5, sticky="ew")
 
        CTkButton(self.root, text="Записать", command=lambda: self.write_database()).grid(row=13, column=4, padx=20,
                                                                                          pady=5)
 
    def generate_rsa_parameters(self) -> None:
        try:
            bit_length_text = int(self.get_text_entry('bit_length'))
            if bit_length_text >= 8:
                self.rsa = Rsa(bit_length_text)
                fields = ('p_text', 'q_text', 'n_text', 'phi_text', 'e_text', 'd_text')
                for text, field in zip(self.rsa.all_parameters, fields):
                    self.insert_text(text, field)
            else:
                self.show_warning('Необходимо ввести число бит больше или равное 20')
        except ValueError:
            self.show_warning('В поле ввода количества бит необходимо ввести только числа')
 
    def write_database(self) -> None:
        if self.rsa is not None:
            login = self.get_text_entry('login_text').strip()
            password = self.get_text_entry('password_text').strip()
            if not login or not password:
                self.show_warning('Необходимо заполнить поля логина и пароля')
            else:
                if check_user_in_db(login):
                    self.show_warning('Пользователь с таким логином уже существует')
                else:
                    password = hashlib.sha1(password.strip().encode()).hexdigest()
                    id = insert_user_data(login, password)
                    insert_rsa_data(id, *self.rsa.all_parameters)
 
                    self.show_info('Данные успешно записаны в базу данных')
        else:
            self.show_warning('Необходимо сгенерировать параметры RSA')
 
    def create_socket_server(self) -> None:
        self.SERVER.listen(5)
        print("ожидание соединения")
        self.ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        self.ACCEPT_THREAD.start()
 
    def accept_incoming_connections(self) -> None:
        while True:
            client, client_address = self.SERVER.accept()
            print(f"{client_address[0]}:{client_address[1]} соединено")
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()
 
    def handle_client(self, client: socket) -> None:
        while True:
            msg = client.recv(self.BUFSIZ).decode('utf-8')
            print(msg)
            json_acceptable_string = msg.replace("'", "\"")
            data = json.loads(json_acceptable_string)
            if data['title'] == 'check_login':
                self.send(mode='login_answer', data=data['login'])
            if data['title'] == 'super_hash':
                login = data['login']
                h_client = data['h']
                password = return_password(login)
                w = hashlib.sha1(return_w(login).encode()).hexdigest()
                h_server = hashlib.sha1((password.strip() + w.strip()).encode()).hexdigest()
                check_time = get_time(login)
                if check_time >= datetime.datetime.now():
                    self.show_info('Ответ уложился по времени')
                    if h_server == h_client:
                        self.send(mode='superhash_answer', data=True)
                    else:
                        self.send(mode='superhash_answer', data=False)
                else:
                    self.show_warning('Ответ не уложился во время')
 
    def send(self, mode: str, data=None) -> None:
        if mode == 'login_answer':
            if check_user_in_db(data):
                w = randomword(10)
                insert_user_w(data, w)
                w_hash = hashlib.sha1(w.encode()).hexdigest()
                time_check = datetime.datetime.now() + datetime.timedelta(minutes=1)
                insert_user_time(data, time_check)
                data = json.dumps({'title': 'login_answer', 'result': True, 'w': w_hash})
            else:
                data = json.dumps({'title': 'login_answer', 'result': False})
        if mode == 'superhash_answer':
            if data:
                data = json.dumps({'title': 'superhash_answer', 'result': True})
            else:
                data = json.dumps({'title': 'superhash_answer', 'result': False})
        for clients in self.addresses:
            clients.send(bytes(data, encoding="utf-8"))
        time.sleep(0.2)
 
    def run_app(self) -> None:
        super().run_app()
        self.draw_server_widgets()
        self.create_socket_server()
        self.root.mainloop()
 
 
class Client(BaseUI):
    def __init__(self, title='Клиент'):
        super().__init__(title)
 
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.w_text = CTkTextbox(self.root, state='disabled', width=400, height=75)
 
    def draw_client_widgets(self) -> None:
        CTkButton(self.root, text="Отправить логин", command=lambda: self.send(mode='check_login')).grid(row=0,
                                                                                                         column=5,
                                                                                                         padx=20,
                                                                                                         pady=10)
        CTkLabel(self.root, text="w:", font=('Teja', 25)).grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        self.w_text.grid(row=4, column=1, columnspan=3, padx=20, pady=5, sticky="ew")
        CTkButton(self.root, text="Отправить супер хеш", command=lambda: self.send(mode='super_hash')).grid(row=5,
                                                                                                            column=5,
                                                                                                            padx=20,
                                                                                                            pady=10)
 
    def receive(self) -> None:
        while True:
            try:
                msg = self.client_socket.recv(1024).decode('utf-8')
                print(msg)
                json_acceptable_string = msg.replace("'", "\"")
                data = json.loads(json_acceptable_string)
                if data['title'] == 'login_answer':
                    if data['result']:
                        self.insert_text(data['w'], 'w_text')
                        self.show_info('Такой логин существует')
                    else:
                        self.show_warning('Такого логина не существует')
                        self.insert_text('', 'w_text')
                if data['title'] == 'superhash_answer':
                    if data['result']:
                        self.show_info('Супер хеши совпадают')
                    else:
                        self.show_warning('Супер хеши не совпадают')
            except OSError:
                break
 
    def send(self, mode: str, data=None) -> None:
        if mode == 'check_login':
            login = self.get_text_entry('login_text')
            if login:
                data = json.dumps({'title': 'check_login', 'login': login})
                self.client_socket.send(bytes(data, encoding="utf-8"))
                time.sleep(0.2)
            else:
                self.show_warning('Необходимо ввести логин')
        if mode == 'super_hash':
            password = self.get_text_entry('password_text')
            w = self.get_text_text('w_text')
            if not password:
                self.show_warning('Необходимо ввести пароль')
            elif not w:
                self.show_warning('Необходимо получить w')
            else:
                login = self.get_text_entry('login_text')
                password = hashlib.sha1(password.strip().encode()).hexdigest()
                password_w = password + w.strip()
                h = hashlib.sha1(password_w.encode()).hexdigest()
                data = json.dumps({'title': 'super_hash', 'login': login, 'h': h})
                self.client_socket.send(bytes(data, encoding="utf-8"))
                time.sleep(0.2)
 
    def run_app(self) -> None:
        super().run_app()
        self.draw_client_widgets()
        receive_thread = Thread(target=self.receive)
        receive_thread.start()
        self.root.mainloop()
