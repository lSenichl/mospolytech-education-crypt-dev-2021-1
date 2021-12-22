from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted, replace_all_to, clear_text, dict
from math import gcd
from base import dict as dictionary

bp = Blueprint('lab10', __name__, url_prefix='/lab10')


@bp.route('/26', methods=['GET', 'POST'])
def lab10_26():
    alphavit = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4,
            'е': 5, 'ё': 6, 'ж': 7, 'з': 8, 'и': 9, 'й': 10,
            'к': 11, 'л': 12, 'м': 13, 'н': 14, 'о': 15,
            'п': 16, 'р': 17, 'с': 18, 'т': 19, 'у': 20,
            'ф': 21, 'х': 22, 'ц': 23, 'ч': 24, 'ш': 25,
            'щ': 26, 'ъ': 27, 'ы': 28, 'ь': 29, 'э': 30,
            'ю': 31, 'я': 32
            }


    def ciphergostd(clearText):
        out = ''
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
        out += "p = " + str(p) + '\n'
        q = 5
        out += "q = " + str(q) + '\n'
        a = 2
        out += "a = " + str(a) + '\n'

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
        out += "x = " + str(x) + '\n'
        y = a**x % p
        k = 4
        out += "k = " + str(k) + '\n'
        r = (a**k % p) % q

        msg = clearText
        msg_list = list(msg)
        alpha_code_msg = list()
        for i in range(len(msg_list)):
            alpha_code_msg.append(int(alphavit.get(msg_list[i])))
        out += "Длина исходного сообщения {} символов".format(len(alpha_code_msg)) + '\n'
        hash_code_msg = hash_value(p, alpha_code_msg)
        out += "Хэш сообщения:= {}".format(hash_code_msg) + '\n'

        s = (x*r+k*hash_code_msg) % q

        out += "Цифровая подпись = " + str(r % (2**256)) + "," + str(s % (2**256)) + '\n'

        v = (hash_code_msg**(q-2)) % q
        z1 = s*v % q
        z2 = ((q-r)*v) % q
        u = (((a**z1)*(y**z2)) % p) % q
        out += str(r) + " = " + str(u) + '\n'
        if u == r:
            out += "r = u, следовательно: " + "Подпись верна" +'\n'
        else:
            out += "Подпись неверна" +'\n'
        return out


    def hash_value(n, alpha_code):
        i = 0
        hash = 1
        while i < len(alpha_code):
            hash = (((hash-1) + int(alpha_code[i]))**2) % n
            i += 1
        return hash
    
    clear = ''
    if request.method == 'POST':
        clear = request.form.get('clear')
        encrypted = ciphergostd(replace_all_to(clear.lower().replace(' ', ''), dictionary))
        return render_template('lab10_26.html', clear_text=clear, encrypted_text=encrypted)
    else:
        return render_template('lab10_26.html', clear_text=clear_text)
