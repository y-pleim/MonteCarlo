import numpy

class SpinConfigurationSystem():
    def __init__(self):
        '''
        Creates a SpinConfigurationSystem object containing an empty list.
        '''
        self.collection = []
        

    def initialize(self,N):
        '''
        Populates a SpinConfigurationSystem with all possible SpinConfiguration objects for N sites.
        '''
        for i in range(2**N): # iterates until 2**N, the number of possible configurations for N sites.
            bit_string = numpy.binary_repr(i) # sets the bit_string
            if len(bit_string) < N: # if the binary representation of i has less than N digits
                zero_string = "" # string to be updated
                # adds the necessary number of zeroes to the front of the bit_string:
                for i in range(N-len(bit_string)):
                    zero_string += "0" # adds additional zeroes
                bit_string = zero_string + bit_string
            configuration = SpinConfiguration()
            configuration.initialize(list(bit_string),True)
            self.collection.append(configuration)
            
            
    def __str__(self):
        '''
        Prints the collection of spin configurations contained inside a SpinConfigurationSystem object.
        '''
        sys_string = ""
        for i in range(len(self.collection)):
            sys_string += self.collection[i].__str__() + "\n"
        return sys_string

