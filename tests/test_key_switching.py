# coding: utf-8

import math
import numpy as np


from bgv.key_switching import bit_decomp


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

