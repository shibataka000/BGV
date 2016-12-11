# coding: utf-8

import math
import numpy as np
import mock

import bgv.basic_encryption_scheme as E
from bgv.key_switching import (
    bit_decomp, powerof2, switch_key_gen, switch_key
)


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
    assert (x0 == x1).all()


def test_lemma_2():
    n = 100
    q = 100
    c = np.random.randint(0, q, n)
    s = np.random.randint(0, q, n)

    left = sum(bit_decomp(c, q) * powerof2(s, q)) % q
    right = sum(c * s) % q
    assert left == right


def test_lemma_3():
    params = (q, d, n, N, chi) = (10, 10, 10, 70, 10)

    params1 = (q1, d1, n1, N1, chi1) = params
    (q1, d1, n1, N1, chi1) = params1
    sk1 = E.secret_key_gen(params1)
    pk1 = E.public_key_gen(params1, sk1)

    params2 = (q2, d2, n2, N2, chi2) = params
    (q2, d2, n2, N2, chi2) = params2
    sk2 = E.secret_key_gen(params2)

    _N2 = (n1 + 1) * math.ceil(math.log(q, 2))
    _params2 = (q2, d2, n2, _N2, chi2)
    pk2 = E.public_key_gen(_params2, sk2)

    with mock.patch("bgv.basic_encryption_scheme", return_value=pk2):
        tau = switch_key_gen(sk1, sk2, params1, params2)

    e2 = np.dot(pk2, sk2) % q

    m = 0
    c1 = E.enc(params1, pk1, m)
    c2 = switch_key(tau, c1, q)

    left = sum(c2 * sk2) % q
    right = (sum(bit_decomp(c1, q) * e2) + sum(c1 * sk1)) % q

    assert left == right
