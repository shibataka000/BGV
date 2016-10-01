# coding: utf-8

import math
import numpy as np


from bgv.key_switching import bit_decomp, powerof2


def test_bit_decomp():
    q = 100
    n = 100
    x0 = np.random.randint(0, q, n)
    u_list = bit_decomp(x0, q)
    log_q = math.floor(math.log(q, 2))
    x1 = np.zeros(n)
    for j in range(log_q + 1):
        for i in range(n):
            x1[i] += (2 ** j) * u_list[j * n + i]
    assert all(x0 == x1)


def test_lemma2():
    n = 100
    q = 100
    c = np.random.randint(0, q, n)
    s = np.random.randint(0, q, n)

    left = sum(bit_decomp(c, q) * powerof2(s, q))
    right = sum(c * s)
    assert left == right
