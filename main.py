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


show_all_results = True
show_rail_exit_accel_limiting_factor = False
show_copv_limiting_factor = False



# The variable_inputs_array will be separate from the constant_inputs_array to save memory size and hopefully increase speed
variable_inputs_array = numpy_ndarray_handler.dictionary_to_ndarray(inputs.variable_inputs)
constant_inputs_array = numpy_ndarray_handler.dictionary_to_ndarray(inputs.constant_inputs)

output_names = [
    # "OXIDIZER_TANK_LENGTH",                          # [ft]
    # "CHAMBER_TEMPERATURE",                       # [k]
    
    "MASS_FLOW_RATE",                         # [kg/s]
    "ISP",                                      # [s]
    "JET_THRUST",                             # [lbf] engine jet thrust
    # "TOTAL_LENGTH",                              # [ft]
    # "WET_MASS",                                 # [lbm]
    # "DRY_MASS",                                 # [lbm]
    "BURN_TIME",                 # [s]
    
    # "APOGEE",                                   # [ft]
    # "MAX_ACCELERATION",                         # [G's]
    # "MAX_VELOCITY",                         # [m/s]
    # "RAIL_EXIT_VELOCITY",                          # [ft/s]
    # "RAIL_EXIT_ACCELERATION",                          # [ft/s]
    # "RAIL_EXIT_TWR",                            # [n/a]
] # USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 
  # USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 
  # USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 
  # USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 
  # USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 
  # USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 

def AccelerationToTWR(acceleration):
    TWR = (acceleration/c.GRAVITY) + 1
    return TWR

# CEA_Array = engine.CreateMassiveCEAArray(constant_inputs_array, variable_inputs_array)

def run_rocket_function(idx, variable_input_combination):

    fuel_name = numpy_ndarray_handler.GetFrom_ndarray("FUEL_NAME", constant_inputs_array, variable_input_combination)

    fuel_tank_length = numpy_ndarray_handler.GetFrom_ndarray("FUEL_TANK_LENGTH", constant_inputs_array, variable_input_combination)

    jet_thrust, isp, mass_flow_rate, chamber_temperature = engine.ThrustyBusty(
                fuel_name,
                numpy_ndarray_handler.GetFrom_ndarray("OXIDIZER_NAME", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_OUTER_DIAMETER", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("CONTRACTION_RATIO", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("CHAMBER_PRESSURE", constant_inputs_array, variable_input_combination),
                # CEA_Array[idx],
                )

    total_usable_propellant_mass, engine_burn_time, oxidizer_tank_length, best_case_tanks_too_big, worst_case_tanks_too_big = tanks.GoFluids(
                numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_INNER_DIAMETER", constant_inputs_array, variable_input_combination),
                fuel_tank_length,
                numpy_ndarray_handler.GetFrom_ndarray("CHAMBER_PRESSURE", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("OXIDIZER_NAME", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("FUEL_NAME", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, variable_input_combination),
                mass_flow_rate,
                )

    # wet_mass = total_usable_propellant_mass * numpy_ndarray_handler.GetFrom_ndarray("WET_MASS_TO_USABLE_PROPELLANT_MASS_RATIO", constant_inputs_array, variable_input_combination)
    # dry_mass = wet_mass - total_usable_propellant_mass
    
    regulator_mass = 1.200 # regulator https://valvesandregulators.aquaenvironment.com/item/high-flow-reducing-regulators-2/873-d-high-flow-dome-loaded-reducing-regulators/item-1659
    valves_mass = 2 * 5.84 * c.LB2KG # fuel and ox 3/4 inch valve https://habonim.com/wp-content/uploads/2020/08/C47-BD_C47__2023_VO4_28-06-23.pdf
    tank_wall_mass = (0.2200 * ((oxidizer_tank_length + fuel_tank_length) * c.M2IN) * c.LB2KG) # 0.2200 lbs per inch * tank length
    bulkhead_mass = (4 * 2.6227 * 4 * c.LB2KG) # 4 bulkheads * 2.6227 lbs per inch * 4 inch long bulkhead
    recovery_bay_mass = 25 * c.LB2KG  # [kg] Estimated mass of the recovery bay https://github.com/Purdue-Space-Program/PSPL_Rocket_4_Sizing/blob/2b15e1dc508a56731056ff594a3c6b5afb639b4c/scripts/structures.py#L75
    structures = 15 * c.LB2KG # structures !
    
    dry_mass = (valves_mass + regulator_mass + tank_wall_mass + bulkhead_mass  + recovery_bay_mass + structures) * 1.2 # 1.2 factor of safety margin
    wet_mass = total_usable_propellant_mass + dry_mass
    
    total_length = 7 * (oxidizer_tank_length + fuel_tank_length) # fix this dumbass
    
    if show_all_results:
        best_case_tanks_too_big = False # override to show all results
        worst_case_tanks_too_big = False # override to show all results
    
    if show_copv_limiting_factor:
        if show_all_results:
            raise RuntimeError("DUMBASS. DONT HAVE SHOW ALL RESULTS AND SHOW COPV LIMITING FACTOR AT THE SAME TIME")
        
        if best_case_tanks_too_big:
            jet_thrust = 0
        elif worst_case_tanks_too_big and (best_case_tanks_too_big == False):
            jet_thrust = 0.2
        elif worst_case_tanks_too_big == False:
            jet_thrust = 1
    else:
        if worst_case_tanks_too_big:
            jet_thrust = np.nan
            isp = np.nan
            engine_burn_time = np.nan
            mass_flow_rate = np.nan
    
    # avoid calculating trajectory if the value is not going to be used
    if any(output in output_names for output in ["APOGEE", "MAX_ACCELERATION", "RAIL_EXIT_VELOCITY", "RAIL_EXIT_ACCELERATION", "TAKEOFF_TWR", "RAIL_EXIT_TWR", "MAX_ACCELERATION"]):
        estimated_apogee, max_accel, max_velocity, rail_exit_velocity, rail_exit_accel, total_impulse = trajectory.calculate_trajectory(
                                wet_mass, 
                                mass_flow_rate,
                                jet_thrust,
                                numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_OUTER_DIAMETER", constant_inputs_array, variable_input_combination),
                                3,
                                0.15,
                                engine.RadiusToArea((numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_OUTER_DIAMETER", constant_inputs_array, variable_input_combination)/2) - (0.5 * c.IN2M)), # lowkey a guess
                                15 * c.PSI2PA,
                                engine_burn_time, 
                                total_length,
                                False
                            )
        
        rail_exit_TWR = AccelerationToTWR(rail_exit_accel)
            
    initial_thrust = ((jet_thrust) - (c.GRAVITY * wet_mass)) / wet_mass
    
    if worst_case_tanks_too_big or initial_thrust <= 0:
        rail_exit_accel = np.nan
        rail_exit_velocity = np.nan
        rail_exit_TWR = np.nan
        max_velocity = np.nan
        max_accel = np.nan
        estimated_apogee = np.nan


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
        "DRY_MASS": dry_mass,
        "OXIDIZER_TANK_LENGTH": oxidizer_tank_length,
        "TOTAL_LENGTH" : total_length,
        "CHAMBER_TEMPERATURE": chamber_temperature,
        "BURN_TIME" : engine_burn_time,
        
        "APOGEE": estimated_apogee if "estimated_apogee" in locals() else np.nan,
        "MAX_ACCELERATION": max_accel if "max_accel" in locals() else np.nan,
        "MAX_VELOCITY": max_velocity if "max_velocity" in locals() else np.nan,
        "RAIL_EXIT_VELOCITY": rail_exit_velocity if "rail_exit_velocity" in locals() else np.nan,
        "RAIL_EXIT_ACCELERATION": rail_exit_accel if "rail_exit_accel" in locals() else np.nan,
        "RAIL_EXIT_TWR": rail_exit_TWR if "rail_exit_TWR" in locals() else np.nan,
    }


    dtype = []
    for output_name in output_names:
        if output_name in mapping:
            dtype.append((output_name, np.float32))

    # HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Allocate structured array with one record
    output_list = np.zeros(1, dtype=dtype)
    
    # Fill values
    for name, _ in dtype:
        
        if show_rail_exit_accel_limiting_factor:
            exists = (any((name == "RAIL_EXIT_ACCELERATION") and not(np.isnan(mapping[name])) for name, value in dtype))
            if exists:
                within_bounds = ((rail_exit_accel > (5 * c.GRAVITY)) and (rail_exit_accel < (7 * c.GRAVITY)))
            
            if exists and within_bounds:
                output_list[name] = mapping[name]
            else:
                output_list[name] = np.nan
        else:
            output_list[name] = mapping[name]

    # # Compare to Copperhead
    # CR = numpy_ndarray_handler.GetFrom_ndarray("CONTRACTION_RATIO", constant_inputs_array, variable_input_combination)
    # FTL = numpy_ndarray_handler.GetFrom_ndarray("FUEL_TANK_LENGTH", constant_inputs_array, variable_input_combination)
    # if (CR > 4.9) & (CR < 5.1) & (FTL > 3.9 * c.FT2M) & (FTL < 4.1 * c.FT2M):
    #     print(f"Contraction Ratio: {CR}, Fuel Tank Length: {FTL * c.M2FT}, Estimated Apogee: {estimated_apogee * c.M2FT}, Takeoff TWR: {takeoff_TWR}")

    # # Chosen parameters
    # CR = numpy_ndarray_handler.GetFrom_ndarray("CONTRACTION_RATIO", constant_inputs_array, variable_input_combination)
    # FTL = numpy_ndarray_handler.GetFrom_ndarray("FUEL_TANK_LENGTH", constant_inputs_array, variable_input_combination)
    # if (CR > 4.95) & (CR < 5.06) & (FTL > 11.8 * c.IN2M) & (FTL < 12.2 * c.IN2M):
    #     print(f"\nContraction Ratio: {CR}")
    #     print(f"Fuel Tank Length: {FTL * c.M2FT} feet")
              
    #     print(f"\nJET_THRUST: {jet_thrust * c.N2LBF} lbf")
    #     print(f"ISP: {isp} seconds")
    #     print(f"MASS_FLOW_RATE: {mass_flow_rate * c.KG2LB} lbm")
    #     print(f"BURN_TIME: {engine_burn_time} seconds")
    #     print(f"TOTAL_LENGTH: {total_length * c.M2FT} feet")
    #     print(f"WET_MASS: {wet_mass * c.KG2LB} lbm")
    #     print(f"DRY_MASS: {dry_mass * c.KG2LB} lbm")
        
    #     print(f"Estimated Apogee: {estimated_apogee * c.M2FT} feet")
    #     print(f"Off the rail TWR: {rail_exit_TWR}")
    #     print(f"Off the rail acceleration: {rail_exit_accel / c.GRAVITY} G's")
    #     print(f"Off the rail velocity: {rail_exit_velocity} m/s")
    #     print(f"Max Acceleration: {max_accel / c.GRAVITY} G's")
    #     print(f"Max Velocity: {max_velocity / 343} Mach")

        # print(f"ox tank volume: {oxidizer_tank_length}")
    
    
    
    return (idx, output_list)


output_array = threaded_run.ThreadedRun(run_rocket_function, variable_inputs_array, output_names, True)


print(constant_inputs_array)
print("\nfix that dumbass !")

AXES = [variable_inputs_array.dtype.names[i] for i in range(len(variable_inputs_array.dtype))]
if len(AXES) == 2:
    # make axes automated (idc to do that rn)
    p.PlotColorMaps(AXES[0], AXES[1], variable_inputs_array, output_names, output_array, show_copv_limiting_factor)
elif len(AXES) == 3:
    p.PlotColorMaps3D(AXES[0], AXES[1], AXES[2], variable_inputs_array, output_names, output_array, show_copv_limiting_factor)
else:
    raise ValueError(f"{len(AXES)} is an unsupported number of axis")
