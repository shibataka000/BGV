# coding: utf-8

import bgv.fhe_scheme as FHE


def test_decrypt():
    (l, L, b) = (10, 10, 10)
    params = FHE.setup(l, L, b)
    (sk, pk) = FHE.key_gen(params, L)
    m = 0
    c = FHE.enc(params, pk, m, L)
    assert m == FHE.dec(params, sk, c, L)
    m = 1
    c = FHE.enc(params, pk, m, L)
    assert m == FHE.dec(params, sk, c, L)
