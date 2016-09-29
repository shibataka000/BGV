# coding: utf-8

import math
import numpy as np


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
    return u_list
