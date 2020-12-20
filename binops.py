from ustruct import unpack, pack
import uhashlib


def bitstring_to_bytes(bitstring):
    v = int(bitstring, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])


def num_to_nbytes(num, nbytes):
    if nbytes == 1:
        return signedchar_to_bytes(num)
    elif nbytes == 2:
        return short_to_bytes(num)
    elif nbytes == 4:
        return int_to_bytes(num)
    elif nbytes == 8:
        return long_to_bytes(num)
    raise OSError('BinOpNotImplemented')


def nbytes_to_num(_bytes, nbytes):
    if nbytes == 1:
        return bytes_to_signedchar(_bytes)
    elif nbytes == 2:
        return bytes_to_short(_bytes)
    elif nbytes == 4:
        return bytes_to_int(_bytes)
    elif nbytes == 8:
        return bytes_to_long(_bytes)
    raise OSError('BinOpNotImplemented')


def bytes_to_signedchar(_byte):
    return unpack('>b', _byte)[0]


def signedchar_to_bytes(_signedchar):
    return pack('>b', _signedchar)


def bytes_to_short(_bytes):
    return unpack('>b', _bytes)[0]


def short_to_bytes(_short):
    return pack('>b', _short)


def bytes_to_long(_bytes):  # signed int
    return unpack(">q", _bytes)[0]


def long_to_bytes(_int):  # signed int
    return pack(">q", _int)


def bytes_to_int(_bytes):  # signed int
    return unpack(">i", _bytes)[0]


def int_to_bytes(_int):  # signed int
    return pack(">i", _int)


def calculate_checksum(data):
    return uhashlib.md5(data).digest()
