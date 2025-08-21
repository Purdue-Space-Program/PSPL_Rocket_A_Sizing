# Main
# Owners: David Gustafsson

#    _      _      _      _      _      _      _      _      _      _      _      _      _      _
#  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_
# (_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)
#  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)
#    _                                                                                          _
#  _( )_     ____    _                          _____   _   _                                 _( )_
# (_ o _)   / ___|  (_)  ____   ___   _   _    |  ___| | | (_)   ___   ___    ___   _   _    (_ o _)
#  (_,_)    \___ \  | | |_  /  / _ \ | | | |   | |_    | | | |  / _ \ / __|  / _ \ | | | |    (_,_)
#    _       ___) | | |  / /  |  __/ | |_| |   |  _|   | | | | |  __/ \__ \ |  __/ | |_| |      _
#  _( )_    |____/  |_| /___|  \___|  \__, |   |_|     |_| |_|  \___| |___/  \___|  \__, |    _( )_
# (_ o _)                             |___/                                         |___/    (_ o _)
#  (_,_)                                                                                      (_,_)
#    _      _      _      _      _      _      _      _      _      _      _      _      _      _
#  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_  _( )_
# (_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)(_ o _)
#  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)  (_,_)

from vehicle_scripts import (
    engine,
    numpy_ndarray_handler,
    # tanks,
    # structures,
    # trajectory
)
import inputs
import coding_utils.constants as c
import numpy as np
import matplotlib.pyplot as plt


# Converting the dictionary to a structured numpy array is more computationally efficient:
# https://numpy.org/doc/stable/reference/arrays.ndarray.html
# https://numpy.org/doc/stable/user/basics.rec.html
# good visual: https://www.w3resource.com/numpy/ndarray/index.php

# The variable_inputs_array will be separate from the constant_inputs_array to save memory size and hopefully increase speed

variable_inputs_array = numpy_ndarray_handler.dictionary_to_ndarray(inputs.variable_inputs)
constant_inputs_array = numpy_ndarray_handler.dictionary_to_ndarray(inputs.constant_inputs)

# print(variable_inputs_array.shape)
# # Iterate while keeping the structure
# it = np.nditer(variable_inputs_array, flags=["multi_index"], op_flags=["readonly"])
# for variable_input_combination in it: 
#     # print(f"{it.multi_index}: {variable_input_combination}")
    
#     thrust_lbf = engine.ThrustyBusty(
#                   constant_inputs_array["FUEL_NAME"], 
#                   # variable_input_combination["FUEL_NAME"],
                  
#                   constant_inputs_array["OXIDIZER_NAME"],
#                   constant_inputs_array["PROPELLANT_TANK_OUTER_DIAMETER"],
                  
#                   constant_inputs_array["CONTRACTION_RATIO"],
#                   # variable_input_combination["CONTRACTION_RATIO"],
                 
#                   variable_input_combination["OF_RATIO"],
#                   variable_input_combination["CHAMBER_PRESSURE"],
#                  ) * c.N2LBF
#     # print(thrust_lbf)
    
    
    
    
thrust_map = []

# Iterate while keeping the structure
it = np.nditer(variable_inputs_array, flags=["multi_index"], op_flags=["readonly"])
for variable_input_combination in it: 
    thrust_lbf = engine.ThrustyBusty(
                constant_inputs_array["FUEL_NAME"], 
                # variable_input_combination["FUEL_NAME"],
                
                constant_inputs_array["OXIDIZER_NAME"],
                constant_inputs_array["PROPELLANT_TANK_OUTER_DIAMETER"],
                
                # constant_inputs_array["CONTRACTION_RATIO"],
                variable_input_combination["CONTRACTION_RATIO"],
                
                variable_input_combination["OF_RATIO"],
                
                # constant_inputs_array["CHAMBER_PRESSURE"].item(),
                variable_input_combination["CHAMBER_PRESSURE"],
                ) * c.N2LBF
    thrust_map.append(thrust_lbf)
    print(f"{it.multi_index}: {variable_input_combination} -> {thrust_lbf}")

x = np.array(variable_inputs_array[0, :]["CHAMBER_PRESSURE"])
y = np.array(variable_inputs_array[:, 0]["OF_RATIO"])
z = np.array(thrust_map)

Y, X = np.meshgrid(x, y) # I don't know why you have to swap X and Y but you do
Z = z.reshape(len(x), len(y))

# plt.pcolormesh(X, Y, Z, cmap='Spectral_r')
plt.contourf(X, Y, Z, 100, cmap='Spectral_r')

plt.colorbar(label='Thrust [lbf]')
plt.xlabel('OF Ratio')
plt.ylabel('Chamber Pressure [psi]')

plt.show()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# chat gpt shit

# Assume variable_inputs_array.shape = (n_pressures, n_of_ratios)
# n_pressures = variable_inputs_array.shape[0]
# n_of_ratios = variable_inputs_array.shape[1]

# # Initialize a 2D array to hold thrust
# thrust_map = np.zeros((n_pressures, n_of_ratios))

# # Fill the thrust_map
# for i in range(n_pressures):
#     for j in range(n_of_ratios):
#         combo = variable_inputs_array[i, j]
#         thrust_map[i, j] = engine.ThrustyBusty(
#             constant_inputs_array["FUEL_NAME"],
#             constant_inputs_array["OXIDIZER_NAME"],
#             constant_inputs_array["PROPELLANT_TANK_OUTER_DIAMETER"],
#             constant_inputs_array["CONTRACTION_RATIO"],
#             combo["OF_RATIO"],
#             combo["CHAMBER_PRESSURE"]
#         ) * c.N2LBF
        
        
# # Assuming chamber pressures vary along axis 0 and OF_ratios along axis 1
# chamber_pressures = np.array([variable_inputs_array[i,0]["CHAMBER_PRESSURE"] for i in range(n_pressures)])
# of_ratios = np.array([variable_inputs_array[0,j]["OF_RATIO"] for j in range(n_of_ratios)])


# plt.figure(figsize=(8,6))
# plt.imshow(thrust_map, origin='lower', 
#            aspect='auto', cmap='viridis')
# plt.colorbar(label='Thrust [lbf]')
# plt.xlabel('O/F Ratio')
# plt.ylabel('Chamber Pressure [Pa]')  # change units if needed
# plt.title('Thrust vs O/F Ratio and Chamber Pressure')
# plt.show()
