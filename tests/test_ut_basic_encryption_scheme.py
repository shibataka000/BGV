# coding: utf-8

import numpy as np
import mock

import bgv.basic_encryption_scheme as E


def randint(low, high, size, dtype="l"):
    return np.array([1 for i in range(size)])


def test_setup():
    pass


def test_secret_key_gen():
    params = (q, d, n, N, chi) = (10, 10, 10, 70, 10)
    with mock.patch("numpy.random.randint", randint):
        sk_exp = np.array([1 for i in range(n + 1)])
        sk_act = E.secret_key_gen(params)
        assert (sk_act == sk_exp).all()


def test_public_key_gen():
    params = (q, d, n, N, chi) = (10, 10, 10, 70, 10)
    with mock.patch("numpy.random.randint", randint):
        sk = E.secret_key_gen(params)
        pk_act = E.public_key_gen(params, sk)
        pk_exp_row = [(n + 2) % q] + [-1 % q] * n
        pk_exp = np.array([pk_exp_row for i in range(N)])
        assert (pk_act == pk_exp).all()


def test_enc():
    params = (q, d, n, N, chi) = (10, 10, 10, 70, 10)
    with mock.patch("numpy.random.randint", randint):
        sk = E.secret_key_gen(params)
        pk = E.public_key_gen(params, sk)

        m = 0
        c_act = E.enc(params, pk, m)
        c_exp = np.array([(m + N * n * 3) % q] + [(-1 * N) % q] * n)
        assert (c_act == c_exp).all()


def test_dec():
    params = (q, d, n, N, chi) = (10, 10, 10, 70, 10)
    with mock.patch("numpy.random.randint", randint):
        sk = E.secret_key_gen(params)
        pk = E.public_key_gen(params, sk)
        m = 0
        c = E.enc(params, pk, m)
        m_dec = E.dec(params, sk, c)
        assert m == m_dec
