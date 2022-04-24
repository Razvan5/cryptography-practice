import random
import math
import time
from sympy import *


def Jacobi_Symbol(a, n):
    if n <= 0 or n % 2 == 0:
        return "ERROR"

    a %= n  # (a/n) = (a%n/ n)
    result = 1

    while a != 0:
        while a % 2 == 0:  # for a=2a' |=> 2a'/n = a'/n if V else -1*
            a /= 2                                       # V
            n_mod_8 = n % 8                              # V
            if n_mod_8 in (3, 5):  # m = ± 3 mod 8 pt ±1 mod 8 nimic
                result = -result

        a, n = n, a # a,n odd => inversare

        if a % 4 == 3 and n % 4 == 3:  # m = 3 mod 4 sau a = 3 mod 4
            result = -result

        a %= n
    if n == 1:
        return result
    else:
        return 0


def Solovoy_Strassen(n, t):
    for i in range(1, t):
        a = random.randint(2, n - 2)
        r = pow(a, (n - 1) // 2, n)
        if r != 1 and r != n - 1:
            return f"{n} IS COMPOSITE"
        s = Jacobi_Symbol(a, n)

        if s == "ERROR":
            return f"{n} IS COMPOSITE Er"
        if r != s % n:
            return f"{n} IS COMPOSITE J*"
    return f"{n} IS PRIME"


def modulus(k, s, p):
    i = (k & p) + (k >> s)
    # print(f"{s}, {k}, {p}, {i}")

    if i >= p:
        return i - p
    else:
        return i


def mersenne_modulus(tested_number, merssene_power, suspected_mersenne_prime):
    # base b = 2, z = tested_number
    # p = 2^mersenepower - 1

    # A1 = tested_number // (suspected_mersenne_prime+1)
    A1 = tested_number >> merssene_power
    # A0 = tested_number % (suspected_mersenne_prime+1)
    A0 = tested_number - A1*(suspected_mersenne_prime+1)
    # print(f"{merssene_power}, {tested_number}, {suspected_mersenne_prime}, A1:{A1}, A0:{A0}")
    if A1 == A0 == suspected_mersenne_prime:
        return 0
    elif A1 + A0 < suspected_mersenne_prime:
        return A1 + A0
    else:
        return A1 + A0 - suspected_mersenne_prime


def Lucas_Lehmer(n, s):
    for i in range(2, math.floor(math.sqrt(s))):
        if n % s == 0:
            return f"{n} IS COMPOSITE"
    u = 4
    for k in range(1, s - 1):
        # u = modulus(u**2 - 2, s, n)
        u = mersenne_modulus(u ** 2 - 2, s, n)
        # u = (u ** 2 - 2) % n
    if u == 0:
        return f"(s={s}) {n} is PRIME"
    return f"{n} IS COMPOSITE"


def Lucas_Lehmer_Slow(n, s):
    for i in range(2, math.floor(math.sqrt(s))):
        if n % s == 0:
            return f"{n} IS COMPOSITE"
    u = 4
    for k in range(1, s - 1):
        u = (u ** 2 - 2) % n
    if u == 0:
        return f"(s={s}) {n} is PRIME"
    return f"{n} IS COMPOSITE"


def Lucas_Lehmer_Fast(n, s):
    for i in range(2, math.floor(math.sqrt(s))):
        if n % s == 0:
            return f"{n} IS COMPOSITE"
    u = 4
    for k in range(1, s - 1):
        u = modulus((u ** 2 - 2), s, n)
    if u == 0:
        return f"(s={s}) {n} is PRIME"
    return f"{n} IS COMPOSITE"


def speed_test(lehmer, mersenne_power):
    start = time.time_ns()
    test = lehmer((2 ** mersenne_power) - 1, mersenne_power)
    end = (time.time_ns() - start) / (10 ** 9)
    print(f"NAME: {lehmer.__name__}\n TIME:{end}s => {test}")


if __name__ == '__main__':

    print(Solovoy_Strassen(25, 11))
    print(Solovoy_Strassen(21, 11))
    print(Solovoy_Strassen(19, 13))
    print(Solovoy_Strassen(19, 17))
    print(Solovoy_Strassen(25, 22))
    print(Solovoy_Strassen(17, 24))
    print(Solovoy_Strassen(171, 24))
    print(Solovoy_Strassen(534231, 24))
    print(Solovoy_Strassen(15465634, 24))
    print(Solovoy_Strassen(145456, 24))

    for i in range(1, 10000):
        a = random.randint(1, 1000000)
        if isprime(a):
            t = "PRIME"
        else:
            t = "COMPOSITE"
        if t in Solovoy_Strassen(a, 17):
            print(f"S_S: {Solovoy_Strassen(a, 17)} vs Library?:{t} ✔️")
        else:
            print(f"S_S: {Solovoy_Strassen(a, 17)} vs Library?:{t} ❌   ")

    print("___________________")
    speed_test(Lucas_Lehmer, 23)
    speed_test(Lucas_Lehmer_Fast, 23)
    speed_test(Lucas_Lehmer_Slow, 23)
    print("___________________")
    total_start = time.time_ns()

    for s in range(3, 859433):
        # print(1 << (2 * s) - 1)
        start = time.time_ns()
        test = Lucas_Lehmer((2 ** s) - 1, s)
        end = (time.time_ns() - start) / (10 ** 9)
        if "PRIME" in test:
            total_end = (time.time_ns() - total_start) / (10 ** 9)
            print(f"TOTAL_TIME: {total_end} TIME:{end}s=>{test}")

