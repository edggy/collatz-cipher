chars = "ùéèêàâôîïçÉ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \n" #extracted from the string library : string.printable, with some minor changes.
max_shift = len(chars)

def collatz_sequence(n, steps):
    sequence = [n]
    i = 1
    while n != 1 and i < steps:
        n = 3 * n + 1 if n & 1 else n // 2
        sequence.append(n)
        i += 1

    if len(sequence) < steps:
        return ((steps // len(sequence)) + 1) * sequence    

    return sequence

def encode(char, key):
    try:
        result = chars.index(char) + 1
    except ValueError:
        print("Missing char in chars var : " + char)

    result += key
    if result > max_shift:
        result %= max_shift

    return chars[result-1]

def decode(char, key):
    try:
        result = chars.index(char) + 1
    except ValueError:
        print("Missing char in chars var : " + char)

    result = result - key % max_shift
    if result < 0:
        result += max_shift

    return chars[result - 1]

def encrypt_str(plaintext, key):
    keys = collatz_sequence(key, len(plaintext))
    ciphertext = ''

    for i in range(len(plaintext)):
        ciphertext += encode(plaintext[i], keys[i])

    return ciphertext

def decrypt_str(ciphertext, key):
    keys = collatz_sequence(key, len(ciphertext))
    plaintext = ''

    for i in range(len(ciphertext)):
        plaintext += decode(ciphertext[i], keys[i])

    return plaintext


message = "The bird is purple."
key = 2*210-91
cipher = encrypt_str(message, key)
print(cipher)
deciphered = decrypt_str(cipher, key)
print(deciphered)
print(message == deciphered)