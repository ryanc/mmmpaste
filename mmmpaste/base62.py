import string

ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase

# Derived from: http://stackoverflow.com/a/1119769

def b62_encode(number, alphabet = ALPHABET):
    """
    Convert a base 10 number into Base 62.

    Keyword arguments:
    number - the base 10 number
    alphabet - the base 62 alphabet

    """
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
    """
    Convert a base 62 number into Base 10.

    Keyword arguments:
    string - the base 62 number
    alphabet - the base 62 alphabet

    """
    number = 0
    index = 0

    base = len(alphabet)
    length = len(string)

    for char in string:
        power = (length - (index + 1))
        number += alphabet.index(char) * (base ** power)
        index += 1

    return number
