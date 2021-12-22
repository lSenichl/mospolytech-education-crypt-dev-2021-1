from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from base import input_for_cipher_short, input_for_cipher_long, output_from_decrypted, replace_all_to, clear_text
from base import dict as dictionary
import numpy as np
from egcd import egcd
import random

bp = Blueprint('lab08', __name__, url_prefix='/lab08')


@bp.route('/21', methods=['GET', 'POST'])
def lab08_21():
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a


    def multiplicative_inverse(e, r):
        for i in range(r):
            if((e*i) % r == 1):
                return i


    def is_prime(num):
        if num == 2:
            return True
        if num < 2 or num % 2 == 0:
            return False
        for n in range(3, int(num**0.5)+2, 2):
            if num % n == 0:
                return False
        return True


    def generate_keypair(p, q):
        if not (is_prime(p) and is_prime(q)):
            raise ValueError('Оба числа должны быть простыми.')
        elif p == q:
            raise ValueError('p и q не могут быть равны друг другу')
        n = p * q

        phi = (p-1) * (q-1)

        e = random.randrange(1, phi)

        g = gcd(e, phi)
        while g != 1:
            e = random.randrange(1, phi)
            g = gcd(e, phi)
        d = multiplicative_inverse(e, phi)
        return ((e, n), (d, n))


    def encrypt(pk, plaintext):
        key, n = pk
        cipher = [(ord(char) ** key) % n for char in plaintext]
        return cipher


    def decrypt(pk, ciphertext):
        key, n = pk
        plain = [chr((int(char) ** int(key)) % int(n)) for char in ciphertext]
        return ''.join(plain)

    clear = ''
    encrypted = ''
    decrypted = ''
    p_key = 107
    q_key = 109
    if request.method == 'POST':
        p_key = int(request.form.get('p_key'))
        q_key = int(request.form.get('q_key'))
        if p_key == '' or q_key == '':
            p_key = 107
            q_key = 109
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        if clear:
            if encrypted:
                public = request.form.get('public')
                private = request.form.get('private')
                encrypted = encrypted[1:-1].split(', ')
                decrypted = output_from_decrypted(decrypt(public[1:-1].split(', '), encrypted)).replace(' ', '')
                return render_template('lab08_21.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, p_key=p_key, q_key=q_key, public=public, private=private)
            else:
                public, private = generate_keypair(p_key, q_key)
                encrypted = replace_all_to(clear.lower().replace(' ', ''), dictionary)
                encrypted = encrypt(private, encrypted)
                return render_template('lab08_21.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, p_key=p_key, q_key=q_key, public=public, private=private)
        return render_template('lab08_21.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, p_key=p_key, q_key=q_key)
    else:
        return render_template('lab08_21.html', clear_text=clear_text, p_key = 107, q_key = 109)
