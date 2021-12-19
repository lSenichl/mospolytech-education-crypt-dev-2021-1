from base import alphabet, input_for_cipher_short, input_for_cipher_long, output_from_decrypted

hard_dictionary = {"а": "11", "б": "12", "в": "13",
                   "г": "14", "д": "15", "е": "16", "ё": "21",
                   "ж": "22", "з": "23", "и": "24", "й": "25",
                   "к": "26", "л": "31", "м": "32", "н": "33",
                   "о": "34", "п": "35", "р": "36", "с": "41",
                   "т": "42", "у": "43", "ф": "44", "х": "45",
                   "ц": "46", "ч": "51", "ш": "52", "щ": "53",
                   "ъ": "54", "ы": "55", "ь": "56", "э": "61",
                   "ю": "62", "я": "63"}


def square_encode(input):
    new_txt = ""
    for x in input:
        if x in hard_dictionary:
            new_txt += hard_dictionary.get(x)
        else:
            new_txt += (x + x)
    return new_txt


def square_decode(input):
    new_txt = ""
    list_fraze = []
    step = 2
    for i in range(0, len(input), 2):
        list_fraze.append(input[i:step])
        step += 2
    key_hard_dictionary_list = list(hard_dictionary.keys())
    val_hard_dictionary_list = list(hard_dictionary.values())

    for x in list_fraze:
        if x in val_hard_dictionary_list:
            i = val_hard_dictionary_list.index(x)
            new_txt += key_hard_dictionary_list[i]
        else:
            new_txt += x[0:1]
    return new_txt


def main():
    print(f'''
    КВАДРАТ ПОЛИБИЯ:
    Ключ: {hard_dictionary}
    КОРОТКИЙ ТЕКСТ:
    Зашифрованный текст:
    {square_encode(input_for_cipher_short())}
    
    Расшифрованный текст:
    {output_from_decrypted(square_decode(square_encode(
        input_for_cipher_short())))}
    
    ДЛИННЫЙ ТЕКСТ:
    Зашифрованный текст:
    {square_encode(input_for_cipher_long())}
    
    Расшифрованный текст:
    {output_from_decrypted(square_decode(square_encode(
        input_for_cipher_long())))}
    ''')

if __name__ == "__main__":
    main()


