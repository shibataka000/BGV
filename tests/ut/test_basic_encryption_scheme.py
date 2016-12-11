# coding: utf-8

import numpy as np
import mock

import bgv.basic_encryption_scheme as E


def randint(low, high, size, dtype="l"):
    return np.array([1 for i in range(size)])


def create_exp_data():
    params = (q, d, n, N, chi) = (12, 10, 10, 70, 10)
    sk = np.array([1 for i in range(n + 1)])
    pk = np.array([[(n + 2) % q] + [-1 % q] * n for i in range(N)])
    m = 0
    c0 = np.array([(m + N * n * 3) % q] + [(-1 * N) % q] * n)
    m = 1
    c1 = np.array([(m + N * n * 3) % q] + [(-1 * N) % q] * n)
    return (params, sk, pk, c0, c1)


def test_secret_key_gen():
    (params, sk_exp, _, _, _) = create_exp_data()
    with mock.patch("numpy.random.randint", randint):
        sk_act = E.secret_key_gen(params)
        assert (sk_act == sk_exp).all()


def test_public_key_gen():
    (params, sk, pk_exp, _, _) = create_exp_data()
    with mock.patch("numpy.random.randint", randint):
        pk_act = E.public_key_gen(params, sk)
        assert (pk_act == pk_exp).all()


def test_enc():
    (params, _, pk, c0_exp, c1_exp) = create_exp_data()
    with mock.patch("numpy.random.randint", randint):
        c_act = E.enc(params, pk, 0)
        assert (c_act == c0_exp).all()
        c_act = E.enc(params, pk, 1)
        assert (c_act == c1_exp).all()


def test_dec():
    (params, sk, pk, c0, c1) = create_exp_data()
    with mock.patch("numpy.random.randint", randint):
        m_act = E.dec(params, sk, c0)
        assert m_act == 0
        m_act = E.dec(params, sk, c1)
        assert m_act == 1
