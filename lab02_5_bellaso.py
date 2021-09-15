from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted

key = str(input('Введите ключ: '))

def bellaso_decode(msg, key):
    decrypted = ''
    offset = 0
    for ix in range(len(msg)):
        if msg[ix] not in alphabet:
            output = msg[ix]
            offset += -1
        elif (alphabet.find(msg[ix])) > (len(alphabet) - (alphabet.find(key[((ix + offset) % len(key))])) - 1):
            output = alphabet[(alphabet.find(msg[ix]) - (alphabet.find(key[((ix + offset) % len(key))]))) % 33]
        else:
            output = alphabet[alphabet.find(msg[ix]) - (alphabet.find(key[((ix + offset) % len(key))]))]
        decrypted += output
    return decrypted

def bellaso_encode(msg, key):
    encoded = ''
    offset = 0
    for ix in range(len(msg)):
        if msg[ix] not in alphabet:
            output = msg[ix]
            offset += -1
        elif (alphabet.find(msg[ix])) > (len(alphabet) - (alphabet.find(key[((ix + offset) % len(key))])) - 1):
            output = alphabet[(alphabet.find(msg[ix]) + (alphabet.find(key[((ix + offset) % len(key))]))) % 33]
        else:
            output = alphabet[alphabet.find(msg[ix]) + (alphabet.find(key[((ix + offset) % len(key))]))]
        encoded += output
    return encoded

# вывод результатов работы программы
print(f'''
Шифр Тритемия:
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