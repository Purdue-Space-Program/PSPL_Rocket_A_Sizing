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

ATMOSPHERE_DATA = pd.read_csv("atmosphere.csv")


def run_rocket_function(idx, variable_input_combination):
    # Do imports inside the worker (not passed in)
    from vehicle_scripts import engine
    from coding_utils import constants as c
    from inputs import constant_inputs as constant_inputs_dict

    print(f"chamber_pressure: {numpy_ndarray_handler.GetFrom_ndarray("CHAMBER_PRESSURE", constant_inputs_array, variable_input_combination) * c.PA2PSI}")
    print(f"OF Ratio: {numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, variable_input_combination)}")


    thrust_newton, mass_flow_kg, isp = engine.ThrustyBusty(
                numpy_ndarray_handler.GetFrom_ndarray("FUEL_NAME", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("OXIDIZER_NAME", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_OUTER_DIAMETER", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("CONTRACTION_RATIO", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("CHAMBER_PRESSURE", constant_inputs_array, variable_input_combination),
                )


    total_usable_propellant_mass, engine_burn_time, oxidizer_tank_length = (14.577917569187084, 8.77083825323153, 0.46935451405705586)
    # total_usable_propellant_mass, engine_burn_time, oxidizer_tank_length = tanks.GoFluids(
    #             numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_INNER_DIAMETER", constant_inputs_array, variable_input_combination),
    #             numpy_ndarray_handler.GetFrom_ndarray("FUEL_TANK_LENGTH", constant_inputs_array, variable_input_combination),
    #             numpy_ndarray_handler.GetFrom_ndarray("CHAMBER_PRESSURE", constant_inputs_array, variable_input_combination),
    #             numpy_ndarray_handler.GetFrom_ndarray("OXIDIZER_NAME", constant_inputs_array, variable_input_combination),
    #             numpy_ndarray_handler.GetFrom_ndarray("FUEL_NAME", constant_inputs_array, variable_input_combination),
    #             numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, variable_input_combination),
    #             mass_flow_kg,
    #             )
    # print(total_usable_propellant_mass, engine_burn_time, oxidizer_tank_length)
    # print(f"prop mass: {total_usable_propellant_mass} burn time: {engine_burn_time}")
    
    total_rocket_mass = total_usable_propellant_mass * 3.7 # assume total mass is 3 times the wet mass (estimated ratio for copperhead was 2.154)
    estimated_apogee, max_accel, rail_exit_velocity, rail_exit_accel, total_impulse = trajectory.calculate_trajectory(
                            total_rocket_mass, 
                            mass_flow_kg,
                            thrust_newton,
                            numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_OUTER_DIAMETER", constant_inputs_array, variable_input_combination),
                            engine.RadiusToArea((numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_OUTER_DIAMETER", constant_inputs_array, variable_input_combination)/2) - (0.5 * c.IN2M)), # lowkey a guess
                            10 * c.PSI2PA,
                            engine_burn_time,
                            2 * (oxidizer_tank_length + numpy_ndarray_handler.GetFrom_ndarray("FUEL_TANK_LENGTH", constant_inputs_array, variable_input_combination)), # fix this dumbass
                            ATMOSPHERE_DATA,
                            1,
                        )
    print(f"rail_exit_velocity: {rail_exit_velocity}")
    print(f"max_accel: {max_accel}")
    print(f"initial mass: {total_rocket_mass * c.KG2LB} lb")
    print(f"initial TWR: {thrust_newton/(total_usable_propellant_mass * 2.5*c.GRAVITY)}, estimated_apogee: {estimated_apogee * c.M2FT} ft")
    
    return (idx, thrust_newton, mass_flow_kg, isp)


newton_thrust_map, isp_map, mass_flow_map = threaded_run.ThreadedRun(run_rocket_function, constant_inputs_array, variable_inputs_array, False)


# ___  _    ____ ___ ___ _ _  _ ____ 
# |__] |    |  |  |   |  | |\ | | __ 
# |    |___ |__|  |   |  | | \| |__] 

color_variable_map = isp_map
X, Y, Z = p.SetupArrays(variable_inputs_array, color_variable_map)
p.PlotColorMap(X, Y, Z, constant_inputs_array, color_variable_map, "isp [s]")

"isp [s] or Mass Flow Rate [kg/s] or Thrust [lbf]"