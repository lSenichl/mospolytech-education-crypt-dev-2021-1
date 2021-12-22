from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from base import input_for_cipher_short, input_for_cipher_long, output_from_decrypted, replace_all_to, clear_text, alphabet
from base import dict as dictionary
import numpy as np
from egcd import egcd
import math
import random

bp = Blueprint('lab05', __name__, url_prefix='/lab05')


alphabet_new = alphabet.replace(' ', '')
alphabet_lower = {}
i = 0
while i < (len(alphabet)):
    alphabet_lower.update({alphabet_new[i]: i})
    i += 1


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def shenon_encode(msg):
    msg_list = list(msg)
    msg_list_len = len(msg_list)
    msg_code_bin_list = list()
    for i in range(len(msg_list)):
        msg_code_bin_list.append(alphabet_lower.get(msg_list[i]))

    key_list = list()
    for i in range(msg_list_len):
        key_list.append(random.randint(0, 32))

    cipher_list = list()
    for i in range(msg_list_len):
        m = int(msg_code_bin_list[i])
        k = int(key_list[i])
        cipher_list.append(int(bin(m ^ k), base=2))
    return cipher_list, key_list


def shenon_decode(msg, key_list):
    decipher_list = list()
    msg_list_len = len(msg)
    for i in range(msg_list_len):
        c = int(msg[i])
        k = int(key_list[i])
        decipher_list.append(int(bin(c ^ k), base=2))
    deciphered_str = ""
    for i in range(len(decipher_list)):
        deciphered_str += get_key(alphabet_lower, decipher_list[i])
    return deciphered_str


@bp.route('/13', methods=['GET', 'POST'])
def lab05_13():
    clear = ''
    encrypted = ''
    decrypted = ''
    key = ''
    if request.method == 'POST':
        key = request.form.get('key')
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        if clear:
            if encrypted:
                decrypted = output_from_decrypted(shenon_decode(list(encrypted[1:-1].split(', ')), list(key[1:-1].split(', '))))
                return render_template('lab05_13.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
            else:
                encrypted, key = shenon_encode(replace_all_to(clear.lower().replace(' ', ''), dictionary))
                return render_template('lab05_13.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
        return render_template('lab05_13.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
    else:
        return render_template('lab05_13.html', clear_text=clear_text, key='')

class GostCrypt(object):
    def __init__(self, key, sbox):
        self._key = None
        self._subkeys = None
        self.key = key
        self.sbox = sbox

    @staticmethod
    def _bit_length(value):
        return len(bin(value)[2:])

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key
        self._subkeys = [(key >> (32 * i)) & 0xFFFFFFFF for i in range(8)]

    def _f(self, part, key):
        temp = part ^ key
        output = 0
        for i in range(8):
            output |= ((self.sbox[i][(temp >> (4 * i)) & 0b1111]) << (4 * i))
        return ((output >> 11) | (output << (32 - 11))) & 0xFFFFFFFF

    def _decrypt_round(self, left_part, right_part, round_key):
        return left_part, right_part ^ self._f(left_part, round_key)

    def encrypt(self, plain_msg):
        def _encrypt_round(left_part, right_part, round_key):
            return right_part, left_part ^ self._f(right_part, round_key)

        left_part = plain_msg >> 32
        right_part = plain_msg & 0xFFFFFFFF
        for i in range(24):
            left_part, right_part = _encrypt_round(
                left_part, right_part, self._subkeys[i % 8])
        for i in range(8):
            left_part, right_part = _encrypt_round(
                left_part, right_part, self._subkeys[7 - i])
        return (left_part << 32) | right_part

    def decrypt(self, crypted_msg):
        def _decrypt_round(left_part, right_part, round_key):
            return right_part ^ self._f(left_part, round_key), left_part

        left_part = crypted_msg >> 32
        right_part = crypted_msg & 0xFFFFFFFF
        for i in range(8):
            left_part, right_part = _decrypt_round(
                left_part, right_part, self._subkeys[i])
        for i in range(24):
            left_part, right_part = _decrypt_round(
                left_part, right_part, self._subkeys[(7 - i) % 8])
        return (left_part << 32) | right_part

import numpy.random
import itertools

sbox = [numpy.random.permutation(l)
        for l in itertools.repeat(list(range(16)), 8)]
sbox = (
    (4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3),
    (14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9),
    (5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11),
    (7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3),
    (6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2),
    (4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14),
    (13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12),
    (1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12),
)

@bp.route('/14', methods=['GET', 'POST'])
def lab05_14():
    clear = ''
    encrypted = ''
    decrypted = ''
    key = 18318279387912387912789378912379821879387978238793278872378329832982398023031
    if request.method == 'POST':
        key = int(request.form.get('key'))
        if key == '':
            key = 18318279387912387912789378912379821879387978238793278872378329832982398023031
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        gost = GostCrypt(key, sbox)
        if clear:
            if encrypted:
                decrypted = gost.decrypt(int(encrypted))
                decrypted = bytes.fromhex(hex(decrypted)[2::]).decode('utf-8')
                decrypted = output_from_decrypted(decrypted)
                return render_template('lab05_14.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
            else:
                encrypted = replace_all_to(clear.lower().replace(' ', ''), dictionary)
                encrypted = gost.encrypt(int(encrypted.encode().hex(), 16))
                return render_template('lab05_14.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
        return render_template('lab05_14.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
    else:
        return render_template('lab05_14.html', clear_text=clear_text, key = 18318279387912387912789378912379821879387978238793278872378329832982398023031)