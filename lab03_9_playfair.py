# импорт компонентов, необходимых для работы программы
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted

alphabet = alphabet.replace(' ', '') + 'abc'

# установка ключа
key = 'ключ'

# функция шифрования
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

# функция расшифрования
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

#вывод результатов работы программы
def main():
    print(f'''
    Шифр Плейфера:
    Ключ: {key}
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {playfair_encode(input_for_cipher_short(), key)}
    
    Расшифрованный текст:
    {output_from_decrypted(playfair_decode(playfair_encode(
        input_for_cipher_short(), key), key))}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {playfair_encode(input_for_cipher_long(), key)}
    
    Расшифрованный текст:
    {output_from_decrypted(playfair_decode(playfair_encode(
        input_for_cipher_long(), key), key))}
    ''')

if __name__ == "__main__":
    main()


