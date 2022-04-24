import random
import math


def sign(x):
    if x >= 0:
        return 1
    else:
        return -1


def karatsubaMultiply(a, b, beta, n0, n):
    if n <= n0:
        return a * b

    k = math.ceil(n/2)
    a0, b0 = (a % beta**k, b % beta**k)
    a1, b1 = (a // beta**k, b // beta**k)

    sa = sign(a0 - a1)
    sb = sign(b0 - b1)

    print(f"K={k}, A0={a0}, B0={b0}, A1={a1}, B1={b1}")
    c0 = karatsubaMultiply(a0, b0, beta, n0, k)
    c1 = karatsubaMultiply(a1, b1, beta, n0, k)
    c2 = karatsubaMultiply(abs(a0 - a1), abs(b0 - b1), beta, n0, k)

    print(f"K={k}, C0={c0}, C1={c1}, C2={c2}, sa = {sa}, sb = { sb}")
    return c0 + (c0 + c1 - sa*sb*c2)*beta**k + c1*beta**(2*k)


def ToomCook3(a, b, n, beta, n1=3):
    if n < n1:
        return karatsubaMultiply(a, b, beta, n1, n)

    k = math.ceil(n/3)
    x2 = beta**(k*2)
    a0 = a % beta
    b0 = b % beta

    a1 = (a // beta) % beta
    b1 = (b // beta) % beta

    a2 = a // x2
    b2 = b // x2

    print(f"K={k}:\nA0={a0}, B0={b0}, A1={a1}, B1={b1}, A2={a2}, B2={b2}")

    v0 = ToomCook3(a0, b0, k, beta)
    v1 = ToomCook3(a0+a2+a1, b0+b2+b1, k, beta)
    v_1 = ToomCook3(a0+a2-a1, b0+b2-b1, k, beta)
    v2 = ToomCook3(a0 + 2*a1 + 4*a2, b0 + 2*b1 + 4*b2, k, beta)
    vInf = ToomCook3(a2, b2, k, beta)

    print(f"K={k}:\nV0={v0}, V1={v1}, V-1={v_1}, V1={v2}, Vinf={vInf}, B2={b2}")

    t1 = (3*v0 + 2*v_1 + v2)//6 - 2*vInf
    t2 = (v1 + v_1)//2

    print(f"T1={t1}, T2={t2}")

    c0 = v0
    c1 = v1 - t1
    c2 = t2 - v0 - vInf
    c3 = t1 - t2
    c4 = vInf

    print(f"K={k}:\nC0={c0}, C1={c1}, C2={c2}, C3={c3}, C4={c4}")

    return c0 + c1 * beta**k + c2 * beta**(2*k) + c3 * beta ** (3*k) + c4 * beta ** (4*k)


def binary_extended_gcd(x, y):
    g = 1
    while x % 2 == y % 2 == 0:
        x //= 2
        y //= 2
        g *= 2
    u = x
    v = y
    A = 1
    B = 0
    C = 0
    D = 1
    print(f"Phase  0:  A={A} |B {B}  |C {C}  |D {D} |u {u} v {v}  |g {g}")
    i = 0
    while u:
        i += 1
        while u % 2 == 0:
            print(f"Phase  {i}:  A {A}  |B {B}  |C {C}  |D {D}  |u {u} |v {v} |g {g}")
            u //= 2
            if A % 2 == B % 2 == 0:
                A //= 2
                B //= 2
            else:
                A = (A + y)//2
                B = (B - x)//2
            print("--------------------------------")

        while v % 2 == 0:
            print(f"Phase  {i}:  A {A}  |B {B}  |C {C}  |D {D}  |u {u} |v {v} |g {g}")
            v //= 2
            if C % 2 == D % 2 == 0:
                C //= 2
                D //= 2
            else:
                C = (C + y)//2
                D = (D - x)//2
            print("--------------------------------")

        if u >= v:
            u = u - v
            A = A - C
            B = B - D
        else:
            v = v - u
            C = C - A
            D = D - B

    a = C
    b = D
    return a, b, g * v


def bauer(n):
    chain = [0] * n
    in_chain = [False] * (n + 1)
    best = None
    best_len = n
    cnt = 0

    def extend_chain(x=1, pos=0):
        nonlocal best, best_len, cnt

        if x << (best_len - pos) < n:
            return

        chain[pos] = x
        in_chain[x] = True
        pos += 1

        if in_chain[n - x]:  # found solution
            if pos == best_len:
                cnt += 1
            else:
                best = tuple(chain[:pos])
                best_len, cnt = pos, 1
        elif pos < best_len:
            for i in range(pos - 1, -1, -1):
                c = x + chain[i]
                if c < n:
                    extend_chain(c, pos)

        in_chain[x] = False

    extend_chain()
    return best + (n,), cnt


def jacobi(a, n):
    if n <= 0:
        raise ValueError("'n' must be a positive integer.")
    if n % 2 == 0:
        raise ValueError("'n' must be odd.")
    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    else:
        return 0

# def lehmer_gcd(x, y):
#     radix = 10
#     while y >= radix:
#         x_, y_ = int(str(x)[:1]), int(str(y)[:1])
#         A = 1
#         B = 0
#         C = 0
#         D = 1
#         while (y_ + C) != 0 and (y_ + D) != 0:
#             q = math.floor((x_ + A)/(y_ + C))
#             q_ = math.floor((x_ + B)/(y_ + D))
#             if q != q_:
#                 if B = 0
#                 t = A - q * C
#                 A = C
#                 C = t
#                 t = B - q * D
#                 B = D
#                 D = t
#                 t = x_ - q*y_

# Lehmer's gcd algorithm;  revised version

DIGIT_BITS = 30
BASE = 1 << DIGIT_BITS

def nbits(n, correction = {
        '0': 4, '1': 3, '2': 2, '3': 2,
        '4': 1, '5': 1, '6': 1, '7': 1,
        '8': 0, '9': 0, 'a': 0, 'b': 0,
        'c': 0, 'd': 0, 'e': 0, 'f': 0}):
    """Number of bits in binary representation of the positive integer n,
    or 0 if n == 0.
    """
    if n < 0:
        raise ValueError("The argument to _nbits should be nonnegative.")
    hex_n = "%x" % n
    return 4*len(hex_n) - correction[hex_n[0]]

def lehmer_gcd(a, b):
    """Greatest common divisor of nonnegative integers a and b."""

    # initial reductions
    if a < b:
        a, b = b, a

    while b >= BASE:
        size = nbits(a) - DIGIT_BITS
        x, y = int(a >> size), int(b >> size)
        # single-precision arithmetic from here...
        A, B, C, D = 1, 0, 0, 1
        while True:
            if y+C == 0 or y+D == 0:
                break
            q = (x+A)//(y+C)
            if q != (x+B)//(y+D):
                break
            A, B, x, C, D, y = C, D, y, A-q*C, B-q*D, x-q*y
        # ...until here

        if B:
            a, b = A*a + B*b, C*a + D*b
        else:
            a, b = b, a % b

    a, b = int(b), int(a%b)
    # final single-precision gcd computation
    while b:
        a, b = b, a%b
    return a


if __name__ == '__main__':
    print(karatsubaMultiply(1028, 1028, 10, 1, 4))
    # print(ToomCook3(150112, 123123, 3, 10))
    # print(binary_extended_gcd(693, 609))
    # print(binary_extended_gcd(51, 71))
    # for n in [7, 14, 21, 29, 32, 42, 64, 47, 79, 191, 382, 379]:
    #     best, cnt = bauer(n)
    #     print(f'L({n}) = {len(best) - 1}, count of minimum chain: {cnt}\ne.g.: {best}\n')
    # print(lehmer_gcd(693, 609))
    # print(lehmer_gcd(51, 71))