import itertools
import time
import random


def calculate_fc_worst_case(combination, coefficient_values, p):
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
            if j != i:
                numarator *= j
                numitor *= (j-i) % p
        fc = (fc + (coefficient_values[i]*numarator*pow(numitor, -1, p))) % p

    return fc


def calculate_fc_one_inversion(combination, coefficient_values, p):
    fc = 0
    numitor = 1
    for i in combination:
        for j in combination:
            if j != i:
                numitor *= (j - i) % p

    for i in combination:
        numitor_de_inmultit = 1
        numarator = coefficient_values[i]
        for combo_i in reversed(list(itertools.combinations(combination, 2))):
            for c_i in combo_i:
                # zk1*k2*k3
                numarator *= c_i
                numarator %= p
                for j in combination:
                    if j != c_i:
                        # print("j:", j)
                        # print("i:", c_i)
                        # print("---------------------")
                        numitor_de_inmultit *= (j - c_i) % p
            # print("VVVVVVVVVVVVVV")
            numitor_de_inmultit %= p
            fc = (fc + (numitor_de_inmultit*numarator) % p) % p

        fc = fc * pow(numitor, -1, p)

        return fc % p


#  numerator
# -----------
# denominator
def calculate_fc_one_inversion_2(combination, coefficient_values, p):
    # k1 = indexul 1 din combination care poate sau nu sa fie 1
    # z_k1 = valoarea coefficientului de la indexul k1
    # >x denota variabila care ii dau track
    # >k1 sau k2 sau k3
    fc = 0
    for i in combination:
        # >z_k1 sau z_k2 sau z_k3
        numerator = coefficient_values[i]
        print(f"N: {numerator}")
        # >[k2, k3] sau [k1, k3] sau [k1, k2]
        for combo_i in reversed(list(itertools.combinations(combination, 2))):
            # >k2 sau >k3 || k1 sau k3 || k1 sau k2
            for c_i in combo_i:
                # >z_k1 * k2 * k3
                numerator = (numerator * c_i) % p
            # >k2 sau >k3 || k1 sau k3 || k1 sau k2
            denominator_up = 1
            for c_i in combo_i:
                # ~k1 ~k2 ~k3
                for j in combination:
                    if j != c_i:
                        # print(f'{j} - {c_i}')
                        # (j  - combo_i)...
                        # create (k1 - k2)(k3 - k2)(k1 - k3)(k2 - k3) and similar ones and multiply with numerator
                        denominator_up = (denominator_up * (j - c_i) % p) % p
            print(f"{combo_i} -> {denominator_up} <-{numerator}")
            print("-------------")
            # >(k1 - k2)(k3 - k2)(k1 - k3)(k2 - k3)*(z_k1)*k2*k3
            # print(denominator_up)
            numerator = (numerator * denominator_up) % p
            # print("_____________")
        fc = (fc + numerator) % p

    denominator = 1
    for i in combination:
        for j in combination:
            if j != i:
                denominator = (denominator * (j - i)) % p

    fc = (fc * pow(denominator, -1, p)) % p
    return fc


def calculate_fc_one_inversion_3(combination, coefficient_values, p):
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
    # print(numarator_vector)
    # print(numitor_vector)

    final_numarator = 0
    for index1, numarator_element in enumerate(numarator_vector):
        up_numitor = numarator_element
        for index2, numitor_element in enumerate(numitor_vector):
            if index1 != index2:
                up_numitor = (numitor_element*up_numitor) % p
        up_numitor_vector.append(up_numitor)

    # print(up_numitor_vector)

    final_numitor = 1
    for numitor_element in numitor_vector:
        final_numitor = (final_numitor*numitor_element) % p

    fc = 0
    for element in up_numitor_vector:
        fc = (fc + element) % p

    fc = fc*pow(final_numitor, -1, p)

    return fc % p


if __name__ == '__main__':
    coefficient_index = range(1, 30)
    combinations = list(itertools.combinations(coefficient_index, 10))
    # print(combinations)

    values_vector = ["null"]
    for i in range(1, 1000):
        values_vector.append(random.randint(1, 996))
    # print(values_vector)

    for combo in combinations:
        print(combo)
        start_time = time.time_ns()
        print("Real FC         :", calculate_fc_worst_case(combo, values_vector, 997))
        print("Time: ", time.time_ns() - start_time)
        start_time = time.time_ns()
        print("K Inversions FC :", calculate_fc_k_inversion(combo, values_vector, 997))
        print("Time: ", time.time_ns() - start_time)
        start_time = time.time_ns()
        print("1 Inversion  FC :", calculate_fc_one_inversion_3(combo, values_vector, 997))
        print("Time: ", time.time_ns() - start_time)
        print("__________________")
