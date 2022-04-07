from .SpinConfiguration import *
from .Hamiltonian import *

def montecarlo_metropolis(N,ham,temp,montecarlo_steps,burn_steps=0):
    spins = SpinConfiguration()
    spins.randomize(N)

    energies = []
    magnetizations = []
    energies_squared = []
    magnetizations_squared = []
          
    for i in range(burn_steps):
        spins = ham.metropolis_sweep(spins,temp)

    for i in range(montecarlo_steps):
        spins = ham.metropolis_sweep(spins,temp)
        E_step = ham.compute_energy(spins)
        M_step = spins.compute_magnetization()

        energies.append(E_step)
        magnetizations.append(M_step)
        energies_squared.append(E_step**2)
        magnetizations_squared.append(M_step**2)
    
    avg_energy = sum(energies)/(montecarlo_steps)
    avg_mag = sum(magnetizations)/(montecarlo_steps)
    avg_energies_squared = sum(energies_squared)/(montecarlo_steps)
    avg_magnetizations_squared = sum(magnetizations_squared)/(montecarlo_steps)
    
    heat_cap = (avg_energies_squared - avg_energy**2) / (temp**2)
    mag_susceptibility = (avg_magnetizations_squared - avg_mag**2) / temp
    return avg_energy, avg_mag, heat_cap, mag_susceptibility
