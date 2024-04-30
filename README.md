# Необходимые зависимости
```
pip install customtkinter
pip install packaging
pip install psycopg2
```
# Cryptography

## prime_numbers.py 


В этом файле находятся функции:

- generate_prime_numbers - генерирует простое число заданного кол-ва бит
- miller_rabin - реализует проверку числа на простоту по тесту Миллера Рабина (вызывается в generate_prime_numbers)
- find_coprime_number - находит взаимно простое число. Используется для нахождения **e**
- multiplicatively_inverse - находит мультипликативно обратное число. Используется для нахождения **d**
- egcd - расширенный алгоритм Евклида

## RSA.py

Класс Rsa
- представляет собой объект, в атрибутах которого хранятся сгенерированные параметры
- в конструкторе класса генерируются все параметры RSA
- пара (e, n) - открытый ключ
- пара (d, n) - закрытый ключ
- свойства property возвращают пары открытых, закрытых ключей и все сгенерированные параметры

# Frontend

## ui.py

Класс BaseUI

- интерфейс рисуется через customtkinter
- абстрактный класс от которого наследуются интерфейс сервера и клиента
- конструктор принимает название окна приложения
- в самом конструкторе задается название окна приложения, размеры окна и поля логина и пароля, куда они вводятся
  соответственно
- в методе draw_widgets уже рисуется текст и поля логина с паролем, задаются их стили (что-то похожее на css, если бы
  писали это через html)
- get_text - возвращает текст из нужного нам поля ввода текста
- insert_text - вставляет текст в нужное нам поле
- show_warning - принимает текст ошибки и выводит это окно с ошибкой
- show_info - принимает текст и выводит окно с информацией об успешной операции
- run_app - запускает наш customtkinter
![img.png](img.png)