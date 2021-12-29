# импорт компонентов, необходимых для работы программы
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted
import random

# установка ключа
key = 5

# функция шифрования
def caesar_encode(input, step):
    return input.translate(
        str.maketrans(alphabet, alphabet[step:] + alphabet[:step]))

# функция расшифрования
def caesar_decode(input, step):
    return input.translate(
        str.maketrans(alphabet[step:] + alphabet[:step], alphabet))

#вывод результатов работы программы
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


