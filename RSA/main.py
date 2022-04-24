from Crypto.Util import number
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
from functools import reduce
import cryptools
from cryptools import rsa
from cryptools import rsa_decrypt
from cryptools import rsa_encrypt


def chinese_remainder(n, a):
    sum_ = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum_ += a_i * mul_inv(p, n_i) * p
    return sum_ % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def gcd(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def coprimes(a):
    l = []
    for x in range(2, a):e
        if gcd(a, x) == 1 and modinv(x, phi) != None:
            l.append(x)
    for x in l:
        if x == modinv(x, phi):
            l.remove(x)
    return l


def encrypt_block(m):
    c = modinv(m ** e, n)
    if c is None:
        print('No modular multiplicative inverse for block ' + str(m) + '.')
    return c


def decrypt_block(c):
    # m = modinv(c ** d, n)
    n1 = [p, q, r]
    a = [pow(c,d,n), pow(c,d,n), pow(c,d,n)]
    m = chinese_remainder(n1, a)
    print(m)
    if m is None:
        print('No modular multiplicative inverse for block ' + str(c) + '.')
    return m


def encrypt_string(s):
    return ''.join([chr(encrypt_block(ord(x))) for x in list(s)])


def decrypt_string(s):
    return ''.join([chr(decrypt_block(ord(x))) for x in list(s)])


if __name__ == '__main__':
    p = int(input('Enter prime p: '))
    q = int(input('Enter prime q: '))
    r = int(input('Enter prime r: '))
    print("Choosen primes:\np=" + str(p) + ", q=" + str(q) + ", r=" + str(r) + "\n")
    n = p * q * r
    print("n = p * q * r = " + str(n) + "\n")
    phi = (p - 1) * (q - 1) * (r - 1)
    print("Euler's function (totient) [phi(n)]: " + str(phi) + "\n")

    print("Choose an e from a below coprimes array:\n")
    print(str(coprimes(phi)) + "\n")
    e = int(input())
    d = modinv(e, phi)
    print("\nYour public key is a pair of numbers (e=" + str(e) + ", n=" + str(n) + ").\n")
    print("Your private key is a pair of numbers (d=" + str(d) + ", n=" + str(n) + ").\n")

    s = input("Enter a message to encrypt: ")
    print("\nPlain message: " + s + "\n")
    enc = encrypt_string(s)
    print("Encrypted message: " + enc + "\n")
    dec = decrypt_string(enc)
    print("Decrypted message: " + dec + "\n")
    # n_length = 512
    # p = number.getPrime(512)
    # q = number.getPrime(512)
    # r = number.getPrime(512)
    # e = 65537
    # n = p * q * r
    # d = modinv(e, n)
    # message = 7
    # crypto_text = pow(7, d, p)
    # print(crypto_text)
    #
    # print(message ** d)
    # print(message ** d % p)
    # print(message ** d % q)
    # print(message ** d % r)
    #
    # n1 = [p, q, r]
    # a = [message ** d % p, message ** d % q, message ** d % r]
    # print("TRUE NUMBER : ", message ** d % n)
    # print("NUMBER      : ", chinese_remainder(n1, a))
    #
    # print(f" P: {p}\n Q: {q}\n R: {r}\n N:{n}\n")
    #
    # keyPair = RSA.generate(1024)

    # print(keyPair.p, keyPair.e, keyPair.d, keyPair.q, keyPair.n)
    #
    # pubKey = keyPair.publickey()
    # print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
    # pubKeyPEM = pubKey.exportKey()
    # print(pubKeyPEM.decode('ascii'))
    #
    # print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
    # privKeyPEM = keyPair.exportKey()
    # print(privKeyPEM.decode('ascii'))
    #
    # msg = (10).to_bytes(2, "little")
    # print(msg)
    # encryptor = PKCS1_OAEP.new(pubKey)
    # encrypted = encryptor.encrypt(msg)
    # print("Encrypted:", binascii.hexlify(encrypted))
    #
    # decryptor = PKCS1_OAEP.new(keyPair)
    # decrypted = decryptor.decrypt(encrypted)
    # print(int.from_bytes(encrypted, "little"))
    # print('Decrypted:', int.from_bytes(decrypted, "little"))

