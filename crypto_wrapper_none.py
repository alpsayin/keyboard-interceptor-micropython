

def is_encrypted(msg):
    return True


def encrypt(data_bytes):
    return data_bytes


def decrypt(encrypted_bytes):
    return encrypted_bytes


def test(teststr=b'alp'):
    return teststr == decrypt(encrypt(teststr))
