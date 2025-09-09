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

import inputs
import threaded_run

from vehicle_scripts import (
    engine,
    numpy_ndarray_handler,
    tanks,
    trajectory
    # structures,
)
from coding_utils import (
    constants as c,
    plotting as p,
)

import coding_utils.constants as c
import numpy as np
import matplotlib.pyplot as plt
from sys import getsizeof
from tqdm import tqdm
import pandas as pd


# Converting the dictionary to a structured numpy array is more computationally efficient:
# https://numpy.org/doc/stable/reference/arrays.ndarray.html
# https://numpy.org/doc/stable/user/basics.rec.html
# good visual: https://www.w3resource.com/numpy/ndarray/index.php

# The variable_inputs_array will be separate from the constant_inputs_array to save memory size and hopefully increase speed

variable_inputs_array = numpy_ndarray_handler.dictionary_to_ndarray(inputs.variable_inputs)
constant_inputs_array = numpy_ndarray_handler.dictionary_to_ndarray(inputs.constant_inputs)

output_names = [
    # "JET_THRUST",                             # [lbf] engine jet thrust
    # "ISP",                                      # [s]
    "MASS_FLOW_RATE",                         # [kg/s]
    # "WET_MASS",                                 # [lbm]
    
    "APOGEE",                                   # [ft]
    # "TAKEOFF_TWR",                              # [n/a]
    "RAIL_EXIT_TWR",                            # [n/a]
    "BURN_TIME"                 # [s]
]

def run_rocket_function(idx, variable_input_combination):

    jet_thrust, isp, mass_flow_rate = engine.ThrustyBusty(
                numpy_ndarray_handler.GetFrom_ndarray("FUEL_NAME", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("OXIDIZER_NAME", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_OUTER_DIAMETER", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("CONTRACTION_RATIO", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("CHAMBER_PRESSURE", constant_inputs_array, variable_input_combination),
                )


    if inputs.USE_FAKE_TANKS_DATA == True:
        total_usable_propellant_mass, engine_burn_time, oxidizer_tank_length = (14.577917569187084, 8.77083825323153, 0.46935451405705586)
    else:
        total_usable_propellant_mass, engine_burn_time, oxidizer_tank_length = tanks.GoFluids(
                    numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_INNER_DIAMETER", constant_inputs_array, variable_input_combination),
                    numpy_ndarray_handler.GetFrom_ndarray("FUEL_TANK_LENGTH", constant_inputs_array, variable_input_combination),
                    numpy_ndarray_handler.GetFrom_ndarray("CHAMBER_PRESSURE", constant_inputs_array, variable_input_combination),
                    numpy_ndarray_handler.GetFrom_ndarray("OXIDIZER_NAME", constant_inputs_array, variable_input_combination),
                    numpy_ndarray_handler.GetFrom_ndarray("FUEL_NAME", constant_inputs_array, variable_input_combination),
                    numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, variable_input_combination),
                    mass_flow_rate,
                    )

    wet_mass = total_usable_propellant_mass * numpy_ndarray_handler.GetFrom_ndarray("WET_MASS_TO_USABLE_PROPELLANT_MASS_RATIO", constant_inputs_array, variable_input_combination)
    
    # avoid calculating trajectory if the value is not going to be used
    if any(output in output_names for output in ["APOGEE", "MAX_ACCELERATION", "RAIL_EXIT_VELOCITY", "RAIL_EXIT_ACCELERATION", "TAKEOFF_TWR", "RAIL_EXIT_TWR"]):
        estimated_apogee, max_accel, rail_exit_velocity, rail_exit_accel, total_impulse = trajectory.calculate_trajectory(
                                wet_mass, 
                                mass_flow_rate,
                                jet_thrust,
                                numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_OUTER_DIAMETER", constant_inputs_array, variable_input_combination),
                                engine.RadiusToArea((numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_OUTER_DIAMETER", constant_inputs_array, variable_input_combination)/2) - (0.5 * c.IN2M)), # lowkey a guess
                                10 * c.PSI2PA,
                                engine_burn_time,
                                5 * (oxidizer_tank_length + numpy_ndarray_handler.GetFrom_ndarray("FUEL_TANK_LENGTH", constant_inputs_array, variable_input_combination)), # fix this dumbass
                                False,
                            )
        takeoff_TWR = jet_thrust/(wet_mass * c.GRAVITY)
        rail_exit_TWR = (rail_exit_accel/c.GRAVITY) + 1

    
    # for output_name in output_names:
    #     if output_name == "JET_THRUST":
    #         output_list.append(jet_thrust)
    #     elif output_name == "ISP":
    #         output_list.append(isp)
    #     elif output_name == "MASS_FLOW_RATE":
    #         output_list.append(mass_flow_rate)
    #     elif output_name == "APOGEE":
    #         output_list.append(estimated_apogee)
            

    output_list = np.array([])

    mapping = {
        "JET_THRUST": jet_thrust,
        "ISP": isp,
        "MASS_FLOW_RATE": mass_flow_rate,
        "WET_MASS": wet_mass,
                
        "APOGEE": estimated_apogee if "APOGEE" in output_names else np.nan,
        "TAKEOFF_TWR": takeoff_TWR,
        "MAX_ACCELERATION": max_accel,
        "RAIL_EXIT_VELOCITY": rail_exit_velocity,
        "RAIL_EXIT_ACCELERATION": rail_exit_accel,
        "RAIL_EXIT_TWR": rail_exit_TWR,
        "BURN_TIME" : engine_burn_time,
    }


    dtype = []
    for output_name in output_names:
        if output_name in mapping:
            dtype.append((output_name, np.float32))

    # Allocate structured array with one record
    output_list = np.zeros(1, dtype=dtype)

    # Fill values
    for name, _ in dtype:
        output_list[name] = mapping[name]
        
    return (idx, output_list)


output_array = threaded_run.ThreadedRun(run_rocket_function, variable_inputs_array, output_names, True)


if inputs.USE_FAKE_TANKS_DATA == True:
    print("THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE THE DATA IS FAKE ")


AXES = ["CONTRACTION_RATIO", "FUEL_TANK_LENGTH"]
if len(AXES) == 2:
    p.PlotColorMaps(AXES[0], AXES[1], variable_inputs_array, output_names, output_array)
elif len(AXES) == 3:
    X, Y, Z = p.SetupHolyFuckArrays(variable_inputs_array, AXES[0], AXES[1], AXES[2], output_names, output_array)
    p.HolyFuck(AXES[0], AXES[1], AXES[2], variable_inputs_array, output_names, output_array)
else:
    raise ValueError(f"{len(AXES)} is an unsupported number of axis")