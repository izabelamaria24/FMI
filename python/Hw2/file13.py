def encode_caesar_cypher(plain_text, en_shift):
    res = ""
    for ch in plain_text:
        if ch.isalpha():
            upper = ch.isupper()
            ch = ch.lower()

            shifted_ch = chr((ord(ch) - ord('a') + en_shift) % 26 + ord('a'))

            if upper:
                shifted_ch.upper()
            res += shifted_ch
        else:
            res += ch
    return res


def decode_caesar_cypher(cypher, en_shift):
    return encode_caesar_cypher(cypher, -en_shift)

text = input()
shift = int(input())

encoded = encode_caesar_cypher(text, shift)
print(f'Encoded text: {encoded}')
decoded = decode_caesar_cypher(encoded, shift)
print(f'Decoded text: {decoded}')