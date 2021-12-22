from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from base import input_for_cipher_short, input_for_cipher_long, output_from_decrypted, replace_all_to, clear_text, alphabet
from base import dict as dictionary
import numpy as np
from egcd import egcd

bp = Blueprint('lab03', __name__, url_prefix='/lab03')


@bp.route('/8', methods=['GET', 'POST'])
def lab03_8():
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "

    letter_to_index = dict(zip(alphabet, range(len(alphabet))))
    index_to_letter = dict(zip(range(len(alphabet)), alphabet))


    def matrix_mod_inv(matrix, modulus):
        det = int(np.round(np.linalg.det(matrix)))
        det_inv = egcd(det, modulus)[1] % modulus
        matrix_modulus_inv = (
            det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
        )

        return matrix_modulus_inv


    def matrix_encode(message, K):
        encrypted = ""
        message_in_numbers = []
        for letter in message:
            message_in_numbers.append(letter_to_index[letter])

        split_P = [
            message_in_numbers[i: i + int(K.shape[0])]
            for i in range(0, len(message_in_numbers), int(K.shape[0]))
        ]

        for P in split_P:
            P = np.transpose(np.asarray(P))[:, np.newaxis]

            while P.shape[0] != K.shape[0]:
                P = np.append(P, letter_to_index[" "])[:, np.newaxis]

            numbers = np.dot(K, P) % len(alphabet)
            n = numbers.shape[0]

            for idx in range(n):
                number = int(numbers[idx, 0])
                encrypted += index_to_letter[number]
        return encrypted


    def matrix_decode(cipher, Kinv):
        decrypted = ""
        cipher_in_numbers = []
        for letter in cipher:
            cipher_in_numbers.append(letter_to_index[letter])

        split_C = [
            cipher_in_numbers[i: i + int(Kinv.shape[0])]
            for i in range(0, len(cipher_in_numbers), int(Kinv.shape[0]))
        ]

        for C in split_C:
            C = np.transpose(np.asarray(C))[:, np.newaxis]
            numbers = np.dot(Kinv, C) % len(alphabet)
            n = numbers.shape[0]

            for idx in range(n):
                number = int(numbers[idx, 0])
                decrypted += index_to_letter[number]
        return decrypted
    clear = ''
    encrypted = ''
    decrypted = ''
    key = '3 10 20 20 19 17 23 78 17'
    if request.method == 'POST':
        key = request.form.get('key')
        if key == '':
            key = '3 10 20 20 19 17 23 78 17'
        key_for_decrypt = key.split(' ')
        key_for_decrypt = np.matrix([[int(key_for_decrypt[0]), int(key_for_decrypt[1]), int(key_for_decrypt[2])], [int(key_for_decrypt[3]), int(
            key_for_decrypt[4]), int(key_for_decrypt[5])], [int(key_for_decrypt[6]), int(key_for_decrypt[7]), int(key_for_decrypt[8])]])
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        if clear:
            if encrypted:
                decrypted = output_from_decrypted(matrix_decode(encrypted, matrix_mod_inv(key_for_decrypt, len(alphabet)))).replace(' ', '')
                return render_template('lab03_8.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
            else:
                encrypted = matrix_encode(replace_all_to(
                    clear.lower().replace(' ', ''), dictionary), key_for_decrypt)
                return render_template('lab03_8.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
        return render_template('lab03_8.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
    else:
        return render_template('lab03_8.html', clear_text=clear_text, key='3 10 20 20 19 17 23 78 17')


@bp.route('/9', methods=['GET', 'POST'])
def lab03_9():
    alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя ".replace(' ', '') + 'abc'


    def playfair_encode(clearText, key):

        text = clearText
        new_alphabet = []
        for i in range(len(key)):
            new_alphabet.append(key[i])
        for i in range(len(alphabet)):
            bool_buff = False
            for j in range(len(key)):
                if alphabet[i] == key[j]:
                    bool_buff = True
                    break
            if bool_buff == False:
                new_alphabet.append(alphabet[i])
        mtx_abt_j = []
        counter = 0
        for j in range(6):
            mtx_abt_i = []
            for i in range(6):
                mtx_abt_i.append(new_alphabet[counter])
                counter = counter + 1
            mtx_abt_j.append(mtx_abt_i)
        # проверка на одинаковые биграммы
        for i in range(len(text) - 1):
            if text[i] == text[i + 1]:
                if text[i] != 'я':
                    text = text[:i + 1] + 'я' + text[i + 1:]
                else:
                    text = text[:i + 1] + 'ю' + text[i + 1:]
        # проверка на четную длину текста
        if len(text) % 2 == 1:
            text = text + "я"
        enc_text = ""
        for t in range(0, len(text), 2):
            flag = True
            for j_1 in range(6):
                if flag == False:
                    break
                for i_1 in range(6):
                    if flag == False:
                        break
                    if mtx_abt_j[j_1][i_1] == text[t]:
                        for j_2 in range(6):
                            if flag == False:
                                break
                            for i_2 in range(6):
                                if mtx_abt_j[j_2][i_2] == text[t+1]:
                                    if j_1 != j_2 and i_1 != i_2:
                                        enc_text = enc_text + \
                                            mtx_abt_j[j_1][i_2] + \
                                            mtx_abt_j[j_2][i_1]
                                    elif j_1 == j_2 and i_1 != i_2:
                                        enc_text = enc_text + \
                                            mtx_abt_j[j_1][(i_1+1) % 6] + \
                                            mtx_abt_j[j_2][(i_2+1) % 6]
                                    elif j_1 != j_2 and i_1 == i_2:
                                        enc_text = enc_text + \
                                            mtx_abt_j[(j_1+1) % 5][i_1] + \
                                            mtx_abt_j[(j_2+1) % 5][i_2]
                                    elif j_1 == j_2 and i_1 == i_2:
                                        enc_text = enc_text + \
                                            mtx_abt_j[j_1][i_1] + \
                                            mtx_abt_j[j_1][i_1]
                                    flag = False
                                    break
        return enc_text


    def playfair_decode(clearText, key):
        text = clearText
        new_alphabet = []
        for i in range(len(key)):
            new_alphabet.append(key[i])
        for i in range(len(alphabet)):
            bool_buff = False
            for j in range(len(key)):
                if alphabet[i] == key[j]:
                    bool_buff = True
                    break
            if bool_buff == False:
                new_alphabet.append(alphabet[i])
        mtx_abt_j = []
        counter = 0
        for j in range(6):
            mtx_abt_i = []
            for i in range(6):
                mtx_abt_i.append(new_alphabet[counter])
                counter = counter + 1
            mtx_abt_j.append(mtx_abt_i)
        enc_text = ""
        for t in range(0, len(text), 2):
            flag = True
            for j_1 in range(6):
                if flag == False:
                    break
                for i_1 in range(6):
                    if flag == False:
                        break
                    if mtx_abt_j[j_1][i_1] == text[t]:
                        for j_2 in range(6):
                            if flag == False:
                                break
                            for i_2 in range(6):
                                if mtx_abt_j[j_2][i_2] == text[t+1]:
                                    if j_1 != j_2 and i_1 != i_2:
                                        enc_text = enc_text + \
                                            mtx_abt_j[j_1][i_2] + \
                                            mtx_abt_j[j_2][i_1]
                                    elif j_1 == j_2 and i_1 != i_2:
                                        enc_text = enc_text + \
                                            mtx_abt_j[j_1][(i_1-1) % 6] + \
                                            mtx_abt_j[j_2][(i_2-1) % 6]
                                    elif j_1 != j_2 and i_1 == i_2:
                                        enc_text = enc_text + \
                                            mtx_abt_j[(j_1-1) % 5][i_1] + \
                                            mtx_abt_j[(j_2-1) % 5][i_2]
                                    elif j_1 == j_2 and i_1 == i_2:
                                        enc_text = enc_text + \
                                            mtx_abt_j[j_1][i_1] + \
                                            mtx_abt_j[j_1][i_1]
                                    flag = False
                                    break
        return enc_text
    clear = ''
    encrypted = ''
    decrypted = ''
    key = 'ключ'
    if request.method == 'POST':
        key = request.form.get('key')
        if key == '':
            key = 'ключ'
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        if clear:
            if encrypted:
                decrypted = output_from_decrypted(playfair_decode(encrypted, key))
                return render_template('lab03_9.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
            else:
                encrypted = playfair_encode(replace_all_to(clear.lower().replace(' ', ''), dictionary), key)
                return render_template('lab03_9.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
        return render_template('lab03_9.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
    else:
        return render_template('lab03_9.html', clear_text=clear_text, key='ключ')
