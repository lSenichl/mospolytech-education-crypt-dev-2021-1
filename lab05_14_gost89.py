# -*- coding:utf-8 -*-
# импорт компонентов, необходимых для работы программы
import sys
import numpy.random
import itertools
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted
import binascii

# объявление класса
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

    # функция шифрования
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

    # функция расшифрования
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

# объявление S-блока
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

# установка ключа
key = 18318279387912387912789378912379821879387978238793278872378329832982398023031

text_short = input_for_cipher_short().encode().hex()
text_short = int(text_short, 16)

gost_short = GostCrypt(key, sbox)

encode_text_short = gost_short.encrypt(text_short)
decode_text_short = gost_short.decrypt(encode_text_short)
decode_text_short = bytes.fromhex(hex(decode_text_short)[2::]).decode('utf-8')


text_long = input_for_cipher_long().encode().hex()
text_long = int(text_long, 16)

gost_long = GostCrypt(key, sbox)

encode_text_long = gost_long.encrypt(text_long)
decode_text_long = gost_long.decrypt(encode_text_long)
decode_text_long = bytes.fromhex(hex(decode_text_long)[2::]).decode('utf-8')

#вывод результатов работы программы
def main():
    print(f'''
    Гост 28147-89:
    Ключ: {key}
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {encode_text_short}
    
    Расшифрованный текст:
    {output_from_decrypted(decode_text_short)}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {encode_text_long}
    
    Расшифрованный текст:
    {output_from_decrypted(decode_text_long)}
    ''')

if __name__ == "__main__":
    main()


