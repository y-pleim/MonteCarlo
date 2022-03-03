import random


class SpinConfiguration:
    def __init__(self):
        """
        Creates a SpinConfiguration object with an empty list as its object data.
        """

        self.config = []

    def __str__(self):
        """
        Returns a string that is printed when the print function is applied to
        a SpinConfiguration object.

        Returns
        -------
        list_string : str
            A list of all of the spins represented by the SpinConfiguration object.
        """

        list_string = ""  # string to be filled using for loop
        for i in range(len(self.config)):  # executes for every entry in self.config
            if (
                i == len(self.config) - 1
            ):  # specifies that last entry should be appended to the string with a period
                list_string += str(self.config[i]) + "."
            else:
                list_string += (
                    str(self.config[i]) + ", "
                )  # separation character between entries is a comma
        return list_string

    def initialize(self, order):
        """
        Allows user to assign a list of 1's (up spin) and 0's (down spin) to a SpinConfiguration object.

        Parameters
        ----------
        order : list
            An ordered list of integers where each element is either 0 or 1.
        """

        self.config = []  # resets spins list
        self.config = order

    def n_sites(self):
        """
        Returns the number of sites for the configuration represented by a SpinConfiguration object.

        Returns
        -------
        number_of_sites : int
            The number of entries/sites represented by the SpinConfiguration.
        """
        number_of_sites = len(self.config)
        return number_of_sites

    def randomize(self, N):
        """
        Creates a randomly generated spin configuration with N sites.

        Parameters
        ----------
        N : int
            Number of sites that the SpinConfiguration object should represent.
        """
        self.config = []  # resets spins list
        for i in range(N):  # executes N times
            self.config.append(
                random.choice([0, 1])
            )  # randomly adds a 0 or 1 to the end of self.config

    def compute_magnetization(self):
        """
        Computes the magnetization for the configuration represented by the SpinConfiguration object.

        Returns
        -------
        magnetization : int
            The number of up spins minus the number of down spins.
        """

        n_up = 0  # initializes counter for number of up spins
        n_down = 0  # initializes counter for number of down spins

        for i in range(len(self.config)):  # cycles through each element in spins.config
            if self.config[i] == 1:  # if spin is up
                n_up += 1  # increment n_up
            elif self.config[i] == 0:  # if spin is down
                n_down += 1  # increment n_down
        magnetization = n_up - n_down
        return (
            magnetization  # return the magnetization of this particular configuration
        )