from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from base import input_for_cipher_short, input_for_cipher_long, output_from_decrypted, replace_all_to, clear_text
from base import dict as dictionary
import numpy as np
from egcd import egcd

bp = Blueprint('lab03', __name__, url_prefix='/lab03')

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


@bp.route('/8', methods=['GET', 'POST'])
def lab03_8():
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
