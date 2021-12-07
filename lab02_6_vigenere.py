from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted

key = 'ключ'


def vigenere_encode(input, key):
    enc_string = ''
    string_length = len(input)

    expanded_key = key
    expanded_key_length = len(expanded_key)

    while expanded_key_length < string_length:
        expanded_key = expanded_key + key
        expanded_key_length = len(expanded_key)

    key_position = 0

    for letter in input:
        if letter in alphabet:
            position = alphabet.find(letter)

            key_character = expanded_key[key_position]
            key_character_position = alphabet.find(key_character)
            key_position = key_position + 1

            new_position = position + key_character_position
            if new_position >= 33:
                new_position = new_position - 33
            new_character = alphabet[new_position]
            enc_string = enc_string + new_character
        else:
            enc_string = enc_string + letter
    return(enc_string)


def vigenere_decode(input, key):
    dec_string = ''
    string_length = len(input)

    expanded_key = key
    expanded_key_length = len(expanded_key)

    while expanded_key_length < string_length:
        expanded_key = expanded_key + key
        expanded_key_length = len(expanded_key)

    key_position = 0

    for letter in input:
        if letter in alphabet:
            position = alphabet.find(letter)

            key_character = expanded_key[key_position]
            key_character_position = alphabet.find(key_character)
            key_position = key_position + 1

            new_position = position - key_character_position
            if new_position >= 33:
                new_position = new_position + 33
            new_character = alphabet[new_position]
            dec_string = dec_string + new_character
        else:
            dec_string = dec_string + letter
    return(dec_string)


print(f'''
Шифр Вижинера:
Ключ: {key}
КОРОТКИЙ ТЕКСТ:
Зашифрованный текст:
{vigenere_encode(input_for_cipher_short(), key)}

Расшифрованный текст:
{output_from_decrypted(vigenere_decode(vigenere_encode(
    input_for_cipher_short(), key), key))}

ДЛИННЫЙ ТЕКСТ:
Зашифрованный текст:
{vigenere_encode(input_for_cipher_long(), key)}

Расшифрованный текст:
{output_from_decrypted(vigenere_decode(vigenere_encode(
    input_for_cipher_long(), key), key))}
''')
