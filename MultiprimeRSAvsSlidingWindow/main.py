import warnings
from Cryptodome.Util import number
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from sympy import *
    from sympy import crypto
    from sympy.crypto import rsa_public_key
    from sympy.crypto import rsa_private_key
    from sympy.crypto import encipher_rsa
    from sympy.crypto import decipher_rsa
from sympy import randprime

import time


def tcr_garner(m, v):
    c = [0]*len(v)
    t = len(v)
    # print(c)
    # print(m)
    # print(v)
    for i in range(0, t):
        c[i] = 1
        for j in range(0, i):
            u = pow(m[j], -1, m[i])
            c[i] = (u*c[i]) % m[i]
    u = v[0]
    x = u
    # print("C:", c)
    for i in range(1, t):
        # print(i, u, x)
        u = ((v[i] - x)*c[i]) % m[i]
        for j in range(0, i):
            u *= m[j]
        x = x + u
    return x


def part1(bits=512, print_lines=False):
    if print_lines:
        p = number.getPrime(bits)
        q = number.getPrime(bits)
        r = number.getPrime(bits)
        e = 65537
        print("P: ", p)
        print("Q: ", q)
        print("R: ", r)
        public_key = rsa_public_key(p, q, r, e, totient='Euler')
        print(f"Public Key:\nn={public_key[0]}\ne={public_key[1]}  ")
        private_key = rsa_private_key(p, q, r, e, totient='Euler')
        print(f"Private Key:\nn={private_key[0]}\nd={private_key[1]}")

        message = 42935
        print("Message:        ", message)
        y = encipher_rsa(message, public_key, factors=[p, q, r])
        print("Ciphertext:     ", y)

        start = time.time_ns()
        decrypted_message = decipher_rsa(y, private_key, factors=[p, q, r])
        finish = time.time_ns() - start

        print("Decrypted Text: ", decrypted_message)
        print("Time used by library decryption:   ", finish*10**-9, "seconds")

        start1 = time.time_ns()
        d = private_key[1]
        dP = d % (p - 1)
        dQ = d % (q - 1)
        dR = d % (r - 1)
        x_p = pow(y % p, dP, p)
        x_q = pow(y % q, dQ, q)
        x_r = pow(y % r, dR, r)
        decrypted_message2 = tcr_garner([p, q, r],
                                        [x_p, x_q, x_r])
        finish1 = time.time_ns() - start1
        print("TCR Decrypted Text: ", decrypted_message2)
        print("Time used by TCR Garner decryption:", finish1*10**-9, "seconds")

    p = number.getPrime(bits)
    q = number.getPrime(bits)
    r = number.getPrime(bits)
    e = 65537
    public_key = rsa_public_key(p, q, r, e, totient='Euler')
    private_key = rsa_private_key(p, q, r, e, totient='Euler')

    message = 42935
    y = encipher_rsa(message, public_key)

    start = time.time_ns()
    decrypted_message = decipher_rsa(y, private_key)
    finish = time.time_ns() - start

    start1 = time.time_ns()
    d = private_key[1]
    dP = d % (p - 1)
    dQ = d % (q - 1)
    dR = d % (r - 1)
    x_p = pow(y % p, dP, p)
    x_q = pow(y % q, dQ, q)
    x_r = pow(y % r, dR, r)
    decrypted_message2 = tcr_garner([p, q, r],
                                    [x_p, x_q, x_r])
    finish1 = time.time_ns() - start1
    return tuple((finish*10**-9, finish1*10**-9))


def part2(bits=512, print_lines = False):
    if print_lines:
        p = number.getPrime(bits)
        q = number.getPrime(bits)
        e = 65537
        print("P: ", p)
        print("Q: ", q)
        public_key = rsa_public_key(p*p, q, e, totient='Euler')
        print(f"Public Key:\nn={public_key[0]}\ne={public_key[1]}  ")
        private_key = rsa_private_key(p*p, q, e, totient='Euler')
        print(f"Private Key:\nn={private_key[0]}\nd={private_key[1]}")

        message = 42
        print("Message:        ", message)
        y = encipher_rsa(message, public_key, factors=[p*p, q])
        print("Ciphertext:     ", y)

        start = time.time_ns()
        decrypted_message = decipher_rsa(y, private_key, factors=[p*p, q])
        finish = time.time_ns() - start

        print("Decrypted Text: ", decrypted_message)
        print("Time used by library decryption:   ", finish*10**-9, "seconds")

        # lema lui Hensel
        start1 = time.time_ns()
        d = private_key[1]
        dP = d % (p - 1)
        dQ = d % (q - 1)
        x_q = pow(y % q, dQ, q)
        x_0 = pow(y % p, dP, p)
        p2 = p*p
        # print((y-pow(x_0, e, p2))/p)
        x_1 = (((y - pow(x_0, e, p2)) * e * pow(pow(x_0, e - 1, p2) % p, -1, p)) // p) % p
        x_p2 = x_1*p + x_0

        decrypted_message2 = tcr_garner([p*p, q],
                                        [x_p2, x_q])
        finish1 = time.time_ns() - start1
        print("TCR Decrypted Text: ", decrypted_message2)
        print("Time used by TCR Garner decryption:", finish1*10**-9, "seconds")
    else:
        p = number.getPrime(bits)
        q = number.getPrime(bits)
        e = 65537
        public_key = rsa_public_key(p*p, q, e, totient='Euler')
        private_key = rsa_private_key(p*p, q, e, totient='Euler')
        message = 42
        y = encipher_rsa(message, public_key, factors=[p*p, q])

        start = time.time_ns()
        decrypted_message = decipher_rsa(y, private_key, factors=[p*p, q])
        finish = time.time_ns() - start

        # lema lui Hensel
        start1 = time.time_ns()
        d = private_key[1]
        dP = d % (p - 1)
        dQ = d % (q - 1)
        x_q = pow(y % q, dQ, q)
        x_0 = pow(y % p, dP, p)
        p2 = p*p
        x_1 = (((y - pow(x_0, e, p2)) * e * pow(pow(x_0, e - 1, p2) % p, -1, p)) // p) % p
        x_p2 = x_1*p + x_0

        decrypted_message2 = tcr_garner([p*p, q],
                                        [x_p2, x_q])
        finish1 = time.time_ns() - start1

    return tuple((finish*10**-9, finish1*10**-9))


def find_longest_bitstring(n, i, w):
    j = i
    j_max = i
    for j in range(i, len(n)):
        if j - i + 1 <= w and n[i] == n[j] == '1':
            if j_max < j:
                j_max = j
    return j_max


def sliding_window(x_, n, m, w):
    x = [1]*(2**w)
    x[1] = x_ % m
    x[2] = x[1]*x[1] % m
    for omega in range(3, (2**w), 2):
        x[omega] = x[omega-2]*x[2] % m
        # print(omega, " : ", x[omega])
    # print(x)
    binary_n = str(bin(n))[2:]
    # binary_n = binary_n[::-1]
    # print("Binary:", binary_n)
    y = 1

    i = 0

    while i < len(binary_n):
        # print("I:", i)
        if binary_n[i] == 0:
            y = y*y % m
            i = i + 1

        j = find_longest_bitstring(binary_n, i, w)
        # print("J:", j)
        for l in range(1, j-i+2):
            # print("L:", l)
            y = y*y % m
        # print("X:", x[int(binary_n[j:i + 1], 2)])
        # print("Y_:", y)
        y = y * x[int(binary_n[i:j+1], 2)] % m
        i = j + 1
    return y


def part1_sliding_window(bits=512, print_message=false):
    if print_message:
        p = number.getPrime(bits)
        q = number.getPrime(bits)
        r = number.getPrime(bits)
        e = 65537
        print("P: ", p)
        print("Q: ", q)
        print("R: ", r)
        public_key = rsa_public_key(p, q, r, e, totient='Euler')
        print(f"Public Key:\nn={public_key[0]}\ne={public_key[1]}  ")
        private_key = rsa_private_key(p, q, r, e, totient='Euler')
        print(f"Private Key:\nn={private_key[0]}\nd={private_key[1]}")

        message = 42
        print("Message:        ", message)
        y = encipher_rsa(message, public_key)
        print("Ciphertext:     ", y)

        start = time.time_ns()
        decrypted_message = decipher_rsa(y, private_key)
        finish = time.time_ns() - start

        print("Decrypted Text: ", decrypted_message)
        print("Time used by library decryption:   ", finish*10**-9, "seconds")

        start1 = time.time_ns()
        d = private_key[1]
        dP = d % (p - 1)
        dQ = d % (q - 1)
        dR = d % (r - 1)
        x_p = sliding_window(y % p, dP, p, 3)
        x_q = sliding_window(y % q, dQ, q, 3)
        x_r = sliding_window(y % r, dR, r, 3)
        decrypted_message2 = tcr_garner([p, q, r],
                                        [x_p, x_q, x_r])
        finish1 = time.time_ns() - start1
        print("TCR Decrypted Text: ", decrypted_message2)
        print("Time used by TCR Garner decryption:", finish1*10**-9, "seconds")
    else:
        p = number.getPrime(bits)
        q = number.getPrime(bits)
        r = number.getPrime(bits)
        e = 65537
        public_key = rsa_public_key(p, q, r, e, totient='Euler')
        private_key = rsa_private_key(p, q, r, e, totient='Euler')
        message = 42
        y = encipher_rsa(message, public_key, factors=[p, q, r])
        start = time.time_ns()
        decrypted_message = decipher_rsa(y, private_key, factors=[p, q, r])
        finish = time.time_ns() - start
        start1 = time.time_ns()
        d = private_key[1]
        dP = d % (p - 1)
        dQ = d % (q - 1)
        dR = d % (r - 1)
        x_p = sliding_window(y % p, dP, p, 9)
        x_q = sliding_window(y % q, dQ, q, 9)
        x_r = sliding_window(y % r, dR, r, 9)
        decrypted_message2 = tcr_garner([p, q, r],
                                        [x_p, x_q, x_r])
        finish1 = time.time_ns() - start1

        return tuple((finish*10**-9, finish1*10**-9))


if __name__ == '__main__':
    percentage = 0
    sample_size = 100
    x = []
    r = []
    for i in range(0, sample_size):
        x.append(part1(1024))
        # print(x[i])
        if x[i][0] - x[i][1] > 0:   # a durat mai mult timp pentru librarie decat pentru tcr garner
            percentage += 1
            r.append(x[i][0]/x[i][1])
    print(f"{percentage*100/sample_size}% of tests had TCR faster than library with average time difference of {sum([abs(i1-i2) for i1,i2 in x]) / sample_size} "
          f"with avg ratio: {sum(r)/sample_size} and max ratio: {max(r)}({x[r.index(max(r))]})")
    percentage = 0
    sample_size = 100
    x = []
    r = []
    for i in range(0, sample_size):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x.append(part2(1024))
        # print(x[i])
        if x[i][0] - x[i][1] > 0:   # a durat mai mult timp pentru librarie decat pentru tcr garner
            percentage += 1
            r.append(x[i][0]/x[i][1])
    print(f"{percentage*100/sample_size}% of tests had TCR faster than library with average time difference of {sum([abs(i1-i2) for i1,i2 in x]) / sample_size} "
          f"with avg ratio: {sum(r)/sample_size} and max ratio: {max(r)}({x[r.index(max(r))]})")
    percentage = 0
    sample_size = 100
    x = []
    r = []
    for i in range(0, sample_size):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x.append(part1_sliding_window(1024))
        # print(x[i])
        if x[i][0] - x[i][1] > 0:   # a durat mai mult timp pentru librarie decat pentru tcr garner
            percentage += 1
        r.append(x[i][0]/x[i][1])
    print(f"{percentage*100/sample_size}% of tests had TCR faster than library with average time difference of {sum([abs(i1-i2) for i1,i2 in x]) / sample_size} "
          f"with avg ratio: {sum(r)/sample_size} and max ratio: {max(r)}({x[r.index(max(r))]})")

    print("TCR vs Librarie:   MultiPrime RSA        ")
    part1(512, True)
    print("TCR vs Librarie:   MultiPower RSA        ")
    part2(512, True)
    print("TCR+Sliding Window vs Librarie:  MultiPrime RSA")
    part1_sliding_window(512, True)


    # part2(512)
    # print(tcr_garner([9, 5], [7, 3]))
    # d = 11
    # e = 11
    # n = 45
    # p = 3
    # q = 5
    # y = 22
    #
    # dP = d % (p - 1)
    # dQ = d % (q - 1)
    # x_q = pow(y % q, dQ, q)
    # print(x_q)
    # x_0 = pow(y % p, dP, p)
    # p2 = p*p
    # x_1 = (((y - pow(x_0, e, p2)) * e * pow(pow(x_0, e-1, p2) % p, -1, p)//p)) % p
    # print(x_0)
    # print(x_1)
    # x_p2 = x_1*p + x_0
    # print(x_p2)
    # print(tcr_garner([9, 5], [x_p2, x_q]))

    # print("Y:", sliding_window(10, 324, 8683317618811886495518194401279999999, 3))
    # print("Y:", sliding_window(4, 50, 497, 2))
    # x = str(bin(50))[2:]
    # print(x)
    # print(x[::-1])
    # part1_sliding_window(512)



