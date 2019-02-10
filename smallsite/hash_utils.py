from django.contrib.auth.hashers import PBKDF2PasswordHasher


def hash_password(password):
    hasher = PBKDF2PasswordHasher()
    password = hasher.encode(password=password, salt='GAm3u8cLS5', iterations=24000)
    return password

