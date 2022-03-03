"""
Unit and regression test for the montecarlo package.
"""

# Import package, test suite, and other packages as needed
import sys

import pytest

import montecarlo

import random


def test_1():
    assert 1 == 1


def test_montecarlo_imported():
    """Sample test, will always pass so long as import statement worked."""
    assert "montecarlo" in sys.modules


def test_SpinConfiguration():
    conf = montecarlo.SpinConfiguration()
    conf2 = montecarlo.SpinConfiguration()
    random.seed(2)
    conf2.randomize(8)
    conf.initialize([1, 1, 1, 1, 1, 1, 1, 1])

    assert conf.__str__() == "1, 1, 1, 1, 1, 1, 1, 1."
    assert conf.config == [1, 1, 1, 1, 1, 1, 1, 1]
    assert conf.n_sites() == 8
    assert conf.compute_magnetization() == 8
    assert conf2.config == [0, 0, 0, 1, 0, 1, 1, 0]


def test_Hamiltonian():
    ham = montecarlo.Hamiltonian()
    conf = montecarlo.SpinConfiguration()
    conf_sys = montecarlo.SpinConfigurationSystem()
    conf.initialize([1, 1, 1, 1, 1, 1, 1, 1])
    ham.initialize(-2, 1.1, False)
    conf_sys.initialize(2)

    assert ham.compute_energy(conf) == 22.8
    # assert (ham.compute_energy(conf,True) == '-7J/k + 8mu/k')
    assert ham.__str__() == "J = -2, mu = 1.1, Periodic boundary conditions? False"

    ham.initialize(-2, 1.1, True)

    assert ham.compute_energy(conf) == 24.8
    # assert ham.compute_energy(conf,True) == '-8J/k + 8mu/k'
    assert round(ham.compute_average_energy(1, conf_sys), 3) == -3.991
    assert round(ham.compute_average_mag(1, conf_sys), 3) == -0.003
    assert round(ham.compute_heat_capacity(1, conf_sys), 3) == 0.053
    assert round(ham.compute_mag_susceptibility(1, conf_sys), 3) == 0.006


def test_SpinConfigSys():
    conf_sys = montecarlo.SpinConfigurationSystem()
    conf = montecarlo.SpinConfiguration()
    conf_sys.initialize(8)
    conf.initialize([0, 0, 0, 0, 0, 0, 0, 1])
    assert conf_sys.collection[1].config == conf.config
    for i in range(len(conf_sys.collection)):
        assert conf_sys.__str__().count(conf_sys.collection[i].__str__()) == 1
