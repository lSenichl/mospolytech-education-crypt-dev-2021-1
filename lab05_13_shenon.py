# импорт компонентов, необходимых для работы программы
import random
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted

alphabet = alphabet.replace(' ', '')
alphabet_lower = {}
i = 0
while i < (len(alphabet)):
    alphabet_lower.update({alphabet[i]: i})
    i += 1

# фунция получения ключа
def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

# функция шифрования
def shenon_encode(msg):
    msg_list = list(msg)
    msg_list_len = len(msg_list)
    msg_code_bin_list = list()
    for i in range(len(msg_list)):
        msg_code_bin_list.append(alphabet_lower.get(msg_list[i]))

    key_list = list()
    for i in range(msg_list_len):
        key_list.append(random.randint(0, 32))

    cipher_list = list()
    for i in range(msg_list_len):
        m = int(msg_code_bin_list[i])
        k = int(key_list[i])
        cipher_list.append(int(bin(m ^ k), base=2))
    return cipher_list, key_list

# функция расшифрования
def shenon_decode(msg, key_list):
    decipher_list = list()
    msg_list_len = len(msg)
    for i in range(msg_list_len):
        c = int(msg[i])
        k = int(key_list[i])
        decipher_list.append(int(bin(c ^ k), base=2))
    deciphered_str = ""
    for i in range(len(decipher_list)):
        deciphered_str += get_key(alphabet_lower, decipher_list[i])
    return deciphered_str


short_encoded = shenon_encode(input_for_cipher_short())
short_decoded = shenon_decode(short_encoded[0], short_encoded[1])

long_encoded = shenon_encode(input_for_cipher_long())
long_decoded = shenon_decode(long_encoded[0], long_encoded[1])

#вывод результатов работы программы
def main():
    print(f'''
    Одноразовый блокнот:
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {short_encoded[0]}
    Ключ:
    {short_encoded[1]}
    
    Расшифрованный текст:
    {output_from_decrypted(short_decoded)}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {long_encoded[0]}
    Ключ:
    {long_encoded[1]}
    
    Расшифрованный текст:
    {output_from_decrypted(long_decoded)}
    ''')

if __name__ == "__main__":
    main()

