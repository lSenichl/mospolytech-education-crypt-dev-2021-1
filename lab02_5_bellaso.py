# импорт компонентов, необходимых для работы программы
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted

# установка ключа
key = 'ключ'

# функция расшифрования
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

# функция шифрования
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

#вывод результатов работы программы
def main():
    print(f'''
    Шифр Белазо:
    Ключ: {key}
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {bellaso_encode(input_for_cipher_short(), key)}
    
    Расшифрованный текст:
    {output_from_decrypted(bellaso_decode(bellaso_encode(
        input_for_cipher_short(), key), key))}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {bellaso_encode(input_for_cipher_long(), key)}
    
    Расшифрованный текст:
    {output_from_decrypted(bellaso_decode(bellaso_encode(
        input_for_cipher_long(), key), key))}
    ''')

if __name__ == "__main__":
    main()


