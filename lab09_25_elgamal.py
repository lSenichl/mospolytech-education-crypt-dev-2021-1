# импорт компонентов, необходимых для работы программы
from math import gcd
import random
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted

# объявление алфавита
alphavit = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4,
            'е': 5, 'ё': 6, 'ж': 7, 'з': 8, 'и': 9, 'й': 10,
            'к': 11, 'л': 12, 'м': 13, 'н': 14, 'о': 15,
            'п': 16, 'р': 17, 'с': 18, 'т': 19, 'у': 20,
            'ф': 21, 'х': 22, 'ц': 23, 'ч': 24, 'ш': 25,
            'щ': 26, 'ъ': 27, 'ы': 28, 'ь': 29, 'э': 30,
            'ю': 31, 'я': 32
            }

# функция проверки числа на простоту
def IsPrime(n):
    d = 2
    while n % d != 0:
        d += 1
    return d == n

# функция получения обратного числа
def modInverse(e, el):
    e = e % el
    for x in range(1, el):
        if ((e * x) % el == 1):
            return x
    return 1

# функция проверки числа на простоту с заданным числом попыток
def is_prime(num, test_count):
    if num == 1:
        return False
    if test_count >= num:
        test_count = num - 1
    for x in range(test_count):
        val = random.randint(1, num - 1)
        if pow(val, num-1, num) != 1:
            return False
    return True

# функция генерации простого числа
def gen_prime(n):
    found_prime = False
    while not found_prime:
        p = random.randint(2**(n-1), 2**n)
        if is_prime(p, 1000):
            return p

# функция хэширования
def hash_value(mod, alpha_code_msg):
    i = 0
    hashing_value = 1
    while i < len(alpha_code_msg):
        hashing_value = (((hashing_value-1) + int(alpha_code_msg[i]))**2) % mod
        i += 1
    return hashing_value

# функция вычисления подписи
def egcipher(clearText):
    p = gen_prime(10)
    print("P =", p)
    g = random.randint(2, p-1)
    print("G =", g)

    x = random.randint(2, p-2)
    y = (g**x) % p
    print("Открытый ключ(Y)={}, Секретный ключ(X)={}".format(y, x))

    msg = clearText
    msg_list = list(msg)
    alpha_code_msg = list()
    for i in range(len(msg_list)):
        alpha_code_msg.append(int(alphavit.get(msg_list[i])))
    print("Длина исходного сообщения {} символов".format(len(alpha_code_msg)))

    hash_code_msg = hash_value(p, alpha_code_msg)
    print("Хэш сообщения:= {}".format(hash_code_msg))

    k = 1
    while True:
        k = random.randint(1, p-2)
        if gcd(k, p-1) == 1:
            print("K =", k)
            break

    a = (g**k) % p

    b = (hash_code_msg - (x*a)) % (p-1)
    print("Значение подписи:S={},{}".format(a, b))
    b = modInverse(k, p-1) * ((hash_code_msg - (x * a)) % (p-1))

    check_hash_value = hash_value(p, alpha_code_msg)
    a_1 = ((y**a) * (a**b)) % p
    print("A1={}".format(a_1))
    a_2 = (g**check_hash_value) % p
    print("A2={}".format(a_2))
    if a_1 == a_2:
        print("Подпись верна\n")
    else:
        print("Подпись неверна")

#вывод результатов работы программы
def main():
    print('ЭЦП Elgamal:')
    print('КОРОТКИЙ ТЕКСТ:')
    egcipher(input_for_cipher_short())
    print('ДЛИННЫЙ ТЕКСТ:')
    egcipher(input_for_cipher_long())

if __name__ == "__main__":
    main()
    

