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

import random
import collections

@bp.route('/27', methods=['GET', 'POST'])
def lab10_27():
    alphabet_lower = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4,
                'е': 5, 'ё': 6, 'ж': 7, 'з': 8, 'и': 9, 'й': 10,
                'к': 11, 'л': 12, 'м': 13, 'н': 14, 'о': 15,
                'п': 16, 'р': 17, 'с': 18, 'т': 19, 'у': 20,
                'ф': 21, 'х': 22, 'ц': 23, 'ч': 24, 'ш': 25,
                'щ': 26, 'ъ': 27, 'ы': 28, 'ь': 29, 'э': 30,
                'ю': 31, 'я': 32
                }


    class Point:
        def __init__(self, x_init, y_init):
            self.x = x_init
            self.y = y_init

        def shift(self, x, y):
            self.x += x
            self.y += y

        def __repr__(self):
            return "".join(["( x=", str(self.x), ", y=", str(self.y), ")"])


    x_1 = 0
    y_1 = 0

    EllipticCurve = collections.namedtuple(
        'EllipticCurve', 'name p q_mod a b q g n h')
    curve = EllipticCurve(
        'secp256k1',
        p=0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f,
        q_mod=0xfffffffffefffffffffcfffffffffffcfffffffffffffffffffffffefffffc2f,

        a=7,
        b=11,

        g=(0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
        0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8),
        q=(0xA0434D9E47F3C86235477C7B1AE6AE5D3442D49B1943C2B752A68E2A47E247C7,
        0x893ABA425419BC27A3B6C7E693A24C696F794C2ED877A1593CBEE53B037368D7),

        n=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141,

        h=1,
    )


    def ciphergosto(clearText):
        out = ''
        msg = clearText
        msg_list = list(msg)
        alpha_code_msg = list()
        for i in range(len(msg_list)):
            alpha_code_msg.append(int(alphabet_lower.get(msg_list[i])))
        out += "Длина исходного сообщения {} символов".format(len(alpha_code_msg)) +'\n'

        out += "Q mod" + str(curve.q_mod) +'\n'
        out += "P mod" + str(curve.p) +'\n'

        hash_code_msg = hash_value(curve.p, alpha_code_msg)
        out += "Хэш сообщения:={}".format(hash_code_msg) +'\n'

        e = hash_code_msg % curve.q_mod
        out += "E={}".format(e) +'\n'

        k = random.randint(1, curve.q_mod)
        out += "K={}".format(k) +'\n'
        
        d = 10
        out += "D={}".format(d) +'\n'
        x, y = scalar_mult(k, curve.g)
        point_c = Point(x, y)
        out += "Point_C={}".format(point_c) +'\n'
        r = point_c.x % curve.q_mod
        out += "R={}".format(r) +'\n'
        s = (r*curve.p + k*e) % curve.q_mod
        out += "S={}".format(s) +'\n'

        v = inverse_mod(e, curve.p)
        out += "V={}".format(v) +'\n'
        z1 = (s*v) % curve.q_mod
        z2 = ((curve.p-r)*v) % curve.q_mod
        x_1, y_1 = scalar_mult(d, curve.g)
        out += "Point_Q=( x={}, y={} )".format(x_1, y_1) +'\n'
        point_c_new = Point(x, y)
        x, y = point_add(scalar_mult(z1, curve.g),
                        scalar_mult(z2, curve.q))
        r_1 = point_c_new.x % curve.q_mod
        out += "R_new={}".format(r_1) +'\n'
        if r == r_1:
            out += "Подпись прошла проверку!\n"
        else:
            out += "Ошибка проверки!" +'\n'
        return out


    def hash_value(mod, alpha_code_msg):
        i = 0
        hashing_value = 1
        while i < len(alpha_code_msg):
            hashing_value = (
                ((hashing_value-1) + int(alpha_code_msg[i]))**2) % curve.p
            i += 1
        return hashing_value


    def is_on_curve(point):
        if point is None:
            return True

        x, y = point

        return (y * y - x * x * x - curve.a * x - curve.b) % curve.p == 0


    def point_neg(point):
        if point is None:
            return None
        x, y = point
        result = (x, -y % curve.p)
        return result


    def inverse_mod(k, p):
        if k == 0:
            raise ZeroDivisionError('деление на 0')

        if k < 0:
            return p - inverse_mod(-k, p)

        s, old_s = 0, 1
        t, old_t = 1, 0
        r, old_r = p, k

        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        gcd, x, y = old_r, old_s, old_t

        assert gcd == 1
        assert (k * x) % p == 1

        return x % p


    def point_add(point1, point2):
        if point1 is None:
            return point2
        if point2 is None:
            return point1

        x1, y1 = point1
        x2, y2 = point2

        if x1 == x2 and y1 != y2:
            return None

        if x1 == x2:
            m = (3 * x1 * x1 + curve.a) * inverse_mod(2 * y1, curve.p)
        else:
            m = (y1 - y2) * inverse_mod(x1 - x2, curve.p)

        x3 = m * m - x1 - x2
        y3 = y1 + m * (x3 - x1)
        result = (x3 % curve.p,
                -y3 % curve.p)
        return result


    def scalar_mult(k, point):
        if k % curve.n == 0 or point is None:
            return None

        if k < 0:
            return scalar_mult(-k, point_neg(point))

        result = None
        addend = point

        while k:
            if k & 1:
                result = point_add(result, addend)
            addend = point_add(addend, addend)
            k >>= 1
        return result


    clear = ''
    if request.method == 'POST':
        clear = request.form.get('clear')
        encrypted = ciphergosto(replace_all_to(clear.lower().replace(' ', ''), dictionary))
        return render_template('lab10_27.html', clear_text=clear, encrypted_text=encrypted)
    else:
        return render_template('lab10_27.html', clear_text=clear_text)
