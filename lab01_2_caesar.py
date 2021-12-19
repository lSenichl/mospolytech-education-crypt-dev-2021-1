from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted
import random

key = 5


def caesar_encode(input, step):
    return input.translate(
        str.maketrans(alphabet, alphabet[step:] + alphabet[:step]))


def caesar_decode(input, step):
    return input.translate(
        str.maketrans(alphabet[step:] + alphabet[:step], alphabet))


def main():
    print(f'''
    ШИФР ЦЕЗАРЯ:
    Ключ: {key}
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {caesar_encode(input_for_cipher_short(), key)}
    
    Расшифрованный текст:
    {output_from_decrypted(caesar_decode(caesar_encode(
        input_for_cipher_short(), key), key))}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {caesar_encode(input_for_cipher_long(), key)}
    
    Расшифрованный текст:
    {output_from_decrypted(caesar_decode(caesar_encode(
        input_for_cipher_long(), key), key))}
    ''')

if __name__ == "__main__":
    main()


