from collatzcipher import *

message = """The cake is a lie.
Let's test some weird characters : !/;?,$"""
print(f"Message is : {message}")
print()

str_key = gen_key(10, default_charset)
key = to_key_object(str_key)
print("The key is : ")
print(str_key)
print()

cipher = encrypt_str(message, key)
deciphered = decrypt_str(cipher, key)

print(f"Encrypted message is :")
print(cipher)
print()

print(f"Decrypted message is :")
print(deciphered)
print(f"Match with original message ? {deciphered == message}")