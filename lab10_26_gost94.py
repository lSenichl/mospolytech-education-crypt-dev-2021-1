# импорт компонентов, необходимых для работы программы
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

# функция вычисления подписи
def ciphergostd(clearText):
    array = []
    flag = False
    for s in range(50, 1000):
        for i in range(2, s):
            if s % i == 0:
                flag = True
                break
        if flag == False:
            array.append(s)
        flag = False
    p = 31
    print("p = ", p)
    q = 5
    print("q = ", q)
    a = 2
    print("a =", a)

    array2 = []
    flag2 = False
    for s in range(2, q):
        for i in range(2, s):
            if s % i == 0:
                flag2 = True
                break
        if flag2 == False:
            array2.append(s)
        flag2 = False

    x = 3
    print("x = ", x)
    y = a**x % p
    k = 4
    print("k = ", k)
    r = (a**k % p) % q

    msg = clearText
    msg_list = list(msg)
    alpha_code_msg = list()
    for i in range(len(msg_list)):
        alpha_code_msg.append(int(alphavit.get(msg_list[i])))
    print("Длина исходного сообщения {} символов".format(len(alpha_code_msg)))
    hash_code_msg = hash_value(p, alpha_code_msg)
    print("Хэш сообщения:= {}".format(hash_code_msg))

    s = (x*r+k*hash_code_msg) % q

    print("Цифровая подпись = ", r % (2**256), ",", s % (2**256))

    v = (hash_code_msg**(q-2)) % q
    z1 = s*v % q
    z2 = ((q-r)*v) % q
    u = (((a**z1)*(y**z2)) % p) % q
    print(r, " = ", u)
    if u == r:
        print("r = u, следовательно:")
        print("Подпись верна\n")
    else:
        print("Подпись неверна")

# функция хэширования
def hash_value(n, alpha_code):
    i = 0
    hash = 1
    while i < len(alpha_code):
        hash = (((hash-1) + int(alpha_code[i]))**2) % n
        i += 1
    return hash

#вывод результатов работы программы
def main():
    print('ГОСТ Р 34.10-94:')
    print('КОРОТКИЙ ТЕКСТ:')
    ciphergostd(input_for_cipher_short())
    print('ДЛИННЫЙ ТЕКСТ:')
    ciphergostd(input_for_cipher_long())

if __name__ == "__main__":
    main()

    

