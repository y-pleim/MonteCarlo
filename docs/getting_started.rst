Getting Started
===============

This page details how to get started with MonteCarlo.

Examples
----------
Calculating the energy of a configuration
'''''''''''''''''''''''''''''''''''''''''
The following is an example of how to use this package to calculate the energy of a spin configuration:
::

 import numpy as np
 import montecarlo

 # Create configuration
 spins = montecarlo.SpinConfiguration()
 spins.initialize([0,1,1,1,0,1])

 # Create hamiltonian with desired values of mu, J and the periodic boundary conditions flag
 ham = montecarlo.Hamiltonian()
 ham.initialize(-2,1.1,True)
 
 # Compute energy
 energy = ham.compute_energy(spins)

 print("Spin configuration:", spins)
 print("Energy:", round(energy,1))

This should produce the following output:
::

 Spin configuration: 0, 1, 1, 1, 0, 1.
 Energy: -1.8
