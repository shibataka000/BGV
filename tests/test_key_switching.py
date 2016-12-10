# coding: utf-8

import math
import numpy as np
import mock

import bgv.basic_encryption_scheme as E
from bgv.key_switching import (
    bit_decomp, powerof2, switch_key_gen, switch_key
)


def test_whether_value_of_bit_decomp_is_correct():
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


def test_whether_shape_of_bit_decomp_is_correct():
    q = 100
    n = 100
    x0 = np.random.randint(0, q, n)
    u_list = bit_decomp(x0, q)
    assert u_list.size == n * math.ceil(math.log(q, 2))


def test_whether_shape_of_powerof2_is_correct():
    q = 100
    n = 100
    x0 = np.random.randint(0, q, n)
    u_list = powerof2(x0, q)
    assert u_list.size == n * math.ceil(math.log(q, 2))


def test_satisfy_lemma_2():
    n = 100
    q = 100
    c = np.random.randint(0, q, n)
    s = np.random.randint(0, q, n)

    left = sum(bit_decomp(c, q) * powerof2(s, q))
    right = sum(c * s)
    assert left == right


def test_satisfy_lemma_3():
    def randint(low, high, size, dtype="l"):
        return np.array([1 for i in range(size)])

    with mock.patch("numpy.random.randint", randint) as m:
        (l, m, b) = (10, 10, 10)
        params1 = E.setup(l, m, b)
        (q1, d1, n1, N1, chi1) = params1
        sk1 = E.secret_key_gen(params1)
        pk1 = E.public_key_gen(params1, sk1)

        (l, m, b) = (10, 10, 10)
        params2 = E.setup(l, m, b)
        (q2, d2, n2, N2, chi2) = params2
        sk2 = E.secret_key_gen(params2)

        assert q1 == q2
        q = q1

        _N2 = (n1 + 1) * math.ceil(math.log(q, 2))
        _params2 = (q2, d2, n2, _N2, chi2)
        pk2 = E.public_key_gen(_params2, sk2)

        tau = switch_key_gen(sk1, sk2, params1, params2, A=pk2)

        e2 = np.dot(pk2, sk2) % q

        m = 0
        c1 = E.enc(params1, pk1, m)
        c2 = switch_key(tau, c1, q)

        left = sum(c2 * sk2) % q
        right = (sum(bit_decomp(c1, q) * e2) + sum(c1 * sk1)) % q

        assert left == right
