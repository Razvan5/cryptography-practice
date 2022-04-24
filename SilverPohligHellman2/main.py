import sympy
import Cryptodome
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.number import getPrime
import time
from random import randint
from sympy.ntheory import legendre_symbol
from sympy.ntheory import jacobi_symbol
from sympy.ntheory.modular import crt
# il folosesc in caz ca am nevoie de calcule mai rapide
from sympy.ntheory import discrete_log


def SLOW_generate_primitive_root_mod_p(P, Q, verbose=False):
    stop_1 = False
    stop_2 = False
    for a in range(2, P):
        # Q = (p-1)/2
        a1 = pow(a, Q, P)
        a2 = pow(a, 2, P)
        if pow(a1, 2, P) == 1 and pow(a2, Q, P) == 1:
            return a
        # for i in range(2, P):
        #     if pow(a1, i, P) == 1 and not stop_1:
        #         print(f"A1^i mod p:{pow(a1, i, P)} <-Ordin {i}")
        #         stop_1 = True
        #     if pow(a2, i, P) == 1 and not stop_2:
        #         print(f"A2^i mod p:{pow(a2, i, P)} <-Ordin {i}")
        #         stop_2 = True
        #     if stop_1 and stop_2:
        #         break
    # print(f"A1^i mod p:{pow(a1, 2, P)} <-pt {2}")
    # print(f"A2^i mod p:{pow(a2, Q, P)} <-pt {Q}")


def FAST_generate_primitive_root_mod_p(P, Q=None, verbose=False):
    a = randint(2, P - 2)
    # print(f"A: {a}")
    if legendre_symbol(a, P) == -1:
        return a
    else:
        return P - a


def discrete_logarithm_shanks(a_primitive_root, b_arbitrary_element, p_prime):
    # b = a^x mod p | x = ?
    # x = log_a(b) mod p
    m = int(sympy.ceiling(sympy.sqrt(p_prime - 1)))
    print("M:", m)
    baby_steps = []
    for j in range(0, m):
        baby_steps.append((pow(a_primitive_root, j, p_prime), j))
    baby_steps = dict(baby_steps)
    # print("baby steps:", baby_steps)
    a_m = pow(a_primitive_root, -m, p_prime)
    for i in range(0, p_prime):
        find_this = (b_arbitrary_element * pow(a_m, i, p_prime)) % p_prime
        J = baby_steps.get(find_this)
        if J is not None:
            print(f"FIND THIS {find_this}")
            print(f"j:{J}")
            print(f"i:{i}")
            I = i
            return I * m + J


def factorization(number):
    prime_factors = []
    start_prime = 2
    while start_prime * start_prime <= number:
        if number % start_prime == 0:
            expo = 0
            while number % start_prime == 0:
                expo = expo + 1
                number = number // start_prime
            prime_factors.append([start_prime, expo])
        start_prime = start_prime + 1

    if number > 1:
        prime_factors.append([number, 1])

    return prime_factors


def silver_pohlig_hellman2(a_primitive_root, b_arbitrary_element, p_prime, p_factorization):
    k = len(p_factorization)
    # aici e stocat x[i] are lungimea numarilor de factori
    X = [0] * k
    A = [0] * k
    for i in range(0, k):
        e = p_factorization[i][1]
        C = [0] * e
        P_P = (p_prime - 1) // p_factorization[i][0]
        A[i] = pow(a_primitive_root, P_P, p_prime)
        C[0] = discrete_log(p_prime, pow(b_arbitrary_element, P_P, p_prime), A[i])
        X[i] = C[0]
        for j in range(1, e):
            S = X[i]
            aS = pow(a_primitive_root, -S, p_prime)
            C[j] = discrete_log(p_prime,
                                pow(b_arbitrary_element * aS, (p_prime - 1) // (p_factorization[i][0] ** (j + 1)), p_prime),
                                A[i])
            X[i] += C[j] * (p_factorization[i][0] ** j)
    moduli = [(f[0] ** f[1]) for f in p_factorization]
    print("Ai:", A)
    print("Xi:", X)
    print("Moduli:", moduli)
    tcr_solution = crt(moduli, X)
    return tcr_solution[0]


# def silver_pohlig_hellman(a_primitive_root, b_arbitrary_element, p_prime, p_factorization):
#     # prime factorization e de forma [(prime, exponent)] [(p1, e1)...(pi, ei)...(pk,ek)]
#     k = len(p_factorization)
#     a = [0] * k
#
#     xi = [0] * k
#     S = 0
#     # merge de la 0 la k-1 (k c-uri pt numarul x in baza pi)
#     for i in range(0, k):
#         e_i = p_factorization[i][1]
#         c = [0] * e_i
#         X = [0] * e_i
#         p__p_0 = (p_prime - 1) // p_factorization[i][0]
#         a[0] = pow(a_primitive_root, p__p_0, p_prime)
#         c[0] = discrete_log(p_prime, a[0], pow(b_arbitrary_element, p__p_0, p_prime))
#         X[0] = c[0] * (p_factorization[i][0] ** i)
#         for e in range(1, e_i):
#             Sj = sum(X)
#             # p__p_i = (p_prime - 1) // (p_factorization[e][0] ** e)
#             # a[e] = pow(a_primitive_root, p__p_i, p_prime)
#             c[e] = discrete_log(p_prime, a[i], b_arbitrary_element * pow(a_primitive_root, -Sj, p_prime)) % p_factorization[i][0]
#             X[e] = (c[e] * (p_factorization[i][0] ** e))
#         xi[i] = sum(X)
#         a = []
#         c = []
#         X = []
#     moduli = [i[1] for i in p_factorization]
#     tcr_solution = crt(xi, moduli)
#     return tcr_solution


def print_sph(a, b, modulo):
    print("_____________________________________________________________________________________________________")
    factors = factorization(modulo - 1)
    print(f"Silver-Pohlig-Hellman:\n {a}ˣ = {b} mod {modulo} with factors of {modulo - 1} = {factors}")
    answer = silver_pohlig_hellman2(a, b, modulo, factors)
    print("Answer:", answer)
    print(f"Testing:\n {a}^{answer} = {b} mod {modulo} <-[TESTING: {pow(a, answer, modulo)} ]")
    print("_____________________________________________________________________________________________________")


if __name__ == '__main__':
    # q = Cryptodome.Util.number.getPrime(32)
    # p = 2 * q + 1
    # while not sympy.isprime(p):
    #     q = Cryptodome.Util.number.getPrime(32)
    #     p = 2 * q + 1
    # print(f"Q = {q}")
    # print(f"P = {p}")
    # print(Cryptodome.Util.number.getPrime(512)-1)
    # print(factorization(Cryptodome.Util.number.getPrime(32)-1))
    # start = time.time_ns()
    # alfa = FAST_generate_primitive_root_mod_p(p, q)
    # print(f"Alfa:{alfa}")
    # print(f"Time:{(time.time_ns() - start) / 1_000_000} milliseconds")
    # b = randint(1, p - 1)
    # print(f"B:{b}")
    # print(" " * (len(f"Solving {alfa}")) + "x")
    # print(f"Solving {alfa} = {b} mod {p}")
    # x = discrete_logarithm_shanks(alfa, b, p)
    # print(f"x = {x}")
    # print(f"TEST: {pow(alfa, x, p)} ")

    print("______________________________________")

    # p = 41
    # alfa = FAST_generate_primitive_root_mod_p(p)
    # print(alfa)

    # x = [[1, 3], [4, 5]]
    # y = [i[1] for i in x]
    # print(y)
    # print(discrete_log(41, 40, 5))
    # print(discrete_log(41, 1, 40))
    # a = 6
    # b = 5
    # modulo = 41
    # factors = factorization(modulo - 1)
    # answer = silver_pohlig_hellman2(6, 5, 41, factorization(40))
    # print(f"Silver-Pohlig-Hellman:\n {a}ˣ = {b} mod {modulo} with factors of {modulo - 1} = {factors}\n Answer:",
    #       answer)
    # print(f"Testing:\n {a}^{answer} = {b} mod {modulo} <-[ {pow(a, answer, modulo)} ]")
    print("Exemplu clasa")
    print_sph(6, 5, 41)
    print("Numere un pic mai mari")
    print_sph(1168, 15, 2039)
    print_sph(2, 15, 101)
    print("Pe 32 de bits")
    print_sph(1581035097, 94, 4161377459)

    for i in range(1, 1000):
        q = 2**randint(150, 200) * 3**randint(100, 150) * 7 ** randint(50, 100) * 11 ** randint(10, 50)
        if sympy.isprime(q+1):
            print(q)
            p = q + 1
            print(sympy.isprime(p))
    print("A INCEPUT")
    start = time.time()
    p = 1979392391681203398187160916525451593306497315225669832160250795143529956591384429245098961787386995869604803429616855015178573839310389194458877713024870104864113802543140066182561793
    print_sph(5, 3, 1979392391681203398187160916525451593306497315225669832160250795143529956591384429245098961787386995869604803429616855015178573839310389194458877713024870104864113802543140066182561793)
    print("End:", time.time() - start)
    print_sph(5, 3 , p)
    # p = Cryptodome.Util.number.getPrime(32)
    # q = (p-1)//2
    # print("P:", p)
    # print("Facto:", factorization(p-1))
    # print_sph(FAST_generate_primitive_root_mod_p(p, q), randint(1, 100), p)
    # print_sph(FAST_generate_primitive_root_mod_p(3099388321, (3099388321-1)//2), 3, 3099388321)

