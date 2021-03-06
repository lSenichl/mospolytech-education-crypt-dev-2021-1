# -*- coding:utf-8 -*-
# импорт компонентов, необходимых для работы программы
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted
import random

# функция вычисления НОД
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# функция получения обратного числа
def multiplicative_inverse(e, r):
    for i in range(r):
        if((e*i) % r == 1):
            return i

# функция проверки числа на простоту
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

# функция генерации пары ключей
def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Оба числа должны быть простыми.')
    elif p == q:
        raise ValueError('p и q не могут быть равны друг другу')
    n = p * q

    phi = (p-1) * (q-1)

    e = random.randrange(1, phi)

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))

# функция шифрования
def encrypt(pk, plaintext):
    key, n = pk
    cipher = [(ord(char) ** key) % n for char in plaintext]
    return cipher

# функция расшифрования
def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)

# установка ключа
p = 31
q = 37
public, private = generate_keypair(p, q)

message_short = input_for_cipher_short()
encrypted_short = encrypt(private, message_short)
print_enc_short = ''.join([str(x) for x in encrypted_short])
decrypted_short = decrypt(public, encrypted_short)

message_long = input_for_cipher_long()
encrypted_long = encrypt(private, message_long)
print_enc_long = ''.join([str(x) for x in encrypted_long])
decrypted_long = decrypt(public, encrypted_long)

#вывод результатов работы программы
def main():
    print(f'''
    RSA:
    Ключ: 
    p={p} q={q}
    Публичный: {public}
    Приватный: {private}
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {encrypted_short}
    {print_enc_short}
    
    Расшифрованный текст:
    {output_from_decrypted(decrypted_short)}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {print_enc_long}
    
    Расшифрованный текст:
    {output_from_decrypted(decrypted_long)}
    ''')

if __name__ == "__main__":
    main()
    

