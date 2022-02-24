import numpy
import matplotlib.pyplot as plt

class Hamiltonian:      
    def __init__(self):
        '''
        Creates a Hamiltonian object with J = 0, mu = 0, and the periodic boundary conditions set to false.
        '''
        
        self.J = 0
        self.mu = 0
        self.doPeriodicBoundaryConditions = False
        
        
    def __str__(self):
        '''
        Returns a string providing the value of J/mu associated with a Hamiltonian object when the print
        function is called.
        '''
        
        return "J = " + str(self.J) + "\n mu = " + str(self.mu) + "\n Periodic boundary conditions? " + str(self.doPeriodicBoundaryConditions)
        
    def initialize(self,J,mu,periodic_flag=False):
        '''
        Allows user to pass in a value of J/mu to be stored in the Hamiltonian object and indicate whether 
        the Hamiltonian should use periodic boundary conditions.
        '''
        
        self.J = J
        self.mu = mu
        self.doPeriodicBoundaryConditions = periodic_flag
        
        
    def compute_energy(self,spins,string_representation=False):
        '''
        Computes the energy of a SpinConfiguration object according to the formula given in the markdown text above.
        The string_representation argument controls whether the energy is returned in a string form ("number*J/k") or
        if a numerical approximation is returned.
        '''
        
        BOLTZMANN_CONSTANT = 1 # Boltzmann's constant normalized to 1 (?)
        sum_products = 0 # value to be updated in for loop; represents the result of the sum given above
        sum_magnet = 0
        
        for i in range(len(spins.config)-1): # iterates until the second-to-last element to avoid index error
            if spins.config[i] == spins.config[i+1]: # if spins of adjacent sites match
                sum_products += 1 # adds 1 to the sum_products value
            else: # if spins of adjacent sites do not match
                sum_products += -1 # subtracts 1 from the sum_products value
        
        # checks periodic boundary conditions flag
        if self.doPeriodicBoundaryConditions:
            if spins.config[0] == spins.config[len(spins.config)-1]: # considers last and first spin site
                sum_products += 1
            else:
                sum_products -= 1
        
        for i in range(len(spins.config)): # iterates through spin sites
            if spins.config[i] == 0: # if spin is down
                sum_magnet += -1 # add -1 to sum_magnet
            else: # if spin is up
                sum_magnet += 1 # add 1 to sum_magnet
            
        magnet_contribution = self.mu * sum_magnet # calculates magnetic contribution of H
        coupling_contribution = -self.J * sum_products # calculates coupling contribution of H
                
        if string_representation: # returns string representation
            return str(-1*sum_products) + "J/k + " + str(sum_magnet) + "mu/k"
        else: # returns numerical approximation
            return coupling_contribution + magnet_contribution
        
    def partition_function(self,temp,system):
        '''
        Calculates partition function for a system of spin configurations represented by a particular Hamiltonian
        for a particular temperature (temp).
        '''
        sum_factors = 0 # sum to be updated
        for i in range(len(system.collection)): # for each possible configuration in the system
            boltzmann_factor = numpy.exp(-self.compute_energy(system.collection[i])/temp)
            sum_factors += boltzmann_factor
        return sum_factors

    def compute_average_energy(self,temp,system,z):
        '''
        Calculates average energy for a spin system represented by a particular Hamiltonian.
        '''
        avg_energy = 0
        for i in range(len(system.collection)):
            boltzmann_factor = numpy.exp(-self.compute_energy(system.collection[i])/temp)
            avg_energy += self.compute_energy(system.collection[i],False)*boltzmann_factor
        return (avg_energy / z)

    def compute_average_square_energy(self,temp,system,z):
        '''
        Calculates the average of the squared energy values for a spin system represented by a
        particular Hamiltonian.
        '''
        avg_square_energy = 0
        for i in range(len(system.collection)):
            boltzmann_factor = numpy.exp(-self.compute_energy(system.collection[i])/temp)
            avg_square_energy += (self.compute_energy(system.collection[i]))** 2 * boltzmann_factor
        return (avg_square_energy / z)

    def compute_average_mag(self,temp,system,z):
        '''
        Calculates the average magnetization for a spin system represented by a particular
        Hamiltonian.
        '''
        avg_magnetization = 0
        for i in range(len(system.collection)):
            boltzmann_factor = numpy.exp(-self.compute_energy(system.collection[i])/temp)
            avg_magnetization += system.collection[i].compute_magnetization() * boltzmann_factor
        return (avg_magnetization / z)

    def compute_average_square_mag(self,temp,system,z):
        '''
        Calculates the average of the squared magnetization values for a spin system represented
        by a particular Hamiltonian.
        '''
        avg_square_mag = 0
        for i in range(len(system.collection)):
            boltzmann_factor = numpy.exp(-self.compute_energy(system.collection[i])/temp)
            avg_square_mag += system.collection[i].compute_magnetization() ** 2 * boltzmann_factor
        return (avg_square_mag / z)

    def compute_heat_capacity(self,temp,system,z):
        '''
        Calculates the heat capacity of a spin system represented by a particular Hamiltonian.
        '''
        num = self.compute_average_square_energy(temp,system,z) - self.compute_average_energy(temp,system,z)**2
        return num/pow(temp,2)

    def compute_mag_susceptibility(self,temp,system,z):
        '''
        Calculates the magnetic susceptibility of a spin system represented by a particular Hamiltonian.
        '''
        num = self.compute_average_square_mag(temp,system,z) - self.compute_average_mag(temp,system,z)**2
        return num/temp
    
    def graph_thermal_quantities(self,system, start=0.1, end=10, step=0.1):
        energies = []
        magnetization = []
        heat_capacity = []
        mag_susceptibility = []
        temps = []
        z_list = []

        i = start
        while i <= end:
            temps.append(i)
            i += step

        for temp in temps:
            z_list.append(self.partition_function(temp,system))
    
        for i in range(len(temps)):
            energies.append(self.compute_average_energy(temps[i],system,z_list[i]))
            magnetization.append(self.compute_average_mag(temps[i],system,z_list[i]))
            heat_capacity.append(self.compute_heat_capacity(temps[i],system,z_list[i]))
            mag_susceptibility.append(self.compute_mag_susceptibility(temps[i],system,z_list[i]))


        plt.plot(temps,energies,'r-',temps,magnetization,'b-',temps,heat_capacity,'g-',temps,mag_susceptibility,'y-')
        plt.legend(["Average Energy", "Average Magnetization", "Heat Capacity","Mag Susceptibility"],loc='best')
        plt.xlabel("Temperature (K)")