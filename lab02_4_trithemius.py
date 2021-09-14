from base import input_for_cipher_short, input_for_cipher_long, output_from_decrypted

alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя "

def trithemius_decode(text: str, a: int = 1, b: int = 1, c: int = 1) -> str:
    decode: str = ""
    for position, symbol in enumerate(text):
        k: int = (a * position**2) + (b * position) + c
        index: int = (alphabet.find(symbol) - k) % len(alphabet)
        decode += alphabet[index]
    return decode


def trithemius_encode(text: str, a: int = 1, b: int = 1, c: int = 1) -> str:
    encode: str = ""
    for position, symbol in enumerate(text):
        k: int = (a * position**2) + (b * position) + c
        index: int = (alphabet.find(symbol) + k) % len(alphabet)
        encode += alphabet[index]
    return encode


# вывод результатов работы программы
print(f'''
Шифр Тритемия:
КОРОТКИЙ ТЕКСТ:
Зашифрованный текст:
{trithemius_encode(text=input_for_cipher_short())}

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