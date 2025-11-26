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
    trajectory,
    mass_and_length,
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


def save_last_run(variable_inputs_array, plotting_output_names, output_array, show_copv_limiting_factor, filename="last_run.npz"):
# def save_arrays_npz(X, Y, Z, values, filename="data.npz"):
    np.savez_compressed(filename, variable_inputs_array=variable_inputs_array, plotting_output_names=plotting_output_names, output_array=output_array, show_copv_limiting_factor=show_copv_limiting_factor)

def load_last_run(filename="last_run.npz"):
    data = np.load(filename)
    return data["variable_inputs_array"], data["plotting_output_names"], data["output_array"], data["show_copv_limiting_factor"]


ignore_copv_limit = True
show_copv_limiting_factor = False
limit_rail_exit_accel = False


# The variable_inputs_array will be separate from the constant_inputs_array to save memory size and hopefully increase speed
variable_inputs_array = numpy_ndarray_handler.dictionary_to_ndarray(inputs.variable_inputs)
constant_inputs_array = numpy_ndarray_handler.dictionary_to_ndarray(inputs.constant_inputs)

plotting_output_names = [
    
    "MASS_FLOW_RATE",                        # [kg/s]
    "ISP",                                   # [s]
    "JET_THRUST",                            # [lbf]
    "TOTAL_LENGTH",                          # [ft]
    "WET_MASS",                              # [lbm]
    "DRY_MASS",                              # [lbm]
    "BURN_TIME",                             # [s]
    "CHAMBER_TEMPERATURE",                   # [k]
    
    "CHAMBER_INNER_DIAMETER",                      # [in]
    "CHAMBER_STRAIGHT_WALL_LENGTH",          # [in]
    "THROAT_DIAMETER",                       # [in]
    "INJECTOR_TO_THROAT_LENGTH",             # [in]
    
    # "TANK_PRESSURE",                         # [psi]
    # "OXIDIZER_TANK_VOLUME",                
    # "OXIDIZER_TOTAL_MASS",
    # "FUEL_TANK_VOLUME",
    # "FUEL_TOTAL_MASS",
    # "OXIDIZER_TANK_LENGTH",                  # [ft]

    "APOGEE",                                # [ft]
    "MAX_ACCELERATION",                      # [G's]
    "MAX_VELOCITY",                          # [m/s]
    "RAIL_EXIT_VELOCITY",                    # [ft/s]
    "RAIL_EXIT_ACCELERATION",                # [ft/s]
    "RAIL_EXIT_TWR",                         # [n/a] 
    "TOTAL_IMPULSE"                          # [newton-seconds]    
]

# USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 
# USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 
# USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 
# USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 
# USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 
# USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA USE A FUCKING COMMA 

def AccelerationToTWR(acceleration):
    TWR = (acceleration/c.GRAVITY) + 1
    return TWR

# CEA_Array = engine.CreateMassiveCEAArray(constant_inputs_array, variable_inputs_array)

def run_rocket_function(idx, variable_input_combination, specified_output_names):

    fuel_name = numpy_ndarray_handler.GetFrom_ndarray("FUEL_NAME", constant_inputs_array, variable_input_combination)

    fuel_tank_length = numpy_ndarray_handler.GetFrom_ndarray("FUEL_TANK_LENGTH", constant_inputs_array, variable_input_combination)
    propellant_tank_outer_diameter = numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_OUTER_DIAMETER", constant_inputs_array, variable_input_combination)
    propellant_tank_inner_diameter = numpy_ndarray_handler.GetFrom_ndarray("PROPELLANT_TANK_INNER_DIAMETER", constant_inputs_array, variable_input_combination)

    jet_thrust, isp, mass_flow_rate, chamber_temperature, chamber_radius, throat_radius, chamber_length, injector_to_throat_length = engine.ThrustyBusty(
                fuel_name,
                numpy_ndarray_handler.GetFrom_ndarray("OXIDIZER_NAME", constant_inputs_array, variable_input_combination),
                propellant_tank_outer_diameter,
                numpy_ndarray_handler.GetFrom_ndarray("CONTRACTION_RATIO", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("CHAMBER_PRESSURE", constant_inputs_array, variable_input_combination),
                # CEA_Array[idx],
                )
    

    total_usable_propellant_mass, engine_burn_time, oxidizer_tank_length, oxidizer_total_tank_volume, oxidizer_total_propellant_mass, fuel_total_tank_volume, fuel_total_propellant_mass, best_case_tanks_too_big, worst_case_tanks_too_big, tank_pressure = tanks.GoFluids(
                propellant_tank_inner_diameter,
                fuel_tank_length,
                numpy_ndarray_handler.GetFrom_ndarray("CHAMBER_PRESSURE", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("OXIDIZER_NAME", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("FUEL_NAME", constant_inputs_array, variable_input_combination),
                numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, variable_input_combination),
                mass_flow_rate,
                )

    # Function from vehicle parameters page on PSPL_Rocket_A Repo github.com/Purdue-Space-Program/PSPL_Rocket_A/blob/a7066c7267f537f3e2d6b0d332520a23ce78649b/vehicle_parameters.py
    dry_mass, wet_mass, total_length = mass_and_length.calculate_mass(
                   fuel_tank_length, 
                   oxidizer_tank_length, 
                   propellant_tank_outer_diameter, 
                   propellant_tank_inner_diameter, 
                   fuel_total_propellant_mass, 
                   oxidizer_total_propellant_mass,
                   )


    if ignore_copv_limit:
        best_case_tanks_too_big = False # override to show all results
        worst_case_tanks_too_big = False # override to show all results
    
    if show_copv_limiting_factor:
        if ignore_copv_limit:
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
            chamber_temperature = np.nan

    # avoid calculating trajectory if the value is not going to be used
    
    plot_trajectory = False
    if any(output in specified_output_names for output in ["APOGEE", "MAX_ACCELERATION", "RAIL_EXIT_VELOCITY", "RAIL_EXIT_ACCELERATION", "TAKEOFF_TWR", "RAIL_EXIT_TWR", "MAX_ACCELERATION"]):
        estimated_apogee, max_accel, max_velocity, rail_exit_velocity, rail_exit_accel, total_impulse, off_the_rail_time = trajectory.calculate_trajectory(
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
                                plot_trajectory,
                            )
        # print(f"\n\noff_the_rail_time: {off_the_rail_time} [s]")
        rail_exit_TWR = AccelerationToTWR(rail_exit_accel)

    initial_acceleration = ((jet_thrust) - (c.GRAVITY * wet_mass)) / wet_mass
    # initial_TWR = AccelerationToTWR(initial_acceleration)
    # print(f"initial_TWR: {initial_TWR}")

    if worst_case_tanks_too_big or initial_acceleration <= 0:
        rail_exit_accel = np.nan
        rail_exit_velocity = np.nan
        rail_exit_TWR = np.nan
        max_velocity = np.nan
        max_accel = np.nan
        estimated_apogee = np.nan



    output_list = np.array([])

    mapping = {
        "JET_THRUST": jet_thrust,
        "ISP": isp,
        "OF_RATIO": numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, variable_input_combination),
        "MASS_FLOW_RATE": mass_flow_rate,
        "CHAMBER_TEMPERATURE": chamber_temperature,
        
        "CHAMBER_INNER_DIAMETER": chamber_radius*2,
        "CHAMBER_STRAIGHT_WALL_LENGTH": chamber_length,
        "INJECTOR_TO_THROAT_LENGTH": injector_to_throat_length,
        "THROAT_DIAMETER": throat_radius*2,
        
        "TANK_PRESSURE": tank_pressure,
        "OXIDIZER_TANK_LENGTH": oxidizer_tank_length,
        "OXIDIZER_TANK_VOLUME": oxidizer_total_tank_volume,
        "OXIDIZER_TOTAL_MASS": oxidizer_total_propellant_mass,
        "FUEL_TANK_VOLUME": fuel_total_tank_volume,
        "FUEL_TOTAL_MASS": fuel_total_propellant_mass,
        "BURN_TIME": engine_burn_time,
        
        "WET_MASS": wet_mass,
        "DRY_MASS": dry_mass,
        "TOTAL_LENGTH" : total_length,
        
        "APOGEE": estimated_apogee if "estimated_apogee" in locals() else np.nan,
        "MAX_ACCELERATION": max_accel if "max_accel" in locals() else np.nan,
        "MAX_VELOCITY": max_velocity if "max_velocity" in locals() else np.nan,
        "RAIL_EXIT_VELOCITY": rail_exit_velocity if "rail_exit_velocity" in locals() else np.nan,
        "RAIL_EXIT_ACCELERATION": rail_exit_accel if "rail_exit_accel" in locals() else np.nan,
        "RAIL_EXIT_TWR": rail_exit_TWR if "rail_exit_TWR" in locals() else np.nan,
        "TOTAL_IMPULSE": total_impulse if "total_impulse" in locals() else np.nan,
    }


    dtype = []
    for output_name in specified_output_names:
        if output_name in mapping:
            dtype.append((output_name, np.float32))

    # HERE !!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # Allocate structured array with one record
    output_list = np.zeros(1, dtype=dtype)
    
    # Fill values
    for name, _ in dtype:
        
        if limit_rail_exit_accel:
            exists = (any((name == "RAIL_EXIT_ACCELERATION") and not(np.isnan(mapping[name])) for name, value in dtype))
            if exists:
                within_bounds = ((rail_exit_accel > (5 * c.GRAVITY)))# and (rail_exit_accel < (10 * c.GRAVITY)))
            
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
    
    return (idx, output_list)



# avoid calculating all the rocket outputs if the last run was with the same inputs
last_run_variable_inputs_array, last_run_plotting_output_names, last_run_output_array, last_run_show_copv_limiting_factor = load_last_run()

are_inputs_same_from_last_run = (
    np.array_equal(last_run_variable_inputs_array, variable_inputs_array)
    # and np.array_equal(last_run_plotting_output_names, plotting_output_names)    # allow different plot outputs? might lead to an error if trajectory wasn't calculated for a past run
    and np.array_equal(last_run_show_copv_limiting_factor, show_copv_limiting_factor)
)

if are_inputs_same_from_last_run:
    output_array = last_run_output_array
else:
    use_threading = True
    # if __debug__:
    #     use_threading = False 
    output_array = threaded_run.ThreadedRun(run_rocket_function, variable_inputs_array, plotting_output_names, use_threading)


axes_names = [variable_inputs_array.dtype.names[i] for i in range(len(variable_inputs_array.dtype))]


if len(axes_names) == 2:
    save_last_run(variable_inputs_array, plotting_output_names, output_array, show_copv_limiting_factor, filename="last_run.npz")
    p.PlotColorMaps(variable_inputs_array, plotting_output_names, output_array, show_copv_limiting_factor)

elif len(axes_names) == 3:
    save_last_run(variable_inputs_array, plotting_output_names, output_array, show_copv_limiting_factor, filename="last_run.npz")
    p.PlotColorMaps3D(variable_inputs_array, plotting_output_names, output_array, show_copv_limiting_factor)

else:
    raise ValueError(f"{len(axes_names)} is an unsupported number of axes")


fields_dtype = []
desired_input_values = []
for variable_input in list(inputs.variable_inputs):
    fields_dtype.append((variable_input, np.float32))
    
    if variable_input == "CHAMBER_PRESSURE":
        desired_input_values.append(250 * c.PSI2PA)
    
    elif variable_input == "CONTRACTION_RATIO":
        desired_input_values.append(4)

    elif variable_input == "FUEL_TANK_LENGTH":
        desired_input_values.append(1 * c.IN2M)
    
    else:
        raise ValueError

full_output_names = [
    
    "MASS_FLOW_RATE",                        # [kg/s]
    "ISP",                                   # [s]
    "JET_THRUST",                            # [lbf]
    "TOTAL_LENGTH",                          # [ft]
    "WET_MASS",                              # [lbm]
    "DRY_MASS",                              # [lbm]
    "BURN_TIME",                             # [s]
    "CHAMBER_TEMPERATURE",                   # [k]
    
    "CHAMBER_INNER_DIAMETER",                      # [in]
    "CHAMBER_STRAIGHT_WALL_LENGTH",          # [in]
    "THROAT_DIAMETER",                       # [in]
    "INJECTOR_TO_THROAT_LENGTH",             # [in]
    
    "TANK_PRESSURE",                         # [psi]
    "OXIDIZER_TANK_VOLUME",                
    "OXIDIZER_TOTAL_MASS",
    "FUEL_TANK_VOLUME",
    "FUEL_TOTAL_MASS",
    "OXIDIZER_TANK_LENGTH",                  # [ft]

    "APOGEE",                                # [ft]
    "MAX_ACCELERATION",                      # [G's]
    "MAX_VELOCITY",                          # [m/s]
    "RAIL_EXIT_VELOCITY",                    # [ft/s]
    "RAIL_EXIT_ACCELERATION",                # [ft/s]
    "RAIL_EXIT_TWR",                         # [n/a] 
    "TOTAL_IMPULSE"                          # [newton-seconds]    
]

desired_input = np.array([tuple(desired_input_values)], dtype=np.dtype(fields_dtype))
_, desired_rocket_output_list = run_rocket_function(69 / 420, desired_input, full_output_names)

# print(desired_rocket_output_list)
print(f"\n-------Inputs-------")
print(f"Fuel: {numpy_ndarray_handler.GetFrom_ndarray("FUEL_NAME", constant_inputs_array, desired_input).title()}, Oxidizer: {numpy_ndarray_handler.GetFrom_ndarray("OXIDIZER_NAME", constant_inputs_array, desired_input).title()}")
print(f"Chamber Pressure: {numpy_ndarray_handler.GetFrom_ndarray("CHAMBER_PRESSURE", constant_inputs_array, desired_input) * c.PA2PSI} PSI")
print(f"OF Ratio: {numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, desired_input)}")
print(f"Contraction Ratio: {numpy_ndarray_handler.GetFrom_ndarray("CONTRACTION_RATIO", constant_inputs_array, desired_input)}")
print(f"Fuel Tank Length: {numpy_ndarray_handler.GetFrom_ndarray("FUEL_TANK_LENGTH", constant_inputs_array, desired_input) * c.M2IN:.3f} inches")

print(f"\n-------Outputs-------")
print(f"Tank Pressure: {desired_rocket_output_list["TANK_PRESSURE"] * c.PA2PSI} psi")
# print(f"Tank Pressure: {numpy_ndarray_handler.GetFrom_ndarray("TANK_PRESSURE", constant_inputs_array, desired_input) * c.PA2PSI} psi")
print(f"Jet Thrust: {desired_rocket_output_list["JET_THRUST"] * c.N2LBF} lbf")
print(f"ISP: {desired_rocket_output_list["ISP"]} seconds")
print(f"Total Mass Flow Rate: {desired_rocket_output_list["MASS_FLOW_RATE"] * c.KG2LB} lbm/s")
print(f"Chamber Temperature: {desired_rocket_output_list["CHAMBER_TEMPERATURE"]} kelvin")
print("")
print(f"Chamber Inner Diameter: {desired_rocket_output_list["CHAMBER_INNER_DIAMETER"] * c.M2IN} in")
print(f"Throat Diameter: {desired_rocket_output_list["THROAT_DIAMETER"]* c.M2IN} in")
print(f"Chamber Straight Wall Length: {desired_rocket_output_list["CHAMBER_STRAIGHT_WALL_LENGTH"] * c.M2IN} in")
print(f"Injector to Throat Length: {desired_rocket_output_list["INJECTOR_TO_THROAT_LENGTH"] * c.M2IN} in")
print("")
# print("what")
print(f"Oxidizer Tank Length: {desired_rocket_output_list["OXIDIZER_TANK_LENGTH"] * c.M2IN} in")
print(f"Oxidizer Tank Volume: {desired_rocket_output_list["OXIDIZER_TANK_VOLUME"] * c.M32L} liter")
print(f"Oxidizer Total Mass: {desired_rocket_output_list["OXIDIZER_TOTAL_MASS"] * c.KG2LB} lbm")
print(f"Fuel Tank Volume: {desired_rocket_output_list["FUEL_TANK_VOLUME"] * c.M32L} liter")
print(f"Fuel Total Mass: {desired_rocket_output_list["FUEL_TOTAL_MASS"] * c.KG2LB} lbm")
print(f"Burn Time: {desired_rocket_output_list["BURN_TIME"]} seconds")
print("")
print(f"Estimated Apogee: {desired_rocket_output_list["APOGEE"] * c.M2FT} feet")
print(f"Off the rail TWR: {desired_rocket_output_list["RAIL_EXIT_TWR"]}")
print(f"Off the rail acceleration: {desired_rocket_output_list["RAIL_EXIT_ACCELERATION"] / c.GRAVITY} G's")
print(f"Off the rail velocity: {desired_rocket_output_list["RAIL_EXIT_VELOCITY"]} m/s")
print(f"Max Acceleration: {desired_rocket_output_list["MAX_ACCELERATION"] / c.GRAVITY} G's")
print(f"Max Velocity: {desired_rocket_output_list["MAX_VELOCITY"] / 343} Mach")
print("")
print(f"Wet Mass: {desired_rocket_output_list["WET_MASS"] * c.KG2LB} lbm")
print(f"Dry Mass: {desired_rocket_output_list["DRY_MASS"] * c.KG2LB} lbm")
print(f"Total Length: {desired_rocket_output_list["TOTAL_LENGTH"] * c.M2FT} feet")
print(f"Total Impulse: {desired_rocket_output_list["TOTAL_IMPULSE"]} Newton-seconds")



# METRIC VERSION (MISSING SOME VALUES, IF YOU WANNA FIX IT JUST COMBINE THIS WITH THE IMPERIAL ONE WITH AN IF STATEMENT AND CONVERSION FACTOR)

# print(f"\n-------Inputs-------")
# print(f"Chamber Pressure: {desired_input["CHAMBER_PRESSURE"]} Pa")
# print(f"OF Ratio: {numpy_ndarray_handler.GetFrom_ndarray("OF_RATIO", constant_inputs_array, desired_input)}")
# print(f"Contraction Ratio: {desired_input["CONTRACTION_RATIO"]}")
# print(f"Fuel Tank Length: {desired_input["FUEL_TANK_LENGTH"]} meters")

# print(f"\n-------Outputs-------")
# print(f"Tank Pressure: {desired_rocket_output_list["TANK_PRESSURE"]} Pa")
# print(f"JET_THRUST: {desired_rocket_output_list["JET_THRUST"]} Newtons")
# print(f"ISP: {desired_rocket_output_list["ISP"]} seconds")
# print(f"MASS_FLOW_RATE: {desired_rocket_output_list["MASS_FLOW_RATE"]} kg/s")
# print(f"BURN_TIME: {desired_rocket_output_list["BURN_TIME"]} seconds")
# print(f"TOTAL_LENGTH: {desired_rocket_output_list["TOTAL_LENGTH"] } meter")
# print(f"CHAMBER_TEMPERATURE: {desired_rocket_output_list["CHAMBER_TEMPERATURE"]} kelvin")

# print(f"OXIDIZER_TANK_LENGTH: {desired_rocket_output_list["OXIDIZER_TANK_LENGTH"]} meter")
# print(f"OXIDIZER_TANK_VOLUME: {desired_rocket_output_list["OXIDIZER_TANK_VOLUME"] } m^3")
# print(f"OXIDIZER_TOTAL_MASS: {desired_rocket_output_list["OXIDIZER_TOTAL_MASS"]} kg")
# print(f"FUEL_TANK_VOLUME: {desired_rocket_output_list["FUEL_TANK_VOLUME"]} m^3")
# print(f"FUEL_TOTAL_MASS: {desired_rocket_output_list["FUEL_TOTAL_MASS"]} kg")
# print(f"WET_MASS: {desired_rocket_output_list["WET_MASS"]} kg")
# print(f"DRY_MASS: {desired_rocket_output_list["DRY_MASS"]} kg")

# print(f"Estimated Apogee: {desired_rocket_output_list["APOGEE"]} meter")
# print(f"Off the rail TWR: {desired_rocket_output_list["RAIL_EXIT_TWR"]}")
# print(f"Off the rail acceleration: {desired_rocket_output_list["RAIL_EXIT_ACCELERATION"] / c.GRAVITY} G's")
# print(f"Off the rail velocity: {desired_rocket_output_list["RAIL_EXIT_VELOCITY"]} m/s")
# print(f"Max Acceleration: {desired_rocket_output_list["MAX_ACCELERATION"] / c.GRAVITY} G's")
# print(f"Max Velocity: {desired_rocket_output_list["MAX_VELOCITY"] / 343} Mach")

# print(f"Total Impulse: {desired_rocket_output_list["TOTAL_IMPULSE"]} Newton-seconds")

# kill me