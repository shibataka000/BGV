# coding: utf-8

import itertools

import numpy as np

import bgv.basic_encryption_scheme as E
from bgv.key_switching import (
    bit_decomp, powerof2, switch_key_gen, switch_key, scale
)


def setup(l, L, b):
    m = 10
    params_list = [E.setup(l, (j + 1) * m, b) for j in range(L + 1)]
    (q_L, d_L, n_L, N_L, chi_L) = params_list[L]
    params_list = [(q, d_L, n, N, chi_L) for (q, d, n, N, chi) in params_list]
    return params_list


def key_gen(params_list, L):
    def tensor(s):
        s2 = [a * b for (a, b) in itertools.combinations(s, 2)]
        return np.array(s2)

    sk_list = []
    pk_list = []

    for j in range(L + 1):
        s_j = E.secret_key_gen(params_list[j])
        A_j = E.public_key_gen(params_list[j], s_j)

        if j > 0:
            params_j = params_list[j]
            (q_j, d_j, n_j, N_j, chi_j) = params_j
            s1_j = tensor(s_j)
            s2_j = bit_decomp(s1_j, q_j)

            params_k = params_list[j - 1]
            s_k = sk_list[j - 1]

            tau_j = switch_key_gen(s2_j, s_k, params_j, params_k)
        else:
            tau_j = None

        sk_list.append(s_j)
        pk_list.append((A_j, tau_j))

    return (sk_list, pk_list)


def enc(params_list, pk_list, m, L):
    params = params_list[L]
    (A, tau) = pk_list[L]
    return E.enc(params, A, m)


def dec(params_list, sk_list, c, j):
    params = params_list[j]
    s = sk_list[j]
    return E.dec(params, s, c)


def add(params_list, pk_list, c1, c2, j):
    (A, tau) = pk_list[j]
    (q_j, d_j, n_j, N_j, chi_j) = params_list[j]
    (q_k, d_k, n_k, N_k, chi_k) = params_list[j - 1]
    c3 = c1 + c2
    refresh(c3, tau, q_j, q_k)
    

def mul(params_list, pk_list, c1, c2, j):
    (A, tau) = pk_list[j]
    (q_j, d_j, n_j, N_j, chi_j) = params_list[j]
    (q_k, d_k, n_k, N_k, chi_k) = params_list[j - 1]
    c3 = c1 + c2
    refresh(c3, tau, q_j, q_k)
    

def refresh(c, tau, q_j, q_k):
    c1 = powerof2(c, q_j)
    c2 = scale(c1, q_j, q_k, 2)
    c3 = switch_key(tau, c2, q_k)
    return c3
