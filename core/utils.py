import string

BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase

def encode(num):
    """Encodes a positive integer into a Base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]
    arr = []
    base = len(BASE62_ALPHABET)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62_ALPHABET[rem])
    arr.reverse()
    return ''.join(arr)

def decode(string):
    """Decodes a Base62 string into a positive integer."""
    base = len(BASE62_ALPHABET)
    strlen = len(string)
    num = 0
    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += BASE62_ALPHABET.index(char) * (base ** power)
        idx += 1
    return num
