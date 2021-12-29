# импорт компонентов, необходимых для работы программы
from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted
import numpy as np
from egcd import egcd

# установка ключа
key1 = '3 10 20 20 19 17 23 78 17'
inp = key1.split(' ')
key = np.matrix([[int(inp[0]), int(inp[1]), int(inp[2])], [int(inp[3]), int(inp[4]), int(inp[5])], [int(inp[6]), int(inp[7]), int(inp[8])]])

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))

# функция вычисления обратной матрицы
def matrix_mod_inv(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = egcd(det, modulus)[1] % modulus
    matrix_modulus_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )

    return matrix_modulus_inv

# функция шифрования
def matrix_encode(message, K):
    # проверка на определитель равный 0
    if np.linalg.det(K) == 0:
        raise ValueError('Определитель матрицы равен 0! Дальнейшая работа программы невозможна!')
    
    encrypted = ""
    message_in_numbers = []
    for letter in message:
        message_in_numbers.append(letter_to_index[letter])

    split_P = [
        message_in_numbers[i: i + int(K.shape[0])]
        for i in range(0, len(message_in_numbers), int(K.shape[0]))
    ]

    for P in split_P:
        P = np.transpose(np.asarray(P))[:, np.newaxis]

        while P.shape[0] != K.shape[0]:
            P = np.append(P, letter_to_index[" "])[:, np.newaxis]

        numbers = np.dot(K, P) % len(alphabet)
        n = numbers.shape[0]

        for idx in range(n):
            number = int(numbers[idx, 0])
            encrypted += index_to_letter[number]
    return encrypted

# функция расшифрования
def matrix_decode(cipher, Kinv):
    decrypted = ""
    cipher_in_numbers = []
    for letter in cipher:
        cipher_in_numbers.append(letter_to_index[letter])

    split_C = [
        cipher_in_numbers[i: i + int(Kinv.shape[0])]
        for i in range(0, len(cipher_in_numbers), int(Kinv.shape[0]))
    ]

    for C in split_C:
        C = np.transpose(np.asarray(C))[:, np.newaxis]
        numbers = np.dot(Kinv, C) % len(alphabet)
        n = numbers.shape[0]

        for idx in range(n):
            number = int(numbers[idx, 0])
            decrypted += index_to_letter[number]
    return decrypted

#вывод результатов работы программы
def main():
    print(f'''
    Матричный шифр:
    Ключ: {key1}
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {matrix_encode(input_for_cipher_short(), key).replace(' ', '')}
    
    Расшифрованный текст:
    {output_from_decrypted(matrix_decode(matrix_encode(
        input_for_cipher_short(), key), matrix_mod_inv(key, len(alphabet)))).replace(' ', '')}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {matrix_encode(input_for_cipher_long(), key).replace(' ', '')}
    
    Расшифрованный текст:
    {output_from_decrypted(matrix_decode(matrix_encode(
        input_for_cipher_long(), key), matrix_mod_inv(key, len(alphabet)))).replace(' ', '')}
    ''')

if __name__ == "__main__":
    main()


