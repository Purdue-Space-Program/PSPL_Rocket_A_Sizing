import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import coding_utils.constants as c
import inputs

import numpy as np
from itertools import product
import numbers

np.set_printoptions(threshold=sys.maxsize)

# Every combination (not sure if thats the right math term) of inputs will make a rocket.
# Each of these rockets and its inputs will be stored as a dictionary in an n-dimensional array,
# where n = # of variable inputs


def dictionary_to_ndarray(dictionary):
    # There are only two scenarios that can be encountered, and it is important to know which one is occurring,
    # An element in the dictionary has:
    # 1. one value, which shall be referred to as "single value elements" or SVE's e.g. ROCKET_OD: [1.3]
    # 2. multiple values, which shall be referred to as "multiple value elements" or MVE's e.g. FUEL_NAME: ["Ethanol", "RP1"]
    

    # Goes through each element of the array to define which datatype (e.g. float or string) should be used in the numpy ndarray
    fields_dtype = []

    # create a dtype list for each of the elements of the array
    for key, value in dictionary.items():
        
        if IsBoolean(value):
            fields_dtype.append((key, "?"))       # 1-byte bool

        # could optimize this by making the field an integer if its an integer but i dont feel like it rn
        elif IsNumberOrListOfNumbers(value):
            fields_dtype.append((key, np.float16))       # 16-bit float

        elif IsStringOrListOfStrings(value):
            # if it is a list, find the longest string that will have to be stored
            if IsAList(value):
                max_length = max(len(s) for s in value)
            else:
                max_length = len(value)
            fields_dtype.append((key, np.str_,max_length))  # String of length = len(value)

        else:
            raise TypeError(f"Unsupported type for key: {key}\n")
    
    # its easier to deal with everything as a list so make every single element a list
    for key, value in dictionary.items():
        if not(IsAList(value)):
            dictionary[key] = [value]


    # use cartesian product to generate all possible combinations
    possible_combinations = list(product(*dictionary.values())) 
    # Shape of this ^ needs to be n-dimensional with size m of each element (each element being a dictionary).
    # This makes it easy to index to find a rocket for a certain input combination
    # n = number of elements
    # m = number of rockets needed to fully explore the range of each "list element" (using step size)
    shape = [FindNumSubElements(variable_input_range) for variable_input_range in dictionary.values()]

    # holy shit i cooked
    ndarray = np.array(possible_combinations, dtype=np.dtype(fields_dtype))
    ndarray = ndarray.reshape(shape)

    # # this doesn't need to be a n-dimensional whatever cause it's going to be the same for every rocket (hence the constant lol)
    # constant_inputs_array = np.array(tuple(inputs.constant_inputs.values()), dtype=np.dtype(constant_inputs_fields_dtype))

    # print(variable_inputs_array)
    # print(variable_inputs_array[0][0]["OF_RATIO"])

    # print(constant_inputs_array)
    # print(constant_inputs_array["PROPELLANT_TANK_OUTER_DIAMETER"])

    return ndarray



def IsAList(unknown_variable):

    num_sub_elements = FindNumSubElements(unknown_variable)
    
    if num_sub_elements > 1:
        return True
    elif num_sub_elements == 1:
        return False
    else:
        raise ValueError(f"what {unknown_variable}")

def FindNumSubElements(unknown_variable):
    num_sub_elements = 0
    
    if isinstance(unknown_variable, (str, int, float)):
        num_sub_elements = 1  
    
    # check for case when sub_elements are in an ndarray
    elif hasattr(unknown_variable, 'dtype'):
        num_sub_elements = unknown_variable.size
    
    else:
         num_sub_elements = len(unknown_variable)
    
    return(num_sub_elements)


def IsBoolean(unknown_variable):
    if isinstance(unknown_variable, bool):
        return(True)

    elif isinstance(unknown_variable, (list, tuple)):
        # check if it is a list of booleans
        return all(isinstance(item, bool) for item in unknown_variable)

    else:
        return False

def IsNumberOrListOfNumbers(unknown_variable):
    # whether the input is a number or a list of numbers the datatype should be stored as a
    # single number since when you iterate through each possible combination you only use one value
    # for each rocket from the range of possible numbers that a variable input can be. For e.g.:
    # "OF_RATIO":           np.linspace(2, 3, step_size),
    # On a single rocket the "OF_RATIO" will be stored as a single value e.g. 2.3

    if isinstance(unknown_variable, numbers.Number):
        return True

    elif isinstance(unknown_variable, (list, tuple)):
        # check if it is a list of numbers
        return all(isinstance(item, numbers.Number) for item in unknown_variable)

    # check first it had a dtype so it doesn't crash when "unknown_variable.dtype" is called
    elif hasattr(unknown_variable, 'dtype'):

        # dont need to check if np value is a number or a list of numbers since "np.issubdtype" returns true either way
        if np.issubdtype(unknown_variable.dtype, np.number):
            return True

    else:
        return False

def IsStringOrListOfStrings(unknown_variable):

    if isinstance(unknown_variable, str):
        return True

    elif isinstance(unknown_variable, (list, tuple)):
        # check if it is a list of strings
        return all(isinstance(item, str) for item in unknown_variable)

        # check first it had a dtype so it doesn't crash when "unknown_variable.dtype" is called
    elif hasattr(unknown_variable, 'dtype'):
        # dont need to check if np value is a string or a list of string since "np.issubdtype" returns true either way
        if np.issubdtype(unknown_variable.dtype, np.str_):
            return True

    else:
        return False


if __name__ == "__main__":
    print(dictionary_to_ndarray(inputs.variable_inputs))