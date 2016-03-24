# coding: utf-8

import random
import math
import numpy as np


def setup(l, m, b):
    q = 1
    d = 1
    n = 1
    chi = 1
    N = int(math.ceil((2 * n + 1) * math.log(q, 2)))
    return (q, d, n, N, chi)


def secret_key_gen(params):
    (q, d, n, N, chi) = params
    s = np.random.randint(0, q, n + 1)
    s[0] = 1
    return s


def public_key_gen(params, sk):
    (q, d, n, N, chi) = params
    A = np.random.randint(0, q, N * n)
    A.resize(N, n)
    e = np.random.randint(0, q, N)
    b = np.dot(A, sk[1:]) + 2 * e
    b.resize(N, 1)
    A = np.hstack((b, (-1 * A) % q))
    assert all(np.dot(A, sk) % q == (2 * e) % q)
    return A


def enc(params, pk, m):
    assert m == 0 or m == 1
    (q, d, n, N, chi) = params
    m = np.array([m] + [0] * n)
    r = np.random.randint(0, 2, N)
    c = m + np.dot(pk.T, r)
    return c


def dec(params, sk, c):
    (q, d, n, N, chi) = params
    return (sum(c * sk) % q) % 2
