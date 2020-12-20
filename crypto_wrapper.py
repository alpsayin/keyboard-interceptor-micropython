
from credentials import SECRET_KEY

try:
    from Crypto.Cipher import AES
    _enc = AES.new(SECRET_KEY, AES.MODE_ECB)
    _dec = AES.new(SECRET_KEY, AES.MODE_ECB)
except ImportError as ie:
    import ucryptolib
    _enc = ucryptolib.aes(SECRET_KEY, 1)
    _dec = ucryptolib.aes(SECRET_KEY, 1)


def is_encrypted(msg):
    return (len(msg) % 16 == 0)


def encrypt(data_bytes):
    length = len(data_bytes)
    pad_amount = (16 - ((length+2) % 16)) % 16
    padded = bytearray(2+length+pad_amount)
    padded[0] = length >> 8
    padded[1] = length & 0xFF
    padded[2:2+length] = data_bytes
    return _enc.encrypt(bytes(padded))


def decrypt(encrypted_bytes):
    padded = _dec.decrypt(bytes(encrypted_bytes))
    length = (padded[0] << 8) + padded[1]
    return padded[2:2+length]


def test(teststr=b'alp'):
    return teststr == decrypt(encrypt(teststr))
