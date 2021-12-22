import random
from math import pow
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted

a = random.randint(2, 10)

def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


def gen_key(q):
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)
    return key


def power(a, b, c):
    x = 1
    y = a
    while b > 0:
        if b % 2 == 0:
            x = (x*y) % c
        y = (y*y) % c
        b = int(b/2)
    return x % c


def encryption(msg, q, h, g):
    ct = []
    k = gen_key(q)
    s = power(h, k, q)
    p = power(g, k, q)
    for i in range(0, len(msg)):
        ct.append(msg[i])
    for i in range(0, len(ct)):
        ct[i] = s*ord(ct[i])
    return ct, p


def decryption(ct, p, key, q):
    pt = []
    h = power(p, key, q)
    for i in range(0, len(ct)):
        pt.append(chr(int(ct[i]/h)))
    return pt


msg_short = input_for_cipher_short()
msg_long = input_for_cipher_long()
p = random.randint(pow(10, 20), pow(10, 30))
x = random.randint(2, p)
g = gen_key(p)
y = power(x, g, p)

ct_sh, pp_sh = encryption(msg_short, p, y, x)
pt_sh = decryption(ct_sh, pp_sh, g, p)
d_msg_sh = ''.join(pt_sh)

ct_ln, pp_ln = encryption(msg_long, p, y, x)
pt_ln = decryption(ct_ln, pp_ln, g, p)
d_msg_ln = ''.join(pt_ln)


def main():
    print(f'''
    Elgamal:
    Ключ: 
    p={p} x={x} g={g} y={y}
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {ct_sh}
    
    Расшифрованный текст:
    {output_from_decrypted(d_msg_sh)}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {ct_ln}
    
    Расшифрованный текст:
    {output_from_decrypted(d_msg_ln)}
    ''')

if __name__ == "__main__":
    main()

    

