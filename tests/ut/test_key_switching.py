# coding: utf-8

import math
import numpy as np
import mock

import bgv.basic_encryption_scheme as E
from bgv.key_switching import (
    bit_decomp, powerof2, switch_key_gen, switch_key
)


def randint(low, high, size, dtype="l"):
    return np.array([1 for i in range(size)])


def test_whether_value_of_bit_decomp_is_correct():
    q = 3
    n = 3
    x0 = np.array([i % q for i in range(n)])
    u_list_act = bit_decomp(x0, q)
    u_list_exp = np.array([0, 1, 0, 0, 0, 1])
    assert (u_list_exp == u_list_act).all()


def test_whether_shape_of_bit_decomp_is_correct():
    q = 100
    n = 100
    x0 = np.array([i % q for i in range(n)])
    u_list = bit_decomp(x0, q)
    assert u_list.size == n * math.ceil(math.log(q, 2))


def test_whether_value_of_powerof2_is_correct():
    q = 3
    n = 3
    x0 = np.array([i % q for i in range(n)])
    u_list_act = powerof2(x0, q)
    u_list_exp = np.array([0, 1, 2, 0, 2, 1])
    assert (u_list_exp == u_list_act).all()


def test_whether_shape_of_powerof2_is_correct():
    q = 100
    n = 100
    x0 = np.array([i % q for i in range(n)])
    u_list = powerof2(x0, q)
    assert u_list.size == n * math.ceil(math.log(q, 2))


def test_switch_key_gen():
    with mock.patch("numpy.random.randint", randint):
        params = (q, d, n, N, chi) = (10, 10, 10, 70, 10)

        params1 = (q1, d1, n1, N1, chi1) = params
        sk1 = E.secret_key_gen(params1)

        params2 = (q2, d2, n2, N2, chi2) = params
        sk2 = E.secret_key_gen(params2)

        tau = switch_key_gen(sk1, sk2, params1, params2)

        _N2 = (n1 + 1) * math.ceil(math.log(q, 2))

        po2 = sorted([1, 2, 4, 8] * (n2 + 1))
        po2 = np.array(po2) + 2 + n2
        po2.resize((_N2, 1))
        A = np.array([-1] * (_N2 * n2))
        A.resize((_N2, n2))
        B = np.hstack((po2, A)) % q

        assert (tau == B).all()


def test_switch_key():
    with mock.patch("numpy.random.randint", randint):
        params = (q, d, n, N, chi) = (10, 10, 10, 70, 10)

        params1 = (q1, d1, n1, N1, chi1) = params
        sk1 = E.secret_key_gen(params1)
        pk1 = E.public_key_gen(params1, sk1)

        params2 = (q2, d2, n2, N2, chi2) = params
        sk2 = E.secret_key_gen(params2)

        tau = switch_key_gen(sk1, sk2, params1, params2)
        c1 = E.enc(params1, pk1, 1)
        c2 = switch_key(tau, c1, q)

        bd = bit_decomp(c1, q)
        exp = [(n2 + 2) * sum(bd) + sum(c1 * sk1)] + [-1 * sum(bd)] * n2
        exp = np.array(exp) % q

        assert (c2 == exp).all()
