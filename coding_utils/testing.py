import numpy as np

import os
os.environ["CEA_USE_LEGACY"] = "1" # https://github.com/civilwargeeky/CEA_Wrap/issues/8
import CEA_Wrap as CEA
import constants as c

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


CEA_fuel_name = CEA.Fuel("H2(L)", temp=20)
cea_oxidizer_name = CEA.Oxidizer("O2(L)", temp=90)

for of_ratio in [1, 1.5, 2]:
    rocket = CEA.RocketProblem(
            pressure =       200,
            pip =            2,
            materials =      [CEA_fuel_name, cea_oxidizer_name],
            o_f =            of_ratio,
            pressure_units = "psi",
        )

    cea_results = rocket.run()
    print(cea_results.isp)