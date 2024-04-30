import random
import math

# алгоритм Евклида для НОД
def gcd(a: int, b: int) -> int:
    while b != 0:
        a,b = b, a%b
    return a

# расширенный алгоритм Евклида для вычисления закрытой экспоненты, функция возвращает мультипликативно обратное число к числу e по модулю φ(n)
def ext_gcd(a: int, b: int) -> int:
    fieil = a
    div = []  # сохраняются целые части от деления a/b

    while(b>0):
        div.append(a//b)
        t = b
        b = a%b
        a = t

    # s и d - столбцы из таблицы, показанной на практике
    s = [0 for i in range(len(div))]
    d = [0 for i in range(len(div))]
    s[len(div) - 1] = 0
    d[len(div) - 1] = 1

    # в этих столбцах заполнены только последние значения
    # поиск остальных элементов осуществляется через цикл
    for i in range(len(div) - 2, -1, -1):
        s[i] = d[i+1]
        d[i] = s[i+1]-d[i+1]*div[i]
    
    # первый элемент в массиве d - искомая закрытая экспонента
    # однако если это значение меньше нуля, то добавляем к нему значение ф-ии эйлера
    if d[0] > 0:
        return d[0]
    else:
        return d[0] + fieil

      
# тест Миллера-Рабина на простоту чисел, вовзращает булево значение, указывающее проходит число тест Миллера Рабина или нет
def miller_rabin(n):
    if n == 2:
        return True
    if n < 2 or n % 2 == 0:
        return False
    d = n - 1 # станет нечетным числом в разложении n-1=2^i*d
    i = 0   #cтепень двойки в разложении ...
    while(d % 2 == 0):
        d = d // 2
        i =i + 1
    r=2*math.log2(n) #кол-во шагов(проверок)
    
    a = 1
    for j in range (math.ceil(r)):
        a += 1
        x0 = modular_exp(a, d, n)
        
        #если условие выполняется, то a-свидетель простоты => генерация нового а
        if (x0 == 1 or x0 == n - 1):
            continue
        
        #поиск n-1 в последовательности {x1, x2,...xi}, если найдено, то а-свидетель простоты, иначе n-составное
        for k in range (i):
             x0 = modular_exp(x0, 2, n)
             if (x0 == 1):
                 return False #число составное
             if (x0 == n - 1):
                 break #переход на следующую итерацию внешнего цикла
        if (x0 != n - 1):
            return False 
    return True   #вероятно число простое
            
# алгоритм быстрого возведения в степень
def modular_exp(a:int, d: int, n: int) -> int:
    r = []  #в r представляеся число d в двоичной сс
    while (d > 0):
        r.append(d % 2)
        d = d // 2
    r.reverse()  
    c=[]     #заполнение массива по формуле c_i+1={if d_i+1==0 c_i^2 mod n, if d_i+1==1 c_i^2*a mod n}
    c.append(a)
    for i in range(1, len(r)):
        if r[i] == 0:
            c.append(c[i - 1]**2 % n)
        else:
            c.append(c[i - 1]**2*a % n)
    return c[len(r) - 1]   #последний элемент и есть искомое число, возведенное в степень по модулю
 
# функция возвращает простое число указанного размера бит
def generate_prime_numbers(bit_size: int) -> int:
    while True:
        number = random.getrandbits(bit_size)
        if not miller_rabin(number):
            continue
        else:
            return number

# функция нахождения взаимно простого числа
def find_coprime_number(number: int) -> int:
    bit_size = len(bin(number)[2:]) // 3
    start_number = random.getrandbits(bit_size)
    for i in range(start_number, number):
        if gcd(number, i) == 1:
            return i

