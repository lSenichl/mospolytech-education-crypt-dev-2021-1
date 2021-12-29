# импорт компонентов, необходимых для работы программы
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted
import math

# установка ключа
key = 'ключ'

# функция шифрования
def transposition_encode(msg, key):
    cipher = ""

    k_indx = 0

    msg_len = float(len(msg))
    msg_lst = list(msg)
    key_lst = sorted(list(key))

    col = len(key)

    row = int(math.ceil(msg_len / col))

    fill_null = int((row * col) - msg_len)
    msg_lst.extend('_' * fill_null)

    matrix = [msg_lst[i: i + col] for i in range(0, len(msg_lst), col)]

    for _ in range(col):
        curr_idx = key.index(key_lst[k_indx])
        cipher += ''.join([row[curr_idx] for row in matrix])
        k_indx += 1

    return cipher

# функция расшифрования
def transposition_decode(cipher, key):
    msg = ""

    k_indx = 0

    msg_indx = 0
    msg_len = float(len(cipher))
    msg_lst = list(cipher)

    col = len(key)

    row = int(math.ceil(msg_len / col))

    key_lst = sorted(list(key))

    dec_cipher = []
    for _ in range(row):
        dec_cipher += [[None] * col]

    for _ in range(col):
        curr_idx = key.index(key_lst[k_indx])

        for j in range(row):
            dec_cipher[j][curr_idx] = msg_lst[msg_indx]
            msg_indx += 1
        k_indx += 1

    null_count = msg.count('_')

    if null_count > 0:
        return msg[: -null_count]

    msg = ''.join(sum(dec_cipher, []))

    return msg.replace('_', '')

#вывод результатов работы программы
def main():
    print(f'''
    Шифр вертикальной перестановки:
    Ключ: {key}
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {transposition_encode(input_for_cipher_short(), key)}
    
    Расшифрованный текст:
    {output_from_decrypted(transposition_decode(transposition_encode(
        input_for_cipher_short(), key), key))}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {transposition_encode(input_for_cipher_long(), key)}
    
    Расшифрованный текст:
    {output_from_decrypted(transposition_decode(transposition_encode(
        input_for_cipher_long(), key), key))}
    ''')

if __name__ == "__main__":
    main()


