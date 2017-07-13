import argparse
import textwrap

bin2str = {
    '000000': 'A', '000001': 'B', '000010': 'C', '000011': 'D', '000100': 'E', '000101': 'F', '000110': 'G',
    '000111': 'H', '001000': 'I', '001001': 'J', '001010': 'K', '001011': 'L', '001100': 'M', '001101': 'N',
    '001110': 'O', '001111': 'P', '010000': 'Q', '010001': 'R', '010010': 'S', '010011': 'T', '010100': 'U',
    '010101': 'V', '010110': 'W', '010111': 'X', '011000': 'Y', '011001': 'Z', '011010': 'a', '011011': 'b',
    '011100': 'c', '011101': 'd', '011110': 'e', '011111': 'f', '100000': 'g', '100001': 'h', '100010': 'i',
    '100011': 'j', '100100': 'k', '100101': 'l', '100110': 'm', '100111': 'n', '101000': 'o', '101001': 'p',
    '101010': 'q', '101011': 'r', '101100': 's', '101101': 't', '101110': 'u', '101111': 'v', '110000': 'w',
    '110001': 'x', '110010': 'y', '110011': 'z', '110100': '0', '110101': '1', '110110': '2', '110111': '3',
    '111000': '4', '111001': '5', '111010': '6', '111011': '7', '111100': '8', '111101': '9', '111110': '+',
    '111111': '/'
}


def main(argv):
    parser = argparse.ArgumentParser(description='base64 encoder / decoder')
    parser.add_argument('-i', dest='input_filename', type=str)
    parser.add_argument('-o', dest='output_filename', type=str)
    parser.add_argument('-e', dest='encode', action='store_true')
    parser.add_argument('-d', dest='decode', action='store_true')

    args = parser.parse_args(argv)

    input_data = read_file(args.input_filename)

    if (not args.encode and not args.decode) or (args.encode and args.decode) or args.encode:
        result = encode(input_data)
    else:
        result = decode(input_data)

    write_file(args.output_filename, result)


def encode(data: bytes) -> bytes:
    bins = textwrap.wrap(''.join([format(b, '08b') for b in data]), 6)

    if len(bins[-1]) != 6:
        bins[-1] = bins[-1] + '0' * (6 - len(bins[-1]))

    strs = ''.join([bin2str[b] for b in bins])

    if len(strs) % 4 != 0:
        strs += '='

    return strs.encode()


def decode(data: bytes) -> bytes:
    print(data)


def read_file(filename: str) -> bytes:
    with open(filename, 'rb') as f:
        return f.read()


def write_file(filename: str, data: bytes):
    with open(filename, 'wb') as f:
        f.write(data)
