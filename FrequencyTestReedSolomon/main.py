from random import randrange, getrandbits, randint
import itertools


def is_prime(n, k=128):
    """ Test if a number is prime
        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do
        return True if n is prime
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def generate_prime_candidate(length):
    """ Generate an odd integer randomly
        Args:
            length -- int -- the length of the number to generate, in bits
        return a integer
    """
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(length=512):
    """ Generate a prime
        Args:
            length -- int -- length of the prime to generate, in          bits
        return a prime
    """
    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p


# ak-1*x^(k-1)+...+a1*x
# de verificat daca if-ul merge corect
def calculate_poly(coefficient_values, value, p):
    result = 0
    print(f'Value: {value}')
    for i, coefficient in enumerate(coefficient_values):
        semi_result = result*value
        if semi_result < p:
            result = semi_result + coefficient
        else:
            result = semi_result % p + coefficient
        print(i)

    result *= value

    print(result % p)
    return result % p


def encode(coefficient_values, n, p, s=1):
    output = ["null"]
    output += [calculate_poly(coefficient_values, i, p) for i in range(1, n+1)]
    return output


# max_seq_size = max byte count
def convert_message_to_polynomial(string_message, max_seq_size):
    # o litera in ascii este 8 bits (01011010) => 8*max_seq_size < p
    n_bit_sequences = [string_message[index: index + max_seq_size]
                       for index in range(0, len(string_message), max_seq_size)]
    print(n_bit_sequences)
    polynomial = []
    for sequence in n_bit_sequences:
        binary_number = ''
        for letter in sequence:
            binary_number += '{0:08b}'.format(ord(letter))
        print(int(binary_number, 2))
        # print(binary_number)
        number = int(binary_number, 2)
        polynomial.append(number)
    return polynomial


def convert_polynomial_to_message(polynomial, max_seq_size):
    binary_coefficient = ''
    message = ''
    x = '{0:'+str(max_seq_size*8)+'b}'
    for coefficient in polynomial:
        binary_coefficient = str(x.format(coefficient))

        eight_bit_sequences = [binary_coefficient[index: index + 8]
                               for index in range(0, len(binary_coefficient), 8)]
        for eight_bits in eight_bit_sequences:
            message += chr(int(eight_bits, 2))
    return message


def induce_error(coefficient_values, p):
    r = randint(1, len(coefficient_values)-1)
    e = randint(0, p)
    # print(f"R:{r} >? {len(coefficient_values)}")
    coefficient_values[r] = (coefficient_values[r] + e) % p

def calculate_fc(combination, coefficient_values, p):
    fc = 0
    for i in combination:
        multiplication = 1
        for j in combination:
            if j != i:
                multiplication *= j*pow((j-i) % p, -1, p)
        fc = (fc + (coefficient_values[i]*multiplication) % p) % p
    return fc


def calculate_fc_k_inversion(combination, coefficient_values, p):
    fc = 0
    for i in combination:
        numarator = 1
        numitor = 1
        for j in combination:
            if j!= i:
                numarator *= j
                numitor *= (j-i) % p
        fc = (fc + (coefficient_values[i]*numarator*pow(numitor, -1, p))) % p

    return fc


def calculate_fc_one_inversion(combination, coefficient_values, p):
    fc = 0
    numitor_vector = []
    numarator_vector = []
    up_numitor_vector = []
    for i in combination:
        numarator = coefficient_values[i]
        numitor = 1
        for j in combination:
            if j != i:
                numarator *= j
                numitor *= (j-i) % p
        numitor_vector.append(numitor)
        numarator_vector.append(numarator)
        # fc = (fc + (numarator*pow(numitor, -1, p))) % p
    print(numarator_vector)
    print(numitor_vector)

    final_numarator = 0
    for index1, numarator_element in enumerate(numarator_vector):
        up_numitor = numarator_element
        for index2, numitor_element in enumerate(numitor_vector):
            if index1 != index2:
                up_numitor = (numitor_element*up_numitor) % p
        up_numitor_vector.append(up_numitor)

    print(up_numitor_vector)

    final_numitor = 1
    for numitor_element in numitor_vector:
        final_numitor = (final_numitor*numitor_element) % p

    fc = 0
    for element in up_numitor_vector:
        fc = (fc + element) % p

    fc = fc*pow(final_numitor, -1, p)

    return fc % p


def poly_multiply(A, B, p):
    m = len(A)
    n = len(B)
    prod = [0] * (m + n - 1)

    for i in range(m):
        for j in range(n):
            prod[i + j] += A[i] * B[j] % p
            prod[i + j] %= p

    return prod


def scalar_multiply(A, scalar, p):
    m = len(A)
    for i in range(m):
        A[i] = (A[i] * scalar) % p
    return A


def poly_add(A, B, p):
    m = len(B)
    prod = [0] * m

    for i in range(m):
        prod[i] += (A[i] + B[i]) % p

    return prod


def create_poly(coefficient_values, combination, p):
    true_message = [0]*(len(combination))
    for i in combination:
        result = [1]
        for j in combination:
            if j != i:
                print(j)
                result = (poly_multiply(result, [1, -j % p], p))
                result = scalar_multiply(result, pow((i-j) % p, -1, p), p)
        print("______")
        true_message = poly_add(true_message, scalar_multiply(result, coefficient_values[i], p), p)
    return true_message


def decode(coefficient_values, n, p, k):
    coefficient_index = range(1, n+1)
    # print("INDEX:", coefficient_index)
    combinations = list(itertools.combinations(coefficient_index, k))
    print(f"K: {k}")
    for combination in combinations:
        fc = calculate_fc_one_inversion(combination, coefficient_values, p)
        print(f"Calcul fc: {combination} -> {fc}")
        if fc == 0:
            return create_poly(coefficient_values, combination, p)


def decode_with_error(coefficient_values, n, p, k):
    coefficient_index = range(1, n+1)
    print("INDEX:", coefficient_index)
    combinations = list(itertools.combinations(coefficient_index, k))
    print(f"K: {k}")
    for combination in combinations:
        fc = calculate_fc_one_inversion(combination, coefficient_values, p)
        if fc != 0:
            return create_poly(coefficient_values, combination, p)


def pad_message(message_to_pad, padding, padding_character=' '):
    x = padding - len(message_to_pad) % padding
    return message_to_pad + padding_character*x


if __name__ == '__main__':
    # print(generate_prime_number(161))
    # print(convert_message_to_polynomial(message, 20))

    # p = generate_prime_number(10)


    # random message needs to be converted
    # m = [randint(0, p - 1) for i in range(1, k)]
    # message = input()
    # m = [2, 7]
    # p = 17  # numar generat aleator p>=n>k!
    # k = len(m)+1   # numarul de elemente din polinomul mesaj este k-1 !
    # s = 1   # numarul de greseli care pot aparea la transmitere
    # n = k+2*s  #numarul de elemente din mesajul codat este n
    # print(m)
    # print("Encoding: ", encode(m, n, p))
    # y = encode(m, n, p)
    # print(y)
    # y[2] = 3
    # print(y)
    # # am adaugat [:-1] ca sa nu mai apara si coeficientul liber
    # print(f"Decoding {s} error:", decode(y, n, p, k)[:-1])

    message = "I want to check this text for I want to check this text for I want to check this text for I want to check this text for "
    message = pad_message(message, 20, 'X')
    m = convert_message_to_polynomial(message, 20)
    p = generate_prime_number(161)
    print("Prime Number: ", p)
    k = len(m)+1
    s = 1
    n = k+2*s
    y = encode(m, n, p, s)
    print("Encoding     : ", y)
    induce_error(y, p)
    print("Error      Y:  ", y)
    d_y = decode(y, n, p, k)[:-1]
    print("Original Poly: ", m)
    print("Decoded  Poly: ", d_y)
    d_e = decode_with_error(y, n, p, k)[:-1]
    print("Message      : ", convert_polynomial_to_message(d_y, 20))
    print("Message error: ", convert_polynomial_to_message(d_e, 20))