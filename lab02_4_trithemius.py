# импорт компонентов, необходимых для работы программы
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted

# функция расшифрования
def trithemius_decode(input):
    decode: str = ""
    k = 0
    for position, symbol in enumerate(input):
        index = (alphabet.find(symbol) + k) % len(alphabet)
        decode += alphabet[index]
        k -= 1
    return decode

# функция шифрования
def trithemius_encode(input):
    encode = ""
    k = 0
    for position, symbol in enumerate(input):
        index = (alphabet.find(symbol) + k) % len(alphabet)
        encode += alphabet[index]
        k += 1
    return encode

#вывод результатов работы программы
def main():
    print(f'''
    Шифр Тритемия:
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {trithemius_encode(input_for_cipher_short())}
    
    Расшифрованный текст:
    {output_from_decrypted(trithemius_decode(trithemius_encode(
        input_for_cipher_short())))}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {trithemius_encode(input_for_cipher_long())}
    
    Расшифрованный текст:
    {output_from_decrypted(trithemius_decode(trithemius_encode(
        input_for_cipher_long())))}
    ''')

if __name__ == "__main__":
    main()


