import binascii
from functions.settings import DEBUG_MODE


def add_header(bits, fname):
    fname_bitstr = bin(int(binascii.hexlify(fname.encode()), 16))

    if DEBUG_MODE:
        print("add_header: fname_bitstr length %d" % len(fname_bitstr))

    fname_bitstr_length_bitstr = "{0:b}".format(len(fname_bitstr) - 2)

    while len(fname_bitstr_length_bitstr) < 16:
        fname_bitstr_length_bitstr = "0" + fname_bitstr_length_bitstr

    fname_headers = fname_bitstr_length_bitstr + fname_bitstr[2:]

    header_list = []
    for char in fname_headers:
        header_list.append(char)

    payload_length_header = "{0:b}".format(len(bits))

    if DEBUG_MODE:
        print("bits in payload: %d" % len(bits))

    while len(payload_length_header) < 64:
        payload_length_header = "0" + payload_length_header

    for char in payload_length_header:
        header_list.append(char)

    total_header_length = len(header_list)

    header_list.extend(bits)

    return header_list


def decode_header(bits):
    def decode_binary_string(s):
        return ''.join(chr(int(s[i * 8:i * 8 + 8], 2)) for i in range(len(s) // 8))

    fname_length_binstr = ''.join(bits[:16])

    fname_length = int(fname_length_binstr, 2)

    if DEBUG_MODE:
        print("decode_header: fname_length: %d" % fname_length)

    fname_binstr = ''.join(bits[16:16 + fname_length])
    fname_binstr = "0" + fname_binstr

    fname = decode_binary_string(fname_binstr)

    if DEBUG_MODE:
        print("decode_header: fname: %s" % fname)

    payload_length_binstr = ''.join(bits[16 + fname_length:16 + fname_length + 64])

    payload_length = int(payload_length_binstr, 2)

    if DEBUG_MODE:
        print("decode_header: payload_length: %d" % payload_length)

    return fname, bits[16 + fname_length + 64:16 + fname_length + 64 + payload_length]
