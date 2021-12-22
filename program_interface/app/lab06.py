from flask import Flask, render_template, Blueprint, redirect, url_for, flash, request
from base import input_for_cipher_short, input_for_cipher_long, output_from_decrypted, replace_all_to, clear_text
from base import dict as dictionary
import numpy as np
from egcd import egcd
import math

bp = Blueprint('lab06', __name__, url_prefix='/lab06')

@bp.route('/15', methods=['GET', 'POST'])
def lab06_15():
    import re
    import copy
    reg_x_length = 19
    reg_y_length = 22
    reg_z_length = 23

    key_one = ""
    reg_x = []
    reg_y = []
    reg_z = []

    def set_key(key):
        if(len(key) == 64 and re.match("^([01])+", key)):
            key_one = key
            loading_registers(key)
            return True
        return False

    def loading_registers(key):
        i = 0
        while(i < reg_x_length):
            reg_x.insert(i, int(key[i]))
            i = i + 1
        j = 0
        p = reg_x_length
        while(j < reg_y_length):
            reg_y.insert(j, int(key[p]))
            p = p + 1
            j = j + 1
        k = reg_y_length + reg_x_length
        r = 0
        while(r < reg_z_length):
            reg_z.insert(r, int(key[k]))
            k = k + 1
            r = r + 1


    def get_key():
        return key_one


    def to_binary(plain):
        s = ""
        i = 0
        for i in plain:
            binary = str(' '.join(format(ord(x), 'b') for x in i))
            j = len(binary)
            while(j < 12):
                binary = "0" + binary
                s = s + binary
                j = j + 1
        binary_values = []
        k = 0
        while(k < len(s)):
            binary_values.insert(k, int(s[k]))
            k = k + 1
        return binary_values


    def get_majority(x, y, z):
        if(x + y + z > 1):
            return 1
        else:
            return 0


    def get_keystream(length):
        reg_x_temp = copy.deepcopy(reg_x)
        reg_y_temp = copy.deepcopy(reg_y)
        reg_z_temp = copy.deepcopy(reg_z)
        keystream = []
        i = 0
        while i < length:
            majority = get_majority(reg_x_temp[8], reg_y_temp[10], reg_z_temp[10])
            if reg_x_temp[8] == majority:
                new = reg_x_temp[13] ^ reg_x_temp[16] ^ reg_x_temp[17] ^ reg_x_temp[18]
                reg_x_temp_two = copy.deepcopy(reg_x_temp)
                j = 1
                while(j < len(reg_x_temp)):
                    reg_x_temp[j] = reg_x_temp_two[j-1]
                    j = j + 1
                reg_x_temp[0] = new

            if reg_y_temp[10] == majority:
                new_one = reg_y_temp[20] ^ reg_y_temp[21]
                reg_y_temp_two = copy.deepcopy(reg_y_temp)
                k = 1
                while(k < len(reg_y_temp)):
                    reg_y_temp[k] = reg_y_temp_two[k-1]
                    k = k + 1
                reg_y_temp[0] = new_one

            if reg_z_temp[10] == majority:
                new_two = reg_z_temp[7] ^ reg_z_temp[20] ^ reg_z_temp[21] ^ reg_z_temp[22]
                reg_z_temp_two = copy.deepcopy(reg_z_temp)
                m = 1
                while(m < len(reg_z_temp)):
                    reg_z_temp[m] = reg_z_temp_two[m-1]
                    m = m + 1
                reg_z_temp[0] = new_two

            keystream.insert(i, reg_x_temp[18] ^ reg_y_temp[21] ^ reg_z_temp[22])
            i = i + 1
        return keystream


    def convert_binary_to_str(binary):
        s = ""
        length = len(binary) - 12
        i = 0
        while(i <= length):
            s = s + chr(int(binary[i:i+12], 2))
            i = i + 12
        return str(s)


    def encrypt(plain):
        s = ""
        binary = to_binary(plain)
        keystream = get_keystream(len(binary))
        i = 0
        while(i < len(binary)):
            s = s + str(binary[i] ^ keystream[i])
            i = i + 1
        return s


    def decrypt(cipher):
        s = ""
        binary = []
        keystream = get_keystream(len(cipher))
        i = 0
        while(i < len(cipher)):
            binary.insert(i, int(cipher[i]))
            s = s + str(binary[i] ^ keystream[i])
            i = i + 1
        return convert_binary_to_str(str(s))
    clear = ''
    encrypted = ''
    decrypted = ''
    key = '0101001000011010110001110001100100101001000000110111111010110111'
    set_key(key)
    if request.method == 'POST':
        key = request.form.get('key')
        set_key(key)
        if key == '':
            key = '0101001000011010110001110001100100101001000000110111111010110111'
            set_key(key)
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        if clear:
            if encrypted:
                decrypted = output_from_decrypted(decrypt(encrypted))
                return render_template('lab06_15.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
            else:
                encrypted = encrypt(replace_all_to(
                    clear.lower().replace(' ', ''), dictionary))
                return render_template('lab06_15.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
        return render_template('lab06_15.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
    else:
        return render_template('lab06_15.html', clear_text=clear_text, key = '0101001000011010110001110001100100101001000000110111111010110111')


@bp.route('/16', methods=['GET', 'POST'])
def lab06_16():
    import copy
    import re

    reg_x_length = 19
    reg_y_length = 22
    reg_z_length = 23
    reg_e_length = 17

    key_one = ""
    reg_x = []
    reg_y = []
    reg_z = []
    reg_e = []


    def loading_registers(key):
        i = 0
        while(i < reg_x_length):
            reg_x.insert(i, int(key[i]))
            i = i + 1
        j = 0
        p = reg_x_length
        while(j < reg_y_length):
            reg_y.insert(j, int(key[p]))
            p = p + 1
            j = j + 1
        k = reg_y_length + reg_x_length
        r = 0
        while(r < reg_z_length):
            reg_z.insert(r, int(key[k]))
            k = k + 1
            r = r + 1
        i = 0
        while(i < reg_e_length):
            reg_e.insert(i, int(key[i]))
            i = i + 1


    def set_key(key):
        if(len(key) == 64 and re.match("^([01])+", key)):
            key_one = key
            loading_registers(key)
            return True
        return False


    def get_key():
        return key_one


    def to_binary(plain):
        s = ""
        i = 0
        for i in plain:
            binary = str(' '.join(format(ord(x), 'b') for x in i))
            j = len(binary)
            while(j < 12):
                binary = "0" + binary
                s = s + binary
                j = j + 1
        binary_values = []
        k = 0
        while(k < len(s)):
            binary_values.insert(k, int(s[k]))
            k = k + 1
        return binary_values


    def get_majority(x, y, z):
        if(x + y + z > 1):
            return 1
        else:
            return 0


    def get_keystream(length):
        reg_x_temp = copy.deepcopy(reg_x)
        reg_y_temp = copy.deepcopy(reg_y)
        reg_z_temp = copy.deepcopy(reg_z)
        reg_e_temp = copy.deepcopy(reg_e)
        keystream = []
        i = 0
        while i < length:
            majority = get_majority(reg_e_temp[3], reg_e_temp[7], reg_e_temp[10])
            if get_majority(reg_x_temp[12], reg_x_temp[14], reg_x_temp[15]) == majority:
                new = reg_x_temp[13] ^ reg_x_temp[16] ^ reg_x_temp[17] ^ reg_x_temp[18]
                reg_x_temp_two = copy.deepcopy(reg_x_temp)
                j = 1
                while(j < len(reg_x_temp)):
                    reg_x_temp[j] = reg_x_temp_two[j-1]
                    j = j + 1
                reg_x_temp[0] = new

            if get_majority(reg_y_temp[9], reg_y_temp[13], reg_y_temp[16]) == majority:
                new_one = reg_y_temp[20] ^ reg_y_temp[21]
                reg_y_temp_two = copy.deepcopy(reg_y_temp)
                k = 1
                while(k < len(reg_y_temp)):
                    reg_y_temp[k] = reg_y_temp_two[k-1]
                    k = k + 1
                reg_y_temp[0] = new_one

            if get_majority(reg_z_temp[13], reg_z_temp[16], reg_z_temp[18]) == majority:
                new_two = reg_z_temp[7] ^ reg_z_temp[20] ^ reg_z_temp[21] ^ reg_z_temp[22]
                reg_z_temp_two = copy.deepcopy(reg_z_temp)
                m = 1
                while(m < len(reg_z_temp)):
                    reg_z_temp[m] = reg_z_temp_two[m-1]
                    m = m + 1
                reg_z_temp[0] = new_two

            keystream.insert(i, reg_x_temp[18] ^ reg_y_temp[21] ^ reg_z_temp[22])
            i = i + 1
        return keystream


    def convert_binary_to_str(binary):
        s = ""
        length = len(binary) - 12
        i = 0
        while(i <= length):
            s = s + chr(int(binary[i:i+12], 2))
            i = i + 12
        return str(s)


    def encrypt(plain):
        s = ""
        binary = to_binary(plain)
        keystream = get_keystream(len(binary))
        i = 0
        while(i < len(binary)):
            s = s + str(binary[i] ^ keystream[i])
            i = i + 1
        return s


    def decrypt(cipher):
        s = ""
        binary = []
        keystream = get_keystream(len(cipher))
        i = 0
        while(i < len(cipher)):
            binary.insert(i, int(cipher[i]))
            s = s + str(binary[i] ^ keystream[i])
            i = i + 1
        return convert_binary_to_str(str(s))


    def user_input_key():
        tha_key = str(input('Введите 64-bit ключ: '))
        if (len(tha_key) == 64 and re.match("^([01])+", tha_key)):
            return tha_key
        else:
            while(len(tha_key) != 64 and not re.match("^([01])+", tha_key)):
                if (len(tha_key) == 64 and re.match("^([01])+", tha_key)):
                    return tha_key
                tha_key = str(input('Введите 64-bit ключ: '))
        return tha_key
    clear = ''
    encrypted = ''
    decrypted = ''
    key = '0101001000011010110001110001100100101001000000110111111010110111'
    set_key(key)
    if request.method == 'POST':
        key = request.form.get('key')
        set_key(key)
        if key == '':
            key = '0101001000011010110001110001100100101001000000110111111010110111'
            set_key(key)
        clear = request.form.get('clear')
        encrypted = request.form.get('encrypted')
        decrypted = request.form.get('decrypted')
        if clear:
            if encrypted:
                decrypted = output_from_decrypted(decrypt(encrypted))
                return render_template('lab06_16.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
            else:
                encrypted = encrypt(replace_all_to(
                    clear.lower().replace(' ', ''), dictionary))
                return render_template('lab06_16.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
        return render_template('lab06_16.html', clear_text=clear, encrypted_text=encrypted, decrypted_text=decrypted, key=key)
    else:
        return render_template('lab06_16.html', clear_text=clear_text, key = '0101001000011010110001110001100100101001000000110111111010110111')
