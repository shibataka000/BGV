# coding: utf-8

import math
import numpy as np


from bgv.key_switching import bit_decomp, powerof2


def test_bit_decomp():
    q = 10
    n = 10
    x0 = np.random.randint(0, q, n)
    u_list = bit_decomp(x0, q)
    log_q = math.floor(math.log(q, 2))
    x1 = np.zeros(n)
    for i in range(log_q + 1):
        x1 += (2 ** i) * u_list[i]
    assert all(x0 == x1)


def test_lemma2():
    n = 100
    q = 100
    c = np.random.randint(0, q, n)
    s = np.random.randint(0, q, n)

    u_list = bit_decomp(c, q)
    x_list = powerof2(s, q)
    assert len(u_list) == len(x_list)
    l = len(u_list)
    left = 0
    for i in range(l):
        left += sum(u_list[i] * x_list[i])
    right = sum(c * s)
    assert left == right
