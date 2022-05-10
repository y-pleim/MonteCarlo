import numpy
import random
import copy as cp


class Hamiltonian:
    def __init__(self):
        """
        Creates a Hamiltonian object with J = 0, mu = 0, and the periodic boundary conditions set to false.
        """

        self.J = 0
        self.mu = 0
        self.doPeriodicBoundaryConditions = False

    def __str__(self):
        ham_message = (
            "J = "
            + str(self.J)
            + ", mu = "
            + str(self.mu)
            + ", Periodic boundary conditions? "
            + str(self.doPeriodicBoundaryConditions)
        )
        return ham_message

    def initialize(self, J=-1.1, mu=1.01, periodic_flag=False):
        """
        Allows user to pass in a value of J/mu to be stored in the Hamiltonian object and indicate whether
        the Hamiltonian should use periodic boundary conditions.

        Parameters
        ----------
        J : float, default: -1.1
            Constant that represents the strength of the coupling term in the Hamiltonian.
        mu : float, default: 1.01
            Constant that represents the strength of the external field in the Hamiltonian.
        periodic_flag : bool, default: False
            Indicates whether periodic boundary conditions are considered when calculating the Hamiltonian.
        """

        self.J = J
        self.mu = mu
        self.doPeriodicBoundaryConditions = periodic_flag

    def compute_energy(self, spins):
        """
        Computes the energy of the spin configuration in the SpinConfiguration object according to the
        Ising Hamiltonian.

        Parameters
        ----------
        spins : SpinConfiguration
            The spin configuration for which the energy should be calculated.

        Returns
        -------
        energy : float
            The energy of the configuration.
        """

        sum_products = 0  # value to be updated in for loop; represents the result of the sum given above
        sum_magnet = 0

        for i in range(
            len(spins.config) - 1
        ):  # iterates until the second-to-last element to avoid index error
            if (
                spins.config[i] == spins.config[i + 1]
            ):  # if spins of adjacent sites match
                sum_products += 1  # adds 1 to the sum_products value
            else:  # if spins of adjacent sites do not match
                sum_products += -1  # subtracts 1 from the sum_products value

        # checks periodic boundary conditions flag
        if self.doPeriodicBoundaryConditions:
            if (
                spins.config[0] == spins.config[len(spins.config) - 1]
            ):  # considers last and first spin site
                sum_products += 1
            else:
                sum_products -= 1

        for i in range(len(spins.config)):  # iterates through spin sites
            if spins.config[i] == 0:  # if spin is down
                sum_magnet += -1  # add -1 to sum_magnet
            else:  # if spin is up
                sum_magnet += 1  # add 1 to sum_magnet

        magnet_contribution = (
            self.mu * sum_magnet
        )  # calculates magnetic contribution of H
        coupling_contribution = (
            -self.J * sum_products
        )  # calculates coupling contribution of H
        energy = coupling_contribution + magnet_contribution
        return energy

    def partition_function(self, temp, system):
        """
        Evaluates the partition function for a system of spin configurations represented by a particular
        Hamiltonian at a particular temperature.

        Parameters
        ----------
        temp : float
            Temperature of the system.
        system : SpinConfigurationSystem
            The spin configuration system for which the partition function is evaluated.

        Returns
        -------
        sum_factors : float
            The sum of the Boltzmann factors, i.e. the value of the partition function for the chosen temperature.
        """
        sum_factors = 0  # sum to be updated
        for i in range(
            len(system.collection)
        ):  # for each possible configuration in the system
            boltzmann_factor = numpy.exp(
                -self.compute_energy(system.collection[i]) / temp
            )
            sum_factors += boltzmann_factor
        return sum_factors

    def compute_average_energy(self, temp, system):
        """
        Calculates average energy for a spin system represented by a particular Hamiltonian.

        Parameters
        ----------
        temp : float
            Temperature of the system.
        system : SpinConfigurationSystem
            The spin system for which the average energy is calculated.

        Returns
        -------
        avg_energy : float
            The average energy of the system for the chosen temperature.
        """
        z = self.partition_function(temp, system)
        sum_products = 0
        for i in range(len(system.collection)):
            boltzmann_factor = numpy.exp(
                -self.compute_energy(system.collection[i]) / temp
            )
            sum_products += self.compute_energy(system.collection[i]) * boltzmann_factor
        avg_energy = sum_products / z
        return avg_energy

    def compute_average_square_energy(self, temp, system):
        """
        Calculates the average of the squared energy values for a spin system represented by a
        particular Hamiltonian at the specified temperature.

        Parameters
        ----------
        temp : float
            Temperature of the system.
        system : SpinConfigurationSystem
            The spin system for which the average of the squared energies is calculated.

        Returns
        -------
        avg_square_energy : float
            The average of the squared energies of the system for the chosen temperature.
        """
        z = self.partition_function(temp, system)
        sum_products = 0
        for i in range(len(system.collection)):
            boltzmann_factor = numpy.exp(
                -self.compute_energy(system.collection[i]) / temp
            )
            sum_products += (
                self.compute_energy(system.collection[i])
            ) ** 2 * boltzmann_factor
        avg_square_energy = sum_products / z
        return avg_square_energy

    def compute_average_mag(self, temp, system):
        """
        Calculates the average magnetization for a spin system represented by a particular
        Hamiltonian at the specified temperature.

        Parameters
        ----------
        temp : float
            Temperature of the system.
        system : SpinConfigurationSystem
            The spin system for which the average magnetization is calculated.

        Returns
        -------
        avg_magnetization : float
            The average magnetization of the system for the chosen temperature.
        """
        z = self.partition_function(temp, system)
        sum_products = 0
        for i in range(len(system.collection)):
            boltzmann_factor = numpy.exp(
                -self.compute_energy(system.collection[i]) / temp
            )
            sum_products += (
                system.collection[i].compute_magnetization() * boltzmann_factor
            )
        avg_magnetization = sum_products / z
        return avg_magnetization

    def compute_average_square_mag(self, temp, system):
        """
        Calculates the average of the squared magnetization values for a spin system represented
        by a particular Hamiltonian at the specified temperature.

        Parameters
        ----------
        temp : float
            Temperature of the system.
        system : SpinConfigurationSystem
            The spin system for which the average of the square magnetizations is calculated.

        Returns
        -------
        avg_square_mag : float
            The average of the squared magnetizations of the system for the chosen temperature.

        """
        z = self.partition_function(temp, system)
        sum_products = 0
        for i in range(len(system.collection)):
            boltzmann_factor = numpy.exp(
                -self.compute_energy(system.collection[i]) / temp
            )
            sum_products += (
                system.collection[i].compute_magnetization() ** 2 * boltzmann_factor
            )
        avg_square_mag = sum_products / z
        return avg_square_mag

    def compute_heat_capacity(self, temp, system):
        """
        Calculates the heat capacity of a spin system represented by a particular Hamiltonian at
        the specified temperature.

        Parameters
        ----------
        temp : float
            Temperature of the system.
        system : SpinConfigurationSystem
            The spin system for which the heat capacity is calculated.

        Returns
        -------
        heat_capacity : float
            The value of the heat capacity at the specified temperature.
        """
        difference = self.compute_average_square_energy(temp, system) - pow(
            self.compute_average_energy(temp, system), 2
        )
        heat_capacity = difference / pow(temp, 2)
        return heat_capacity

    def compute_mag_susceptibility(self, temp, system):
        """
        Calculates the magnetic susceptibility of a spin system represented by a particular Hamiltonian at
        the specified temperature.

        Parameters
        ----------
        temp : float
            Temperature of the system.
        system : SpinConfigurationSystem
            The spin system for which the magnetic susceptibility is calculated.

        Returns
        -------
        mag_susceptibility : float
            The value of the magnetic susceptibility at the specified temperature.
        """
        difference = (
            self.compute_average_square_mag(temp, system)
            - self.compute_average_mag(temp, system) ** 2
        )
        mag_susceptibility = difference / temp
        return mag_susceptibility

    def generate_thermal_quantities(self, system, start=0.1, end=10, step=0.1):
        """
        Produces lists of the average energy, average magnetization, heat capacity and magnetic
        susceptibility values of a spin system over a specified temperature range.

        Parameters
        ----------
        system : SpinConfigurationSystem
            The spin system for which the data lists are produced.
        start : float, default: 0.1
            The starting temperature value for the graph.
        end : float, default: 10
            The ending temperature value for the graph.
        step : float, default: 0.1
            The spacing between successive temperature values.

        Returns
        -------
        temps_list : list
            The list of temperatures generated from the start, end, and step values.
        energies_list : list
            The list of average energies for the temperatures considered.
        magnetization_list : list
            The list of average magnetization values for the temperatures considered.
        heat_capacity_list : list
            The list of heat capacity values for the temperatures considered.
        mag_susceptibility_list : list
            The list of magnetic susceptibility values for the temperatures considered.

        """
        energies_list = []
        magnetization_list = []
        heat_capacity_list = []
        mag_susceptibility_list = []
        temps_list = []

        i = start
        # populates temperature list
        while i < end:
            temps_list.append(i)
            i += step

        # populates lists of thermal quantities
        for i in range(len(temps_list)):
            energies_list.append(self.compute_average_energy(temps_list[i], system))
            magnetization_list.append(self.compute_average_mag(temps_list[i], system))
            heat_capacity_list.append(self.compute_heat_capacity(temps_list[i], system))
            mag_susceptibility_list.append(
                self.compute_mag_susceptibility(temps_list[i], system)
            )

        return (
            temps_list,
            energies_list,
            magnetization_list,
            heat_capacity_list,
            mag_susceptibility_list,
        )

    def metropolis_sweep(self, spins, temp):
        """
        Performs a metropolis sweep starting from the SpinConfiguration object passed in.

        Parameters
        ----------
        spins : SpinConfiguration
            The spin configuration that serves as the starting point for the metropolis sweep.
        temp : float
            The temperature of the system.

        Returns
        -------
        new_spins : SpinConfiguration
            The most probable spin configuration resulting from the metropolis sweep.

        """
        for i in range(spins.n_sites()):  # for each site in the lattice
            conf = cp.deepcopy(spins)  # copies the result of the previous iteration

            # flips spin at site i
            if spins[i] == 0:
                conf.set_site(i, 1)
            else:
                conf.set_site(i, 0)

            J_term = (
                0  # value that reflects the change in the J term in the Hamiltonian
            )
            mu_term = (
                0  # value that reflects the change in the mu term in the Hamiltonian
            )

            # logic for changing J_term and mu_term
            if self.doPeriodicBoundaryConditions:
                if i == 0:  # compares spin at first site to adjacent spins
                    if conf[len(conf.config) - 1] == conf[i] and conf[i] == conf[1]:
                        J_term = 4
                    elif conf[len(conf.config) - 1] == conf[1]:
                        J_term = -4
                elif (
                    i == len(conf.config) - 1
                ):  # compares spin at last site to adjacent spins
                    if conf[i - 1] == conf[i] and conf[i] == conf[0]:
                        J_term = 4
                    elif conf[i - 1] == conf[0]:
                        J_term = -4
                else:  # compares spin at any other site to adjacent spins
                    if conf[i - 1] == conf[i] and conf[i] == conf[i + 1]:
                        J_term = 4
                    elif conf[i - 1] == conf[i + 1]:
                        J_term = -4
            else:
                if i == 0:  # compares spin at first site to spin at second site
                    if conf[i] == conf[1]:
                        J_term = 2
                    else:
                        J_term = -2
                elif (
                    i == len(conf.config) - 1
                ):  # compares spin at last site to spin before it
                    if conf[i - 1] == conf[i]:
                        J_term = 2
                    else:
                        J_term = -2
                else:  # compares spin at any other site to adjacent spins
                    if conf[i - 1] == conf[i] and conf[i] == conf[i + 1]:
                        J_term = 4
                    elif conf[i - 1] == conf[i + 1]:
                        J_term = -4

            if conf[i] == 0:  # if the spin has been flipped from up to down
                mu_term = -2
            else:  # if the spin has been flipped from down to up
                mu_term = 2

            # calculates change in energy after spin flip
            deltaE = -J_term * self.J + mu_term * self.mu

            check_num = random.random()
            probability = numpy.exp(
                -deltaE / temp
            )  # ratio of Boltzmann factors of final and initial state

            if probability > check_num:  # if the flip is deemed energetically favorable
                spins = cp.deepcopy(
                    conf
                )  # store the reference to the new SpinConfiguration in the spins variable
        new_spins = spins
        return new_spins
