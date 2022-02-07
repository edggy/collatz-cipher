import secrets


chars = "ùéèêàâôîïçÉ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \n" #extracted from the string library : string.printable, with some minor changes. You can add yours !
max_shift = len(chars)


def gen_key():
    return secrets.token_hex(150)

def random_between(min, max):
    rand = secrets.randbelow(max+1)
    while rand < min:
        rand = secrets.randbelow(max+1)
    return rand

def gen_noise():
    noise = ''
    for i in range(random_between(10**2, 10**3)):
        noise += secrets.choice(chars)
    return noise

def collatz_sequence(n):
    sequence = [n]
    while n != 1:
        n = 3 * n + 1 if n & 1 else n // 2
        sequence.append(n)
    
    return sequence

def modified_collatz_sequence(key, size):
    seq = collatz_sequence(key)
    output = [x % max_shift for x in seq if not x & 1]
    if len(output) < size:
        output = (size // len(output) + 1) * output
    return output[0:size]

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
    keys = modified_collatz_sequence(key, len(plaintext) + 10**4)
    plaintext = gen_noise() + 'BEGINREALMESSAGE' + plaintext
    ciphertext = ''

    for i in range(len(plaintext)):
        ciphertext += encode(plaintext[i], keys[i])

    return ciphertext

def decrypt_str(ciphertext, key):
    keys = modified_collatz_sequence(key, len(ciphertext) + 10**4)
    plaintext = ''

    for i in range(len(ciphertext)):
        plaintext += decode(ciphertext[i], keys[i])
    
    try:
        return plaintext.split('BEGINREALMESSAGE')[1]
    except Exception:
        return "Invalid input or key."

message = "The cake is a lie."
print(f"Message is : {message}")
print()

str_key = gen_key()
key = int(str_key, 16)
print("The key is : ")
print(str_key)
print()

cipher = encrypt_str(message, key)
deciphered = decrypt_str(cipher, key)

print(f"Encrypted message is : {cipher}")
print()
print(f"Decrypted message is : {deciphered}")
print(f"Match with original message ? {deciphered == message}")
