from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted, replace_all_to, clear_text, dict

bp = Blueprint('lab02', __name__, url_prefix='/lab02')


def trithemius_decode(input):
    decode: str = ""
    k = 0
    for position, symbol in enumerate(input):
        index = (alphabet.find(symbol) + k) % len(alphabet)
        decode += alphabet[index]
        k -= 1
    return decode


def trithemius_encode(input):
    encode = ""
    k = 0
    for position, symbol in enumerate(input):
        index = (alphabet.find(symbol) + k) % len(alphabet)
        encode += alphabet[index]
        k += 1
    return encode


@bp.route('/4', methods=['GET', 'POST'])
def lab02_4():
    clear = ''
    encrypted = ''
    decrypted = ''
    if request.method == 'POST':
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        if clear:
            if encrypted:
                decrypted = output_from_decrypted(trithemius_encode(encrypted))
                return render_template('lab02_4.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted)
            else:
                encrypted = trithemius_decode(replace_all_to(
                    clear.lower().replace(' ', ''), dict))
                return render_template('lab02_4.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted)
        return render_template('lab02_4.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted)
    else:
        return render_template('lab02_4.html', clear_text=clear_text)


def bellaso_decode(input, key):
    decrypted = ''
    offset = 0
    for ix in range(len(input)):
        if input[ix] not in alphabet:
            output = input[ix]
            offset += -1
        elif (alphabet.find(input[ix])) > (len(alphabet) - (alphabet.find(key[((ix + offset) % len(key))])) - 1):
            output = alphabet[(alphabet.find(
                input[ix]) - (alphabet.find(key[((ix + offset) % len(key))]))) % 33]
        else:
            output = alphabet[alphabet.find(
                input[ix]) - (alphabet.find(key[((ix + offset) % len(key))]))]
        decrypted += output
    return decrypted


def bellaso_encode(input, key):
    encoded = ''
    offset = 0
    for ix in range(len(input)):
        if input[ix] not in alphabet:
            output = input[ix]
            offset += -1
        elif (alphabet.find(input[ix])) > (len(alphabet) - (alphabet.find(key[((ix + offset) % len(key))])) - 1):
            output = alphabet[(alphabet.find(
                input[ix]) + (alphabet.find(key[((ix + offset) % len(key))]))) % 33]
        else:
            output = alphabet[alphabet.find(
                input[ix]) + (alphabet.find(key[((ix + offset) % len(key))]))]
        encoded += output
    return encoded


@bp.route('/5', methods=['GET', 'POST'])
def lab02_5():
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
                decrypted = output_from_decrypted(
                    bellaso_decode(encrypted, key))
                return render_template('lab02_5.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
            else:
                encrypted = bellaso_encode(replace_all_to(
                    clear.lower().replace(' ', ''), dict), key)
                return render_template('lab02_5.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
        return render_template('lab02_5.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
    else:
        return render_template('lab02_5.html', clear_text=clear_text, key='ключ')
