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




# Open RPA graph
import coding_utils.plotting as p
import pandas as pd
import inputs

RPA_df = pd.read_csv(
    "fuck_money.txt",
    delim_whitespace=True,   # values separated by spaces
    comment='#',             # ignore header/comment lines
    header=None              # no header row in data
)

RPA_df.columns = [
    "OF_RATIO", "CHAMBER_PRESSURE", "Nozzle_inl", "Nozzle_exi", "rho", "Tc",
    "M", "gamma", "k", "c_star", "Is_opt", "Is_vac",
    "Cf_opt", "Cf_vac", "c_factor"
]

OF = RPA_df['OF_RATIO'].to_numpy()
Pc = RPA_df['CHAMBER_PRESSURE'].to_numpy()

# 4. Get unique values for axes
OF_unique = np.unique(OF)
Pc_unique = np.unique(Pc)

x = Pc_unique
y = OF_unique
z = RPA_df['Tc'].to_numpy()

Y, X = np.meshgrid(x,y) # I don't know why you have to swap X and Y but you do
Z = z.reshape(len(x), len(y))

p.PlotColorMap(X, Y, Z, RPA_df['Tc'])