import string

ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase

def b62_encode(number, alphabet = ALPHABET):
    string = ""
    base = len(alphabet)

    if (number == 0):
        return alphabet[0]

    while number:
        remainder = number % base
        number = number // base
        string = str(alphabet[remainder]) + string

    return string

def b62_decode(string, alphabet = ALPHABET):
    number = 0
    index = 0

    base = len(alphabet)
    length = len(string)

    for char in string:
        power = (length - (index + 1))
        number += alphabet.index(char) * (base ** power)
        index += 1

    return number
