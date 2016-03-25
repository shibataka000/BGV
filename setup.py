# coding: utf-8

from setuptools import setup, find_packages

setup(
    name = "bgv",
    version = "0.1",
    packages = find_packages(),
    install_requires = ["numpy"],
    test_suite = "test"
)
