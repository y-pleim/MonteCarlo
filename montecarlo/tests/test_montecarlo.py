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

    # Initialize spin configurations
    random.seed(2)
    conf2.randomize(8)
    conf.initialize([1, 1, 1, 1, 1, 1, 1, 1])

    assert conf[0] == 1  # checks __getitem__ method
    assert str(conf) == "1, 1, 1, 1, 1, 1, 1, 1."  # checks __str__ method
    assert conf.get_spins() == [1, 1, 1, 1, 1, 1, 1, 1]  # checks get_spins
    assert conf.n_sites() == 8  # checks n_sites
    assert conf.compute_magnetization() == 8  # checks magnetization calculation
    assert conf2.get_spins() == [0, 0, 0, 1, 0, 1, 1, 0]  # checks randomize output

    conf.set_site(2, 0)  # sets site at index 2 to 0
    assert conf.get_spins() == [1, 1, 0, 1, 1, 1, 1, 1]  # checks set_site method

    # testing that an error is raised by set_site when a bad input is inserted
    # test function based on Python error-handling docs
    def test():
        try:
            conf.set_site(2, "test")
        finally:
            return 1

    assert test() == 1  # checks that an error has occurred


def test_Hamiltonian():
    ham = montecarlo.Hamiltonian()
    conf = montecarlo.SpinConfiguration()
    conf_sys = montecarlo.SpinConfigurationSystem()
    conf.initialize([1, 1, 1, 1, 1, 1, 1, 1])
    ham.initialize(-2, 1.1, False)
    conf_sys.initialize(2)

    assert (
        ham.compute_energy(conf) == 22.8
    )  # checks compute_energy for no periodic boundary conditions
    assert (
        str(ham) == "J = -2, mu = 1.1, Periodic boundary conditions? False"
    )  # checks __str__ method

    ham.initialize(-2, 1.1, True)  # turns on PBC

    assert ham.compute_energy(conf) == 24.8  # checks compute_energy for PBC
    assert (
        round(ham.compute_average_energy(1, conf_sys), 3) == -3.991
    )  # checks compute_average_energy
    assert (
        round(ham.compute_average_mag(1, conf_sys), 3) == -0.003
    )  # checks compute_average_mag
    assert (
        round(ham.compute_heat_capacity(1, conf_sys), 3) == 0.053
    )  # checks compute_heat_capacity
    assert (
        round(ham.compute_mag_susceptibility(1, conf_sys), 3) == 0.006
    )  # checks compute_mag_susceptibility

    (
        temps,
        energies,
        magnetizations,
        heat_caps,
        mag_suscept,
    ) = ham.generate_thermal_quantities(conf_sys)

    # checks generate_thermal_quantities method:
    assert round(temps[9], 1) == 1.0
    assert round(energies[9], 3) == -3.991
    assert round(magnetizations[9], 3) == -0.003
    assert round(heat_caps[9], 3) == 0.053
    assert round(mag_suscept[9], 3) == 0.006

    # checks metropolis_sweep for PBC and no PBC:
    random.seed(2)
    conf.randomize(8)

    conf2 = ham.metropolis_sweep(conf, 1)
    assert conf2.get_spins() == [1, 0, 0, 1, 0, 0, 1, 0]

    ham.initialize(-2, 1.1, False)
    conf2 = ham.metropolis_sweep(conf, 1)
    assert conf2.get_spins() == [1, 0, 0, 1, 0, 0, 1, 0]

    conf.initialize([1, 1, 0, 1, 0, 0, 0, 1])
    random.seed(2)
    conf2 = ham.metropolis_sweep(conf, 1)
    assert conf2.get_spins() == [0, 1, 0, 1, 0, 1, 0, 1]

    conf.initialize([0, 1, 0, 1, 0, 0, 0, 0])
    random.seed(2)
    conf2 = ham.metropolis_sweep(conf, 1)
    assert conf2.get_spins() == [0, 1, 0, 1, 0, 1, 0, 1]

    # checks the average thermal quantity calculations for no PBC
    conf_sys.initialize(8)
    assert round(ham.compute_average_energy(10, conf_sys), 1) == -3.3
    assert round(ham.compute_average_mag(10, conf_sys), 1) == -0.6
    assert round(ham.compute_heat_capacity(10, conf_sys), 1) == 0.3
    assert round(ham.compute_mag_susceptibility(10, conf_sys), 1) == 0.6


def test_SpinConfigSys():
    conf_sys = montecarlo.SpinConfigurationSystem()
    conf = montecarlo.SpinConfiguration()
    conf_sys.initialize(8)
    conf.initialize([0, 0, 0, 0, 0, 0, 0, 1])
    assert conf_sys[1] == conf.get_spins()  # checks __getitem__ method
    # checks that each str(configuration) appears in str(configuration_system)
    for i in range(len(conf_sys.collection)):
        assert str(conf_sys).count(str(conf_sys.collection[i])) == 1


def test_montecarlo_metropolis():
    ham = montecarlo.Hamiltonian()
    ham.initialize(-2, 1.1, True)
    random.seed(2)

    # checks montecarlo_metropolis for 10000 montecarlo steps, 1000 burned steps
    energy, mag, heat_cap, mag_sust = montecarlo.montecarlo_metropolis(
        8, ham, 10, 10000, 1000
    )
    assert round(energy, 2) == -3.90
    assert round(mag, 2) == -0.57
    assert round(heat_cap, 2) == 0.32
    assert round(mag_sust, 2) == 0.51

    random.seed(2)
    # checks the generate_montecarlo_thermal_quantities method
    (
        temps,
        energies,
        magnetizations,
        heat_caps,
        mag_susts,
    ) = montecarlo.generate_montecarlo_thermal_quantities(8, ham, 9)
    index = len(temps) - 1

    assert round(temps[index], 1) == 10
    assert round(energies[index], 0) == -4
    assert round(magnetizations[index], 0) == -1
    assert round(heat_caps[index], 0) == 0
    assert round(mag_susts[index], 0) == 1
