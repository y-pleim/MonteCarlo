import random

class SpinConfiguration:
    def __init__(self):
        '''
        Creates a SpinConfiguration object with an empty list as its object data.
        '''
        
        self.config = []
    
    def __str__(self):
        '''
        Returns a string containing the entries of self.config when the print function is applied to
        a SpinConfiguration object.
        '''
        
        list_string = "" # string to be filled using for loop
        for i in range(len(self.config)): # executes for every entry in self.config
            if i == len(self.config)-1: # specifies that last entry should be appended to the string with a period
                list_string += str(self.config[i]) + "."
            else:
                list_string += str(self.config[i]) + ", " # separation character between entries is a comma
        return list_string

        
    def initialize(self,order,is_string=False):
        '''
        Allows user to assign a list of 1's (up spin) and 0's (down spin) to a SpinConfiguration object.
        '''
        
        self.config = [] # resets spins list
        if is_string:
            for i in range(len(order)):
                self.config.append(int(order[i]))
        else:
            self.config = order
        
        
    def n_sites(self):
        '''
        Returns the number of sites for the configuration represented by a SpinConfiguration object.
        '''
        
        return len(self.config)
        
        
    def randomize(self,N):
        '''
        Uses the random.choice function to create a randomly generated spin configuration with N sites.
        '''
        self.config = [] # resets spins list
        for i in range(N): # executes N times
            self.config.append(random.choice([0,1])) # randomly adds a 0 or 1 to the end of self.config
    
    def compute_magnetization(self):
        '''
        Computes the magnetization (Number of up spins - Number of down spins) for a SpinConfiguration object passed in
        as an argument.
        '''
    
        n_up = 0 # initializes counter for number of up spins
        n_down = 0 # initializes counter for number of down spins
    
        for i in range(len(self.config)): # cycles through each element in spins.config
            if self.config[i] == 1: # if spin is up
                n_up += 1 # increment n_up
            elif self.config[i] == 0: # if spin is down
                n_down += 1 # increment n_down

        return (n_up - n_down) # return the magnetization of this particular configuration