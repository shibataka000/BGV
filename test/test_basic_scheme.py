# coding: utf-8

import bgv.basic_scheme as E


def test_basic_schema():
    params = E.setup(1, 1, 1)
    sk = E.secret_key_gen(params)
    pk = E.public_key_gen(params, sk)
    c0 = E.enc(params, pk, 0)
    assert E.dec(params, sk, c0) == 0
    c1 = E.enc(params, pk, 1)
    assert E.dec(params, sk, c1) == 1
