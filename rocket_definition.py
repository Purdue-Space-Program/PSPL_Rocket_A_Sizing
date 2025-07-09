import coding_utils.constants as c
import inputs as inputs
import numpy as np
import pandas as pd
from itertools import product
import numbers

def CreateEmptyPossibleRocketsArray():

    # Convert the dictionary to a structured data type to make the array more computationally efficient:
    # https://numpy.org/doc/stable/reference/arrays.ndarray.html
    # https://numpy.org/doc/stable/user/basics.rec.html
    variable_dtype_fields = []
    constant_dtype_fields = []

    # Go through each input to define how the field in the dtype should be stored
    for key, value in inputs.variable_inputs.items():
        # print(f"key: {key}, value: {value}")
        # print(type(value))

        if IsBoolean(value):
            variable_dtype_fields.append((key, "?"))       # 1-byte bool
            # print("Its a bool\n")

        # could optimize this by making the field an integer if its an integer but i dont feel like it rn
        elif IsNumberOrListOfNumbers(value):
            # print("It's a number\n")
            variable_dtype_fields.append((key, np.float16))       # 16-bit float

        elif IsStringOrListOfStrings(value):
            # print("Its a string\n")

            # if it is a variable input it is in a list
            if isinstance(value, (list, tuple)):
                max_length = max(len(s) for s in value)
            else:
                max_length = len(value)
            variable_dtype_fields.append((key, np.str_,max_length))  # String of length = len(value)

        else:
            raise TypeError(f"Unsupported type for key: {key}\n")

    # Go through each input to define how the field in the dtype should be stored
    for key, value in inputs.constant_inputs.items():
        # print(f"key: {key}, value: {value}")
        # print(type(value))

        if IsBoolean(value):
            constant_dtype_fields.append((key, "?"))       # 1-byte bool
            # print("Its a bool\n")

        # could optimize this by making the field an integer if its an integer but i dont feel like it rn
        elif IsNumberOrListOfNumbers(value):
            # print("It's a number\n")
            constant_dtype_fields.append((key, np.float16))       # 16-bit float

        elif IsStringOrListOfStrings(value):
            # print("Its a string\n")

            # if it is a variable input it is in a list
            if isinstance(value, (list, tuple)):
                max_length = max(len(s) for s in value)
            else:
                max_length = len(value)
            constant_dtype_fields.append((key, np.str_,max_length))  # String of length = len(value)

        else:
            raise TypeError(f"Unsupported type for variable input: {key}\n")


    possible_combinations = list(product(*inputs.variable_inputs.values())) # use cartesian product to generate all possible combinations of variable inputs
    # Shape of this is ^: n dimensions with size m in each dimension
    # n = number of variable inputs
    # m = number of rockets needed to fully explore the range of each variable input (step size)

    # holy shit i cooked
    variable_inputs_array = np.array(possible_combinations, dtype=np.dtype(variable_dtype_fields))
    print(variable_inputs_array)
    print(variable_inputs_array["CONTRACTION_RATIO"])


    # constant_inputs_array = np.zeros(len(inputs.constant_inputs), dtype=np.dtype(constant_dtype_fields))


    # constant_inputs_array = inputs.constant_inputs




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
    CreateEmptyPossibleRocketsArray()