from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted, replace_all_to, clear_text, dict

bp = Blueprint('lab01', __name__, url_prefix='/lab01')


def atbash(input):
    return input.translate(str.maketrans(
        alphabet + alphabet.upper(), alphabet[::-1] + alphabet.upper()[::-1]))


@bp.route('/1', methods=['GET', 'POST'])
def lab01_1():
    clear = ''
    encrypted = ''
    decrypted = ''
    if request.method == 'POST':
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        if clear:
            if encrypted:
                decrypted = output_from_decrypted(atbash(encrypted))
                return render_template('lab01_1.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted)
            else:
                encrypted = atbash(replace_all_to(
                    clear.lower().replace(' ', ''), dict))
                return render_template('lab01_1.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted)
        return render_template('lab01_1.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted)
    else:
        return render_template('lab01_1.html', clear_text=clear_text)


def caesar_encode(input, step):
    return input.translate(
        str.maketrans(alphabet, alphabet[step:] + alphabet[:step]))


def caesar_decode(input, step):
    return input.translate(
        str.maketrans(alphabet[step:] + alphabet[:step], alphabet))


@bp.route('/2', methods=['GET', 'POST'])
def lab01_2():
    clear = ''
    encrypted = ''
    decrypted = ''
    key = 0
    if request.method == 'POST':
        key = request.form.get('key')
        if key == '':
            key = 0
        key = int(key)
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        if clear:
            if encrypted:
                decrypted = output_from_decrypted(
                    caesar_decode(encrypted, key))
                return render_template('lab01_2.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
            else:
                encrypted = caesar_encode(replace_all_to(
                    clear.lower().replace(' ', ''), dict), key)
                return render_template('lab01_2.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
        return render_template('lab01_2.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
    else:
        return render_template('lab01_2.html', clear_text=clear_text, key=5)


hard_dictionary = {"а": "11", "б": "12", "в": "13",
                   "г": "14", "д": "15", "е": "16", "ё": "21",
                   "ж": "22", "з": "23", "и": "24", "й": "25",
                   "к": "26", "л": "31", "м": "32", "н": "33",
                   "о": "34", "п": "35", "р": "36", "с": "41",
                   "т": "42", "у": "43", "ф": "44", "х": "45",
                   "ц": "46", "ч": "51", "ш": "52", "щ": "53",
                   "ъ": "54", "ы": "55", "ь": "56", "э": "61",
                   "ю": "62", "я": "63"}


def square_encode(input):
    new_txt = ""
    for x in input:
        if x in hard_dictionary:
            new_txt += hard_dictionary.get(x)
        else:
            new_txt += (x + x)
    return new_txt


def square_decode(input):
    new_txt = ""
    list_fraze = []
    step = 2
    for i in range(0, len(input), 2):
        list_fraze.append(input[i:step])
        step += 2
    key_hard_dictionary_list = list(hard_dictionary.keys())
    val_hard_dictionary_list = list(hard_dictionary.values())

    for x in list_fraze:
        if x in val_hard_dictionary_list:
            i = val_hard_dictionary_list.index(x)
            new_txt += key_hard_dictionary_list[i]
        else:
            new_txt += x[0:1]
    return new_txt


@bp.route('/3', methods=['GET', 'POST'])
def lab01_3():
    clear = ''
    encrypted = ''
    decrypted = ''
    if request.method == 'POST':
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        if clear:
            if encrypted:
                decrypted = output_from_decrypted(square_decode(encrypted))
                return render_template('lab01_3.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=hard_dictionary)
            else:
                encrypted = square_encode(replace_all_to(
                    clear.lower().replace(' ', ''), dict))
                return render_template('lab01_3.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=hard_dictionary)
        return render_template('lab01_3.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=hard_dictionary)
    else:
        return render_template('lab01_3.html', clear_text=clear_text, key=hard_dictionary)
