from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted, replace_all_to, clear_text, dict
from math import gcd
from base import dict as dictionary

bp = Blueprint('lab09', __name__, url_prefix='/lab09')


@bp.route('/24', methods=['GET', 'POST'])
def lab09_24():
    alphabet_lower = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4,
                  'е': 5, 'ё': 6, 'ж': 7, 'з': 8, 'и': 9, 'й': 10,
                  'к': 11, 'л': 12, 'м': 13, 'н': 14, 'о': 15,
                  'п': 16, 'р': 17, 'с': 18, 'т': 19, 'у': 20,
                  'ф': 21, 'х': 22, 'ц': 23, 'ч': 24, 'ш': 25,
                  'щ': 26, 'ъ': 27, 'ы': 28, 'ь': 29, 'э': 30,
                  'ю': 31, 'я': 32
                  }


    def IsPrime(n):
        d = 2
        while n % d != 0:
            d += 1
        return d == n


    def modInverse(e, el):
        e = e % el
        for x in range(1, el):
            if ((e * x) % el == 1):
                return x
        return 1


    def check_signature(sign_msg, n, e):
        check = (sign_msg**e) % n
        return check


    def hash_value(n, alpha_code_msg):
        i = 0
        hashing_value = 1
        while i < len(alpha_code_msg):
            hashing_value = (((hashing_value-1) + int(alpha_code_msg[i]))**2) % n
            i += 1
        return hashing_value


    def signature_msg(hash_code, n, d):
        sign = (hash_code**d) % n
        return sign


    def rsacipher(p, q, clearText):
        out = ''
        p = int(p)
        out += 'p: ' + str(IsPrime(p)) + '\n'
        q = int(q)
        out += 'q: ' + str(IsPrime(q)) + '\n'
        n = p * q
        out += 'N =' + str(n) + '\n'
        el = (p-1) * (q-1)
        out += 'El =' + str(el) + '\n'
        e = 7
        out += 'E =' + str(e) + '\n'
        if gcd(e, el) == 1:
            out += str(gcd(e, el)) + ' E подходит\n'
        else:
            out += str(gcd(e, el)) + 'False\n'

        d = modInverse(e, el)
        out += 'D =' + str(d) + '\n'
        out += "Открытый ключ e={} n={}".format(e, n) + '\n'
        out += "Секретный ключ d={} n={}".format(d, n) + '\n'

        msg = clearText
        msg_list = list(msg)
        alpha_code_msg = list()
        for i in range(len(msg_list)):
            alpha_code_msg.append(int(alphabet_lower.get(msg_list[i])))
        out += "Длина исходного сообщения {} символов".format(len(alpha_code_msg)) + '\n'

        hash_code_msg = hash_value(n, alpha_code_msg)
        out += 'Хэш сообщения: ' + str(hash_code_msg) + '\n'

        sign_msg = signature_msg(hash_code_msg, n, d)
        out += "Значение подписи: {}".format(sign_msg) + '\n'

        check_sign = check_signature(sign_msg, n, e)
        out += "Значение проверки хэша = {}".format(check_sign) + '\n'
        return out
    
    clear = ''
    if request.method == 'POST':
        clear = request.form.get('clear')
        p_key = request.form.get('p_key')
        q_key = request.form.get('q_key')
        encrypted = rsacipher(p_key, q_key, replace_all_to(clear.lower().replace(' ', ''), dictionary))
        return render_template('lab09_24.html', clear_text=clear, encrypted_text=encrypted, p_key=p_key, q_key=q_key)
    else:
        return render_template('lab09_24.html', clear_text=clear_text, p_key=31, q_key=7)

import random

@bp.route('/25', methods=['GET', 'POST'])
def lab09_25():
    alphavit = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4,
            'е': 5, 'ё': 6, 'ж': 7, 'з': 8, 'и': 9, 'й': 10,
            'к': 11, 'л': 12, 'м': 13, 'н': 14, 'о': 15,
            'п': 16, 'р': 17, 'с': 18, 'т': 19, 'у': 20,
            'ф': 21, 'х': 22, 'ц': 23, 'ч': 24, 'ш': 25,
            'щ': 26, 'ъ': 27, 'ы': 28, 'ь': 29, 'э': 30,
            'ю': 31, 'я': 32
            }


    def IsPrime(n):
        d = 2
        while n % d != 0:
            d += 1
        return d == n


    def modInverse(e, el):
        e = e % el
        for x in range(1, el):
            if ((e * x) % el == 1):
                return x
        return 1


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


    def gen_prime(n):
        found_prime = False
        while not found_prime:
            p = random.randint(2**(n-1), 2**n)
            if is_prime(p, 1000):
                return p


    def hash_value(mod, alpha_code_msg):
        i = 0
        hashing_value = 1
        while i < len(alpha_code_msg):
            hashing_value = (((hashing_value-1) + int(alpha_code_msg[i]))**2) % mod
            i += 1
        return hashing_value


    def egcipher(clearText):
        out = ''
        p = gen_prime(10)
        out += "P =" + str(p) + '\n'
        g = random.randint(2, p-1)
        out += "G =" + str(g) + '\n'

        x = random.randint(2, p-2)
        y = (g**x) % p
        out += "Открытый ключ(Y)={}, Секретный ключ(X)={}".format(y, x) + '\n'

        msg = clearText
        msg_list = list(msg)
        alpha_code_msg = list()
        for i in range(len(msg_list)):
            alpha_code_msg.append(int(alphavit.get(msg_list[i])))
        out += "Длина исходного сообщения {} символов".format(len(alpha_code_msg)) + '\n'

        hash_code_msg = hash_value(p, alpha_code_msg)
        out += "Хэш сообщения:= {}".format(hash_code_msg) + '\n'

        k = 1
        while True:
            k = random.randint(1, p-2)
            if gcd(k, p-1) == 1:
                out += "K =" + str(k) + '\n'
                break

        a = (g**k) % p

        b = (hash_code_msg - (x*a)) % (p-1)
        out += "Значение подписи: S={},{}".format(a, b) + '\n'
        b = modInverse(k, p-1) * ((hash_code_msg - (x * a)) % (p-1))

        check_hash_value = hash_value(p, alpha_code_msg)
        a_1 = ((y**a) * (a**b)) % p
        out += "A1={}".format(a_1) + '\n'
        a_2 = (g**check_hash_value) % p
        out += "A2={}".format(a_2) + '\n'

        if a_1 == a_2:
            out += "Подпись верна" + '\n'
        else:
            out += "Подпись неверна" + '\n'
        return out
    
    clear = ''
    if request.method == 'POST':
        clear = request.form.get('clear')
        encrypted = egcipher(replace_all_to(clear.lower().replace(' ', ''), dictionary))
        return render_template('lab09_25.html', clear_text=clear, encrypted_text=encrypted)
    else:
        return render_template('lab09_25.html', clear_text=clear_text)
