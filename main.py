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
step_size = inputs.step_size

# Converting the dictionary to a structured numpy array is more computationally efficient:
# https://numpy.org/doc/stable/reference/arrays.ndarray.html
# https://numpy.org/doc/stable/user/basics.rec.html
# good visual: https://www.w3resource.com/numpy/ndarray/index.php

# The variable_inputs_array will be separate from the constant_inputs_array to save memory size and hopefully increase speed

variable_inputs_array = numpy_ndarray_handler.dictionary_to_ndarray(inputs.variable_inputs)
constant_inputs_array = numpy_ndarray_handler.dictionary_to_ndarray(inputs.constant_inputs)




from sys import getsizeof
from tqdm import tqdm

print(f"variable_inputs_array: shape: {variable_inputs_array.shape}, bytes: {variable_inputs_array.nbytes}")

AI_SLOP = True # god help me

if AI_SLOP:

    from concurrent.futures import ThreadPoolExecutor, as_completed

    def compute_thrust(idx, variable_input_combination):
        # Do imports inside the worker (not passed in)
        from vehicle_scripts import engine
        from coding_utils import constants as c
        from inputs import constant_inputs as constant_inputs_dict

        thrust_newton, mass_flow_kg, isp = engine.ThrustyBusty(
                    constant_inputs_array["FUEL_NAME"], 
                    # variable_input_combination["FUEL_NAME"],
                    
                    constant_inputs_array["OXIDIZER_NAME"],
                    constant_inputs_array["PROPELLANT_TANK_OUTER_DIAMETER"],
                    
                    constant_inputs_array["CONTRACTION_RATIO"],
                    # variable_input_combination["CONTRACTION_RATIO"],
                    
                    variable_input_combination["OF_RATIO"],
                    
                    # constant_inputs_array["CHAMBER_PRESSURE"].item(),
                    variable_input_combination["CHAMBER_PRESSURE"],
                    )
        
        return idx, thrust_newton * c.N2LBF, mass_flow_kg, isp



    jobs = []
    it = np.nditer(variable_inputs_array, flags=["multi_index"], op_flags=["readonly"])
    for variable_input_combination in it: 
        jobs.append((it.multi_index, variable_input_combination.copy()))

    thrust_map = np.zeros(variable_inputs_array.size)
    mass_flow_map = np.zeros(variable_inputs_array.size)
    isp_map = np.zeros(variable_inputs_array.size)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(compute_thrust, idx, v) for idx, v in jobs]
        for f in tqdm(as_completed(futures), total=len(futures), desc="Computing thrust"):
            idx, thrust, mass_flow, isp = f.result()
            thrust_map[(idx[0])*step_size + idx[1]] = thrust
            mass_flow_map[(idx[0])*step_size + idx[1]] = mass_flow
            isp_map[(idx[0])*step_size + idx[1]] = isp
            # print(f"{idx}: {thrust}")
            # print(f"{idx}: {variable_inputs_array[idx]} -> {thrust}")


else:
    thrust_map = []
    mass_flow_map = []
    isp_map = []

    # Iterate while keeping the structure
    it = np.nditer(variable_inputs_array, flags=["multi_index"], op_flags=["readonly"])
    
    # for variable_input_combination in tqdm(it, total=len(it), desc="Computing..."):
    for variable_input_combination in it: 
        thrust_newton, mass_flow_kg, isp = engine.ThrustyBusty(
                    constant_inputs_array["FUEL_NAME"], 
                    # variable_input_combination["FUEL_NAME"],
                    
                    constant_inputs_array["OXIDIZER_NAME"],
                    constant_inputs_array["PROPELLANT_TANK_OUTER_DIAMETER"],
                    
                    constant_inputs_array["CONTRACTION_RATIO"],
                    # variable_input_combination["CONTRACTION_RATIO"],
                    
                    variable_input_combination["OF_RATIO"],
                    
                    # constant_inputs_array["CHAMBER_PRESSURE"].item(),
                    variable_input_combination["CHAMBER_PRESSURE"],
                    )
        thrust_map.append(thrust_newton * c.N2LBF)
        mass_flow_map.append(mass_flow_kg)
        isp_map.append(isp)
        print(f"{it.multi_index}: {variable_input_combination} -> {thrust_newton}")

print(f"thrust map: number of elements: {len(thrust_map)}, bytes: {getsizeof(thrust_map)}")


# ___  _    ____ ___ ___ _ _  _ ____ 
# |__] |    |  |  |   |  | |\ | | __ 
# |    |___ |__|  |   |  | | \| |__] 
                                   
x = np.array(variable_inputs_array[0, :]["CHAMBER_PRESSURE"])
y = np.array(variable_inputs_array[:, 0]["OF_RATIO"])
z = np.array(isp_map)

Y, X = np.meshgrid(x, y) # I don't know why you have to swap X and Y but you do
Z = z.reshape(len(x), len(y))

plt.contour(X, Y, Z)
plt.pcolormesh(X, Y, Z, cmap='Spectral_r')
# plt.contourf(X, Y, Z, 100, cmap='Spectral_r')

plt.colorbar(label='isp [s]')
# plt.colorbar(label='Mass Flow Rate [kg/s] or Thrust [lbf]')
plt.xlabel('OF Ratio')
plt.ylabel('Chamber Pressure [psi]')

plt.show()