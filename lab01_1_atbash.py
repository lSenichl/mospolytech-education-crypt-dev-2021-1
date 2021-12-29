# импорт компонентов, необходимых для работы программы
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted

# функция шифрования/расшифрования
def atbash(input):
    return input.translate(str.maketrans(
        alphabet + alphabet.upper(), alphabet[::-1] + alphabet.upper()[::-1]))

#вывод результатов работы программы
def main():
    print(f'''
    ШИФР АТБАШ:
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {atbash(input_for_cipher_short())}
    
    Расшифрованный текст:
    {output_from_decrypted(atbash(atbash(input_for_cipher_short())))}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {atbash(input_for_cipher_long())}
    
    Расшифрованный текст:
    {output_from_decrypted(atbash(atbash(input_for_cipher_long())))}
    ''')

if __name__ == "__main__":
    main()


