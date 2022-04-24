from .SpinConfiguration import *
from .Hamiltonian import *

def montecarlo_metropolis(N,ham,temp,montecarlo_steps,burn_steps=0):
    '''
    Performs metropolis sampling to determine thermal quantities at the specified temperature
    for an N-spin system described by a particular Hamiltonian.

    Parameters
    ----------
    N : int
        The number of sites in the spin system.
    ham : Hamiltonian
        The Hamiltonian used to describe the spin system.
    temp : float
        The temperature of the spin system.
    montecarlo_steps : int
        The number of times the metropolis sweep is performed and the resulting values are kept.
    burn_steps : int, default: 0
        The number of times the metropolis sweep is performed before values are kept.

    Returns
    -------
    avg_energy : float
        The average of the energy values produced by the kept metropolis sweeps.
    avg_mag : float
        The average of the magnetization values produced by the kept metropolis sweeps.
    heat_cap : float
        The heat capacity derived from the average values produced by the kept metropolis sweeps.
    mag_susceptibility : float
        The magnetic susceptibility derived from the average values produced by the kept metropolis sweeps.
    '''
    # Initialize spin configuration with N sites
    spins = SpinConfiguration()
    spins.randomize(N)

    energies = []
    magnetizations = []
    energies_squared = []
    magnetizations_squared = []
    
    # runs sweep without producing values
    for i in range(burn_steps):
        spins = ham.metropolis_sweep(spins,temp)

    # runs sweep and populates lists
    for i in range(montecarlo_steps):
        spins = ham.metropolis_sweep(spins,temp)
        E_step = ham.compute_energy(spins)
        M_step = spins.compute_magnetization()

        energies.append(E_step)
        magnetizations.append(M_step)
        energies_squared.append(E_step**2)
        magnetizations_squared.append(M_step**2)
    
    # calculates quantities of interest
    avg_energy = sum(energies)/(montecarlo_steps)
    avg_mag = sum(magnetizations)/(montecarlo_steps)
    avg_energies_squared = sum(energies_squared)/(montecarlo_steps)
    avg_magnetizations_squared = sum(magnetizations_squared)/(montecarlo_steps)
    
    heat_cap = (avg_energies_squared - avg_energy**2) / (temp**2)
    mag_susceptibility = (avg_magnetizations_squared - avg_mag**2) / temp
    return avg_energy, avg_mag, heat_cap, mag_susceptibility
