Getting Started
===============

This page details how to get started with MonteCarlo.

Installation
------------
This package was developed for use in Python 3.9. It has the following dependencies:

- numpy

Once the required packages are installed, MonteCarlo can be installed in the environment by using the commands below:

::

 git clone  
 # this is not finished yet

Background
----------
This package is based on a simple, one-dimensional model of magnetism where each site in a material hosts a particle
(typically an electron) with an intrinsic magnetic moment. Such a site can either be spin-up or spin-down. The collection of
spins can be described by a spin configuration, which is a list of the spin value for each site.

The macroscopic properties of the collection of spins are based on the coupling between adjacent spins and the effects
of an external energy bias (e.g., an external magnetic field). The energy of a spin configuration is calculated according
to the Ising Hamiltonian:

.. math:: \frac{H}{k} = -\frac{J}{k}\sum_{<ij>} s_is_j + \frac{\mu}{k}\sum_{i} s_i

Examples
--------
Calculating the energy of a configuration
'''''''''''''''''''''''''''''''''''''''''
The following is an example of how to use this package to calculate the energy of a spin configuration:
::

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

Generating a random spin configuration and additional functions
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The following example demonstrates how to create and print a random spin configuration with N=8 sites. The functionality
of the n_sites method is also demonstrated.
::
 
 import montecarlo
 import random
 
 # Create spin configuration object
 spins = montecarlo.SpinConfiguration()

 # Generate a random spin configuration based on seed value 2
 random.seed(2)
 spins.randomize(8)
 
 # Get number of sites
 num_sites = spins.n_sites()
 
 # Prints output
 print("Spin configuration:", spins)
 print("Number of sites in configuration:", num_sites)
 
This should produce the following:
::
 
 Spin configuration: 0, 0, 0, 1, 0, 1, 1, 0.
 Number of sites in configuration: 8

Calculating average thermal quantities
''''''''''''''''''''''''''''''''''''''
An example of calculating the average energy, average magnetization, heat capacity and magnetic susceptibility
of an N=8 spin system at temperature T = 10K is given below:
::

 import montecarlo
 import numpy as np

 # Create spin configuration system

 spin_system = montecarlo.SpinConfigurationSystem()
 spin_system.initialize(8)

 # Create Hamlitonian
 ham = montecarlo.Hamiltonian()
 ham.initialize(-2,1.1,True)

 # Calculate thermal quantities
 temperature = 10
 avg_energy = ham.compute_average_energy(temperature, spin_system)
 avg_magnetization = ham.compute_average_mag(temperature, spin_system)
 heat_capacity = ham.compute_heat_capacity(temperature, spin_system)
 mag_susceptibility = ham.compute_mag_susceptibility(temperature, spin_system)

 # Prints output
 print("Average Energy:", round(avg_energy,1))
 print("Average Magnetization:", round(avg_magnetization,1))
 print("Heat Capacity:", round(heat_capacity,1))
 print("Magnetic Susceptibility:", round(mag_susceptibility,1))

This should produce the following output:
::
 
 Average Energy: -3.7
 Average Magnetization: -0.6
 Heat Capacity: 0.3
 Magnetic Susceptibility: 0.5

Generating a plot of average thermal quantities
'''''''''''''''''''''''''''''''''''''''''''''''
This example shows how to generate a plot of the average thermal quantities over a specified
temperature range.
::
 
 import montecarlo
 import numpy as np
 import matplotlib.pyplot as plt

 # Create spin configuration system with N = 8 spins
 spin_system = montecarlo.SpinConfigurationSystem()
 spin_system.initialize(8)

 # Create Hamiltonian
 ham = montecarlo.Hamiltonian()
 ham.initialize(-1,1.01,True)

 # Generate lists to be graphed
 temperatures, energies, magnetizations, heat_caps, mag_suscept = ham.generate_thermal_quantities(spin_system,0.1,10,0.1)

 # Creates plot
 plt.plot(
  temperatures, energies, 'r-',
  temperatures, magnetizations, 'b-',
  temperatures, heat_caps, 'g-',
  temperatures, mag_suscept, 'y-'
 )
 plt.legend(["Average Energy", "Average Magnetization", "Heat Capacity", "Mag Susceptibility"],loc='best')
 plt.xlabel("Temperature (K)")
 plt.title("Thermal Quantities vs. Temperature")

This should produce the following plot:

.. image:: ./plot.png
 :width: 400


