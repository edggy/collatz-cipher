import secrets


#extracted from the string library : string.printable, with some minor changes. You can add yours ! Be careful with the \ char, however,
#and some other chars that may be used by Python, causing some errors/unexpected behaviour.
default_charset = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
ùéèêàâôîïçÉ !"#$%&'()*+,-./:;<=>?@[]^_`{|}~"""

#exists as the message/key formatting implies to add new lines, and both may contain new lines too.
new_line_replacement_char = '§'

max_shift = len(default_charset)


def format_key(charset, hexkey):
    one_line_key = f"CHARSET:{charset}KEY:{hexkey.upper()}".replace('\n', new_line_replacement_char)
    key = ''
    k = 64
    for i in range(0, len(one_line_key), k):
        key += one_line_key[i:i+k] + '\n'
    
    return '-----BEGIN COLLATTZ CIPHER KEY BLOCK-----\n' + key + '-----END COLLATTZ CIPHER KEY BLOCK-----'

def format_message(unformated_ciphertext):
    unformated_ciphertext = unformated_ciphertext.replace('\n', new_line_replacement_char)

    ciphertext = ''
    k = 64
    for i in range(0, len(unformated_ciphertext), k):
        ciphertext += unformated_ciphertext[i:i+k] + '\n'

    return '-----BEGIN COLLATTZ CIPHER MESSAGE-----\n' + ciphertext + '-----END COLLATTZ CIPHER MESSAGE-----'

def unformat_message(formated_ciphertext):
    ciphertext = formated_ciphertext
    words = ['-----BEGIN COLLATTZ CIPHER MESSAGE-----', '-----END COLLATTZ CIPHER MESSAGE-----', '\n']
    for word in words:
        ciphertext = ciphertext.replace(word, '')

    return ciphertext.replace(new_line_replacement_char, '\n')


def permutation(str_input: str):
    l = len(str_input)
    str_input = list(str_input)
    str_output = ""

    for i in range(l):
        ind = secrets.randbelow(len(str_input))
        str_output += str_input[ind]
        del str_input[ind]

    return str_output

def gen_key(nbytes, charset):
    return format_key(permutation(charset), secrets.token_hex(nbytes))

def to_key_object(str_key):
    str_key = str_key.replace('-----BEGIN COLLATTZ CIPHER KEY BLOCK-----', '').replace('-----END COLLATTZ CIPHER KEY BLOCK-----', '').replace('\n', '').replace('CHARSET:', '')
    try:
        key_obj = {
            'charset': str_key.split('KEY:')[0].replace(new_line_replacement_char, '\n'),
            'key': int(str_key.split('KEY:')[1], 16)
        }
        return key_obj
    except Exception:
        return None


def random_between(min, max):
    rand = secrets.randbelow(max+1)
    while rand < min:
        rand = secrets.randbelow(max+1)
    return rand

def gen_noise(charset):
    noise = ''
    for i in range(random_between(100, 1000)):
        noise += secrets.choice(charset)
    return noise


def collatz_sequence(n):
    sequence = [n]
    while n != 1:
        n = 3 * n + 1 if n & 1 else n // 2
        sequence.append(n)
    
    return sequence

def modified_collatz_sequence(int_key, size):
    seq = collatz_sequence(int_key)
    output = [x % max_shift for x in seq if not x & 1]
    if len(output) < size:
        output = (size // len(output) + 1) * output
    return output[0:size]


def encode(char, charset, int_subkey):
    try:
        result = charset.index(char) + 1
    except ValueError:
        print("Missing char in chars var : " + char)

    result += int_subkey
    if result > max_shift:
        result %= max_shift

    return charset[result-1]

def decode(char, charset, int_subkey):
    try:
        result = charset.index(char) + 1
    except ValueError:
        print(f"Missing char in chars var : {char} (ord : {ord(char)})")

    result = result - int_subkey % max_shift
    if result < 0:
        result += max_shift

    return charset[result - 1]

def encrypt_str(plaintext, key_object):
    plaintext = gen_noise(key_object['charset']) + 'BEGINREALMESSAGE' + plaintext + 'ENDREALMESSAGE' + gen_noise(key_object['charset'])
    keys = modified_collatz_sequence(key_object['key'], len(plaintext))
    unformated_ciphertext = ''

    for i in range(len(plaintext)):
        unformated_ciphertext += encode(plaintext[i], key_object['charset'], keys[i])

    return format_message(unformated_ciphertext)

def decrypt_str(formated_ciphertext, key_object):
    ciphertext = unformat_message(formated_ciphertext)
    keys = modified_collatz_sequence(key_object['key'], len(ciphertext))
    plaintext = ''

    for i in range(len(ciphertext)):
        plaintext += decode(ciphertext[i], key_object['charset'], keys[i])

    try:
        return plaintext.split('BEGINREALMESSAGE')[1].split('ENDREALMESSAGE')[0]
    except Exception:
        return plaintext
