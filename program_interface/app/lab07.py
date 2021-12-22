from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from base import input_for_cipher_short, input_for_cipher_long, output_from_decrypted, replace_all_to, clear_text
from base import dict as dictionary
import numpy as np
from egcd import egcd
import math

bp = Blueprint('lab07', __name__, url_prefix='/lab07')

@bp.route('/17', methods=['GET', 'POST'])
def lab07_17():
    pi0 = [12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1]
    pi1 = [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15]
    pi2 = [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0]
    pi3 = [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11]
    pi4 = [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12]
    pi5 = [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0]
    pi6 = [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7]
    pi7 = [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2]

    pi = [pi0, pi1, pi2, pi3, pi4, pi5, pi6, pi7]

    MASK32 = 2 ** 32 - 1

    def t(x):
        y = 0
        for i in reversed(range(8)):
            j = (x >> 4 * i) & 0xf
            y <<= 4
            y ^= pi[i][j]
        return y

    def rot11(x):
        return ((x << 11) ^ (x >> (32 - 11))) & MASK32

    def g(x, k):
        return rot11(t((x + k) % 2 ** 32))

    def split(x):
        L = x >> 32
        R = x & MASK32
        return (L, R)

    def join(L, R):
        return (L << 32) ^ R

    def magma_key_schedule(k):
        keys = []
        for i in reversed(range(8)):
            keys.append((k >> (32 * i)) & MASK32)
        for i in range(8):
            keys.append(keys[i])
        for i in range(8):
            keys.append(keys[i])
        for i in reversed(range(8)):
            keys.append(keys[i])
        return keys

    def magma_encrypt(x, k):
        keys = magma_key_schedule(k)
        (L, R) = split(x)
        for i in range(31):
            (L, R) = (R, L ^ g(R, keys[i]))
        return join(L ^ g(R, keys[-1]), R)

    def magma_decrypt(x, k):
        keys = magma_key_schedule(k)
        keys.reverse()
        (L, R) = split(x)
        for i in range(31):
            (L, R) = (R, L ^ g(R, keys[i]))
        return join(L ^ g(R, keys[-1]), R)

    clear = ''
    encrypted = ''
    decrypted = ''
    key = 'ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'
    if request.method == 'POST':
        key = request.form.get('key')
        if key == '':
            key = 'ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        if clear:
            if encrypted:
                decr_short = []
                for i in list(encrypted[1:-1].split(', ')):
                    dt = magma_decrypt(int(i), int(key, 16))
                    decr_short.append(bytes.fromhex(hex(dt)[2::]).decode('utf-8'))
                decrypted = output_from_decrypted(''.join(decr_short))
                return render_template('lab07_17.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
            else:
                i = 0
                text_short = replace_all_to(clear.lower().replace(' ', ''), dictionary)
                encr_short = []
                while (i < len(text_short)):
                    text = text_short[i:i+4].encode().hex()
                    text = int(text, 16)
                    text = text % 2**64
                    pt = text
                    ct = magma_encrypt(pt, int(key, 16))
                    encr_short.append(ct)
                    i += 4
                encrypted = encr_short
                return render_template('lab07_17.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
        return render_template('lab07_17.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
    else:
        return render_template('lab07_17.html', clear_text=clear_text, key = 'ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff')
