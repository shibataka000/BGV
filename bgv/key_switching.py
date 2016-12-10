# coding: utf-8

import math
import numpy as np

import bgv.basic_encryption_scheme as E


def bit_decomp(x, q):
    def dec2bin(n, digit):
        b = format(n, "b")
        b = "0" * (digit - len(b)) + b
        return b

    log_q = math.floor(math.log(q, 2))
    u_list = []
    for i in range(log_q + 1):
        digit = log_q + 1
        index = digit - i - 1
        u = [dec2bin(n, digit)[index] for n in x]
        u = np.array([int(n) for n in u])
        u_list.append(u)
    return np.hstack(tuple(u_list))


def powerof2(x, q):
    log_q = math.floor(math.log(q, 2))
    x_list = []
    for i in range(log_q + 1):
        new_x = (2 ** i) * x
        x_list.append(new_x)
    return np.hstack(tuple(x_list))


def switch_key_gen(s1, s2, params1, params2):
    (q1, d1, n1, N1, chi1) = params1
    (q2, d2, n2, N2, chi2) = params2
    assert q1 == q2
    q = q1
    N2 = n1 * math.ceil(math.log(q, 2))
    N2 = (n1 + 1) * math.ceil(math.log(q, 2))
    params2 = (q2, d2, n2, N2, chi2)

    A = E.public_key_gen(params2, s2)
    B = np.array(A)
    B[:, 0] += powerof2(s1, q)
    return B


def switch_key(tau, c1, q):
    c1t = np.transpose(bit_decomp(c1, q))
    c2 = np.dot(c1t, tau)
    return c2
