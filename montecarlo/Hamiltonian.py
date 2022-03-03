import numpy
import matplotlib.pyplot as plt


class Hamiltonian:
    def __init__(self):
        """
        Creates a Hamiltonian object with J = 0, mu = 0, and the periodic boundary conditions set to false.
        """

        self.J = 0
        self.mu = 0
        self.doPeriodicBoundaryConditions = False

    def __str__(self):
        """
        Returns a string to be printed that contains the values associated with a Hamiltonian object.

        Returns
        -------
        ham_message : str
            Contains the values of J/mu and whether periodic boundary conditions are applied..
        """

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
        J : float
            Constant that represents the strength of the coupling term in the Hamiltonian.
        mu : float
            Constant that represents the strength of the external field in the Hamiltonian.
        periodic_flag : bool
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

    # def energy_string_representation(self, spins):
    # energy_string = str(-1 * sum_products) + "J/k + " + str(sum_magnet) + "mu/k"
    # return energy_string

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

    def graph_thermal_quantities(self, system, start=0.1, end=10, step=0.1):
        """
        Produces a graph of the average energy, average magnetization, heat capacity and magnetic
        susceptibility of a spin system over a specified temperature range.

        Parameters
        ----------
        system : SpinConfigurationSystem
            The spin system for which the graph is produced.
        start : float
            The starting temperature value for the graph.
        end : float
            The ending temperature value for the graph.
        step : float
            The spacing between successive temperature values.
        """
        energies = []
        magnetization = []
        heat_capacity = []
        mag_susceptibility = []
        temps = []

        i = start
        while i <= end:
            temps.append(i)
            i += step

        for i in range(len(temps)):
            energies.append(self.compute_average_energy(temps[i], system))
            magnetization.append(self.compute_average_mag(temps[i], system))
            heat_capacity.append(self.compute_heat_capacity(temps[i], system))
            mag_susceptibility.append(self.compute_mag_susceptibility(temps[i], system))

        plt.figure()
        plt.plot(
            temps,
            energies,
            "r-",
            temps,
            magnetization,
            "b-",
            temps,
            heat_capacity,
            "g-",
            temps,
            mag_susceptibility,
            "y-",
        )
        plt.legend(
            [
                "Average Energy",
                "Average Magnetization",
                "Heat Capacity",
                "Mag Susceptibility",
            ],
            loc="best",
        )
        plt.xlabel("Temperature (K)")
