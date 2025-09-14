import numpy as np

import os
os.environ["CEA_USE_LEGACY"] = "1" # https://github.com/civilwargeeky/CEA_Wrap/issues/8
import CEA_Wrap as CEA
import constants as c

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



############# uhhhhhhh
# x = np.array([[(1,2), (1,2)], [(1,2), (1,2)]])
# print(x)

# x = np.array([[[1,2], [1,2,3]], [[1,2], [1,2,3]]])
# print(x)

# ########### check size of element in ndarray
# x = np.array(3.14)
# # print(x, x.dtype)
# # print(x.size)

# # print(len("string"))
# # print(len(["string1","string2"]))
# # print(type("string"))
# # print(type(["string1","string2"]))

# x = np.array(["string1","string2"])
# # print(x.size)

# def FindNumberOfSubElements(unknown_variable):
#     num_sub_elements = 0
    
#     # check for case when sub_element(s) are a string
#     if isinstance(unknown_variable, str):
#         num_sub_elements = 1  
    
#     # check for case when sub_elements are in an ndarray
#     elif hasattr(unknown_variable, 'dtype'):
#         num_sub_elements = unknown_variable.size
    
#     else:
#          num_sub_elements = len(unknown_variable)
#     return num_sub_elements

# for test in [["string1","string2"], np.array(["string1","string2"]), "string"]:
#     print(f"{test} = {FindNumberOfSubElements(test)}")



# string testing
# test = "HeLlO"
# test2 = ["HELLO", "BYE"]
# print(test.lower())




# why the fuck is the CEA website down

# M vs MW (some bullshit)
# CEA_fuel_name = CEA.Fuel("H2", temp=c.T_AMBIENT)
# cea_oxidizer_name = CEA.Oxidizer("O2", temp=c.T_AMBIENT)

# for of_ratio in [100000000, 0.00001, 1]:
#     rocket = CEA.RocketProblem(
#             pressure =       50,
#             pip =            2,
#             materials =      [CEA_fuel_name, cea_oxidizer_name],
#             o_f =            of_ratio,
#             pressure_units = "psi",
#         )

#     cea_results = rocket.run()
#     print(cea_results.c_m)


# CEA_fuel_name = CEA.Fuel("H2(L)", temp=20)
# cea_oxidizer_name = CEA.Oxidizer("O2(L)", temp=90)

# for of_ratio in [1, 1.5, 2]:
#     rocket = CEA.RocketProblem(
#             pressure =       200,
#             pip =            2,
#             materials =      [CEA_fuel_name, cea_oxidizer_name],
#             o_f =            of_ratio,
#             pressure_units = "psi",
#         )

#     cea_results = rocket.run()
#     print(cea_results.isp)




# # Open RPA graph
# import coding_utils.plotting as p
# import pandas as pd
# import inputs

# RPA_df = pd.read_csv(
#     "fuck_money.txt",
#     delim_whitespace=True,   # values separated by spaces
#     comment='#',             # ignore header/comment lines
#     header=None              # no header row in data
# )

# RPA_df.columns = [
#     "OF_RATIO", "CHAMBER_PRESSURE", "Nozzle_inl", "Nozzle_exi", "rho", "Tc",
#     "M", "gamma", "k", "c_star", "Is_opt", "Is_vac",
#     "Cf_opt", "Cf_vac", "c_factor"
# ]

# OF = RPA_df['OF_RATIO'].to_numpy()
# Pc = RPA_df['CHAMBER_PRESSURE'].to_numpy()

# # 4. Get unique values for axes
# OF_unique = np.unique(OF)
# Pc_unique = np.unique(Pc)

# x = Pc_unique
# y = OF_unique
# z = RPA_df['Tc'].to_numpy()

# Y, X = np.meshgrid(x,y) # I don't know why you have to swap X and Y but you do
# Z = z.reshape(len(x), len(y))

# p.PlotColorMap(X, Y, Z, RPA_df['Tc'])


# coolprop ullage collapse testing
from CoolProp.CoolProp import PropsSI
import CoolProp.CoolProp as CP


# total_ox_tank_volume = 6 * c.L2M3
# total_fuel_tank_volume = 11 * c.L2M3


COPV_pressure_1 = 4500 * c.PSI2PA
COPV_temp_1 = c.T_AMBIENT + 15
COPV_volume = 3 * c.L2M3

COPV_density_1 = PropsSI("D", "P", COPV_pressure_1, "T", COPV_temp_1, "nitrogen")
print(f"COPV_density_1: {COPV_density_1:.2f}")

COPV_mass_1 = COPV_density_1 * COPV_volume
print(f"COPV_mass_1: {COPV_mass_1:.2f}")

COPV_entropy_1 = PropsSI("S", "P", COPV_pressure_1, "T", COPV_temp_1, "nitrogen")
print(f"COPV_entropy_1: {COPV_entropy_1:.2f}")


tank_pressure = 100 * c.PSI2PA
ox_tank_volume = 15 * c.L2M3
fuel_tank_volume = 20 * c.L2M3

ox_tank_density = PropsSI("D", "P", tank_pressure, "Q", 1, "nitrogen")
print(f"ox_tank_density: {ox_tank_density:.2f}")

ox_tank_mass = ox_tank_density * ox_tank_volume
print(f"ox_tank_mass: {ox_tank_mass:.2f}")


if (COPV_mass_1 - ox_tank_mass) < 0:
    raise ValueError

COPV_mass_2 = COPV_mass_1 - ox_tank_mass
COPV_density_2 = COPV_mass_2 / COPV_volume
COPV_entropy_2 = COPV_entropy_1 # isentropic expansion
COPV_pressure_2 = PropsSI("P", "D", COPV_density_2, "S", COPV_entropy_2, "nitrogen")
print(f"COPV_pressure_2: {COPV_pressure_2:.2f}")

COPV_temperature_2 = PropsSI("T", "D", COPV_density_2, "S", COPV_entropy_2, "nitrogen")
print(f"COPV_temperature_2: {COPV_temperature_2:.2f}")

nitrogen_gamma = 1.4
fuel_internal_energy = tank_pressure*fuel_tank_volume / (nitrogen_gamma - 1)
print(f"fuel_internal_energy: {fuel_internal_energy:.2f}")

# fuel_tank_mass = (tank_pressure*fuel_tank_volume) / ()
# T = ?
# n = tank_pressure*fuel_tank_volume / 8.31 * T

# fuel_tank_density = PropsSI("D", "UMolar", fuel_internal_energy/n, "P", tank_pressure, "nitrogen")
# fuel_tank_mass = fuel_tank_density * fuel_tank_volume

# if (COPV_mass_2 - fuel_tank_mass) < 0:
#     raise ValueError

# COPV_mass_3 = COPV_mass_2 - fuel_tank_mass
# COPV_density_3 = COPV_mass_3 / COPV_volume
# COPV_entropy_3 = COPV_entropy_2 # isentropic expansion
# COPV_pressure_3 = PropsSI("P", "D", COPV_density_3, "S", COPV_entropy_3, "nitrogen")

fuel_boundary_work = ((COPV_pressure_2*COPV_volume) - (COPV_pressure_3*COPV_volume)) / (nitrogen_gamma - 1)

energy_used_for_fuel = fuel_internal_energy + fuel_boundary_work

COPV_internal_energy_2 = PropsSI("UMolar", "D", COPV_density_2, "S", COPV_entropy_2, "nitrogen")
COPV_internal_energy_3 = COPV_internal_energy_2 - energy_used_for_fuel



# pressurant_in_COPV_density = PropsSI("D", "P", COPV_pressure, "T", c.T_AMBIENT + 15, "nitrogen")
# pressurant_in_COPV_entropy = PropsSI("S", "P", COPV_pressure, "T", c.T_AMBIENT + 15, "nitrogen")
# pressurant_in_fuel_tank_entropy = pressurant_in_COPV_entropy

# pressurant_in_ox_density = PropsSI("D", "P", tank_pressure, "Q", 1, "nitrogen")
# pressurant_in_fuel_density = PropsSI("D", "P", tank_pressure, "S", pressurant_in_fuel_tank_entropy, "nitrogen")

# pressurant_in_ox_tank_before_collapse_density = PropsSI("D", "P", tank_pressure, "S", pressurant_in_fuel_tank_entropy, "nitrogen")
# pressurant_in_ox_tank_after_collapse_density = PropsSI("D", "P", tank_pressure, "Q", 1, "nitrogen")


# pressurant_in_COPV_to_in_ox_density_ratio = pressurant_in_COPV_density/pressurant_in_ox_density
# pressurant_in_COPV_to_in_fuel_density_ratio = pressurant_in_COPV_density/pressurant_in_fuel_density

# print(f"pressurant_in_COPV_to_in_ox_density_ratio: {pressurant_in_COPV_to_in_ox_density_ratio:.2f}")
# print(f"pressurant_in_COPV_to_in_fuel_density_ratio: {pressurant_in_COPV_to_in_fuel_density_ratio:.2f}")

# needed_COPV_volume_for_ox =  (total_ox_tank_volume + (COPV_volume * 2))/pressurant_in_COPV_to_in_ox_density_ratio
# needed_COPV_volume_for_fuel =  (total_fuel_tank_volume + (COPV_volume * 2))/pressurant_in_COPV_to_in_fuel_density_ratio

# needed_COPV_volume = needed_COPV_volume_for_ox + needed_COPV_volume_for_fuel

# print(f"need_copv_volume: {needed_COPV_volume * c.M32L:.2f}")







# 3d plot testing