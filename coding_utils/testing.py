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


# # coolprop ullage collapse testing
# from CoolProp.CoolProp import PropsSI
# import CoolProp.CoolProp as CP


# total_ox_tank_volume = 11.3 * c.L2M3
# total_fuel_tank_volume = 19 * c.L2M3

# tank_pressure = 100 * c.PSI2PA

# COPV_pressure_1 = 4500 * c.PSI2PA
# COPV_temp_1 = c.T_AMBIENT + 15
# COPV_volume = 3 * c.L2M3

# COPV_density_1 = PropsSI("D", "P", COPV_pressure_1, "T", COPV_temp_1, "nitrogen")
# print(f"COPV_density_1: {COPV_density_1:.2f}")
# COPV_mass_1 = COPV_density_1 * COPV_volume
# print(f"COPV_mass_1: {COPV_mass_1:.2f}")
# COPV_entropy_1 = PropsSI("S", "P", COPV_pressure_1, "T", COPV_temp_1, "nitrogen")
# print(f"COPV_entropy_1: {COPV_entropy_1:.2f}")


# ox_tank_density = PropsSI("D", "P", tank_pressure, "Q", 1, "nitrogen")
# print(f"ox_tank_density: {ox_tank_density:.2f}")
# ox_tank_mass = ox_tank_density * total_ox_tank_volume
# print(f"ox_tank_mass: {ox_tank_mass:.2f}")

# if (COPV_mass_1 - ox_tank_mass) <= 0.01: # adding small amount for  floating point bs!
#     raise ValueError("you ran out of pressurant :(")

# COPV_mass_2 = COPV_mass_1 - ox_tank_mass
# COPV_density_2 = COPV_mass_2 / COPV_volume
# COPV_entropy_2 = COPV_entropy_1 # isentropic expansion
# COPV_pressure_2 = PropsSI("P", "D", COPV_density_2, "S", COPV_entropy_2, "nitrogen")
# COPV_temp_2 = PropsSI("T", "D", COPV_density_2, "S", COPV_entropy_2, "nitrogen")
# print(f"COPV_pressure_2: {COPV_pressure_2:.2f}")
# print(f"COPV_temp_2: {COPV_temp_2 - 273.15:.2f}")

# COPV_temp_3 = 0 # initial value to start the while loop that is certainly below the copv real temp
# fuel_tank_temp_guess = COPV_temp_2 # initial guess that is certainly above the real fuel temp
# fuel_tank_temp_actual = 0 # the temperature the nitrogen in fuel tank would be if the initial guess is true
# while fuel_tank_temp_guess > fuel_tank_temp_actual:
  
#   # i am ignoring the work done by the gas expanding into the fuel tank and that is an error that i need to fix... later
#   fuel_tank_density = PropsSI("D", "P", tank_pressure, "T", fuel_tank_temp_guess, "nitrogen")
#   # print(f"fuel_tank_density: {fuel_tank_density:.2f}")
#   fuel_tank_mass = fuel_tank_density * total_fuel_tank_volume
#   # print(f"fuel_tank_mass: {fuel_tank_mass:.2f}")
#   print(f"\nCOPV_temp_3: {COPV_temp_3:.2f}")
#   print(f"fuel_tank_temp: {fuel_tank_temp_guess:.2f}")
  
#   if (COPV_mass_2 - (fuel_tank_mass)) <= 0.01:  # check if under a small amount (instead of zero) for  floating point bs!
#     raise ValueError("you ran out of pressurant :(")
  
#   COPV_mass_3 = COPV_mass_2 - fuel_tank_mass
#   print(f"COPV_mass_3: {COPV_mass_3:.2f}")
#   COPV_density_3 = COPV_mass_3 / COPV_volume
#   COPV_entropy_3 = COPV_entropy_2 # isentropic expansion
#   COPV_pressure_3 = PropsSI("P", "D", COPV_density_3, "S", COPV_entropy_3, "nitrogen")
#   COPV_temp_3 = PropsSI("T", "D", COPV_density_3, "S", COPV_entropy_3, "nitrogen")

#   fuel_tank_temp_actual = PropsSI("T", "P", tank_pressure, "S", COPV_entropy_3, "nitrogen")

#   fuel_tank_temp_guess -= 1

# fuel_tank_temp_real = fuel_tank_temp_guess

# if (COPV_pressure_3 * 2) < tank_pressure:
#     raise ValueError("you ran out of pressurant :(")

  


# # print(f"final fuel_tank_density: {PropsSI("D", "P", tank_pressure, "T", fuel_tank_temp_real, "nitrogen")}")
# # print(f"final COPV_temp_3: {COPV_temp_3}")
# # print(f"final COPV_mass_3: {COPV_mass_3}")
# # print(f"final fuel_tank_temp_real: {fuel_tank_temp_real - 273.15}")
# # print(f"final COPV_pressure_3: {COPV_pressure_3 * c.PA2PSI}")
















# # COPV_temperature_2 = PropsSI("T", "D", COPV_density_2, "S", COPV_entropy_2, "nitrogen")
# # print(f"COPV_temperature_2: {COPV_temperature_2:.2f}")

# # nitrogen_gamma = 1.4
# # fuel_internal_energy = tank_pressure*fuel_tank_volume / (nitrogen_gamma - 1)
# # print(f"fuel_internal_energy: {fuel_internal_energy:.2f}")

# # # fuel_tank_mass = (tank_pressure*fuel_tank_volume) / ()
# # # T = ?
# # # n = tank_pressure*fuel_tank_volume / 8.31 * T

# # # fuel_tank_density = PropsSI("D", "UMolar", fuel_internal_energy/n, "P", tank_pressure, "nitrogen")
# # # fuel_tank_mass = fuel_tank_density * fuel_tank_volume

# # # if (COPV_mass_2 - fuel_tank_mass) < 0:
# # #     raise ValueError

# # # COPV_mass_3 = COPV_mass_2 - fuel_tank_mass
# # # COPV_density_3 = COPV_mass_3 / COPV_volume
# # # COPV_entropy_3 = COPV_entropy_2 # isentropic expansion
# # # COPV_pressure_3 = PropsSI("P", "D", COPV_density_3, "S", COPV_entropy_3, "nitrogen")

# # fuel_boundary_work = ((COPV_pressure_2*COPV_volume) - (COPV_pressure_3*COPV_volume)) / (nitrogen_gamma - 1)

# # energy_used_for_fuel = fuel_internal_energy + fuel_boundary_work

# # COPV_internal_energy_2 = PropsSI("UMolar", "D", COPV_density_2, "S", COPV_entropy_2, "nitrogen")
# # COPV_internal_energy_3 = COPV_internal_energy_2 - energy_used_for_fuel



# # # pressurant_in_COPV_density = PropsSI("D", "P", COPV_pressure, "T", c.T_AMBIENT + 15, "nitrogen")
# # # pressurant_in_COPV_entropy = PropsSI("S", "P", COPV_pressure, "T", c.T_AMBIENT + 15, "nitrogen")
# # # pressurant_in_fuel_tank_entropy = pressurant_in_COPV_entropy

# # # pressurant_in_ox_density = PropsSI("D", "P", tank_pressure, "Q", 1, "nitrogen")
# # # pressurant_in_fuel_density = PropsSI("D", "P", tank_pressure, "S", pressurant_in_fuel_tank_entropy, "nitrogen")

# # # pressurant_in_ox_tank_before_collapse_density = PropsSI("D", "P", tank_pressure, "S", pressurant_in_fuel_tank_entropy, "nitrogen")
# # # pressurant_in_ox_tank_after_collapse_density = PropsSI("D", "P", tank_pressure, "Q", 1, "nitrogen")


# # # pressurant_in_COPV_to_in_ox_density_ratio = pressurant_in_COPV_density/pressurant_in_ox_density
# # # pressurant_in_COPV_to_in_fuel_density_ratio = pressurant_in_COPV_density/pressurant_in_fuel_density

# # # print(f"pressurant_in_COPV_to_in_ox_density_ratio: {pressurant_in_COPV_to_in_ox_density_ratio:.2f}")
# # # print(f"pressurant_in_COPV_to_in_fuel_density_ratio: {pressurant_in_COPV_to_in_fuel_density_ratio:.2f}")

# # # needed_COPV_volume_for_ox =  (total_ox_tank_volume + (COPV_volume * 2))/pressurant_in_COPV_to_in_ox_density_ratio
# # # needed_COPV_volume_for_fuel =  (total_fuel_tank_volume + (COPV_volume * 2))/pressurant_in_COPV_to_in_fuel_density_ratio

# # # needed_COPV_volume = needed_COPV_volume_for_ox + needed_COPV_volume_for_fuel

# # # print(f"need_copv_volume: {needed_COPV_volume * c.M32L:.2f}")






# # # cea_wrap looping testing

# # # Example for how to loop through materials and collate the properties you are concerned about
# # # Note: To run this example you will need numpy and matplotlib

# # try:
# #   import numpy as np
# #   import matplotlib.pyplot as plt
# # except ImportError:
# #   print("You will need to install matplotlib and numpy to run this example")
# #   import sys
# #   sys.exit(1)
# # from time import time

# # # Only import things we'll need for this problem
# # from CEA_Wrap import Fuel, Oxidizer, RocketProblem, DataCollector

# # # For all the examples in this problem we'll use Aluminized AP/HTPB as the reactants
# # ethanol = Fuel("C2H5OH(L)", temp=c.T_AMBIENT)
# # LOx = Oxidizer("O2(L)", temp=90)
# # m_list = [ethanol, LOx] # for convenience so I can pass it into all problems



# # problem = CEA.RocketProblem(
# #             materials = m_list,
# #             pressure =  100,
# #             pressure_units = "psi",
# #     )


# # ## Example 1: Using DataCollector objects (Recommended)
# # print("Running Data Collector Case")
# # OF_ratios = np.linspace(0.1, 2, 90)
# # collector = DataCollector("c_p", "c_t") # want to collect chamber temperature

# # for OF_ratio in OF_ratios:
# #   problem.set_o_f(OF_ratio)
# #   collector.add_data(problem.run()) # adds all desired variables to collector
  
# # plt.plot(OF_ratios, np.asarray(collector.c_t)) #* (10**5) * c.PA2PSI) # could also do collector["c_t"] for the same effect
# # plt.title("Collector Pressure vs Temperature")
# # plt.xlabel("OF Ratio")
# # plt.ylabel("Chamber Temperature (K)")
# # plt.show()






# # # Example 7: Trying the same thing threaded
# # print("Running super-fast multi-threaded case")
# # from concurrent.futures import ThreadPoolExecutor

# # collector = DataCollector("c_t", "ivac") # Show chamber temperature and isp dependence on % aluminum

# # def inner_function(al_percent): # This function is just the inside of the previous loop
# #   # It is wise to re-define our materials and function for each call to this function, so that different runs do not over-write each other's material amounts
# #   aluminum = Fuel("AL(cr)", wt=12) # (cr) for "crystalline" or condensed phase
# #   htpb = Fuel("HTPB", wt=14) # This was added at Purdue so doesn't include (cr) in the name
# #   ap = Oxidizer("NH4CLO4(I)", wt=74) # ammonium perchlorate (form I, specified at room temperature)
# #   aluminum.wt = al_percent
# #   # NOTE: CEA doesn't like it when a material has 0%, so at 0% the material is not entered into the .inp file
# #   ap.wt = (100-12-al_percent)
# #   # We also need to re-define our problem in each function so that we do not accidentally over-write problem components in other threads
# #   problem = RocketProblem(materials=[aluminum, htpb, ap])
# #   problem.set_absolute_o_f() # change our o/f to reflect situation
# #   collector.add_data(problem.run(), al_percent) # Because the threaded cases may run out of order, we add our independent variable to our data collector, so we can sort later

# # start_time = time()
# # with ThreadPoolExecutor() as thread_pool:
# #   thread_pool.map(inner_function, percent_aluminum)
# # collector.sort() # Sort our data collector by our independent variable
# # end_time = time()
# # print("Completed in {}s! {} CEA calls per second".format(end_time-start_time, 250/(end_time-start_time)))

# # # # Example for how to loop through materials and collate the properties you are concerned about
# # # # Note: To run this example you will need numpy and matplotlib

# # # try:
# # #   import numpy as np
# # #   import matplotlib.pyplot as plt
# # # except ImportError:
# # #   print("You will need to install matplotlib and numpy to run this example")
# # #   import sys
# # #   sys.exit(1)
# # # from time import time

# # # # Only import things we'll need for this problem
# # # from CEA_Wrap import Fuel, Oxidizer, RocketProblem, DataCollector

# # # # For all the examples in this problem we'll use Aluminized AP/HTPB as the reactants
# # # aluminum = Fuel("AL(cr)", wt=12) # (cr) for "crystalline" or condensed phase
# # # htpb = Fuel("HTPB", wt=14) # This was added at Purdue so doesn't include (cr) in the name
# # # ap = Oxidizer("NH4CLO4(I)", wt=74) # ammonium perchlorate (form I, specified at room temperature)
# # # m_list = [aluminum, htpb, ap] # for convenience so I can pass it into all problems

# # # # We'll actually use the same problem for the first 3 examples
# # # problem = RocketProblem(materials=m_list)
# # # problem.set_absolute_o_f() # have it calculate o_f for us from material percentage

# # # ## Example 1: Using DataCollector objects (Recommended)
# # # print("Running Data Collector Case")
# # # pressures = np.linspace(1000, 2000, 25) # pressures from 1000 to 2000
# # # collector = DataCollector("c_t") # want to collect chamber temperature
# # # for pressure in pressures:
# # #   problem.set_pressure(pressure)
# # #   collector.add_data(problem.run()) # adds all desired variables to collector
  
# # # plt.plot(pressures, collector.c_t) # could also do collector["c_t"] for the same effect
# # # plt.title("Collector Pressure vs Temperature")
# # # plt.xlabel("Pressure (psi)")
# # # plt.ylabel("Chamber Temperature (K)")
# # # plt.show()


# # # ## Example 2: Using standard python arrays
# # # print("Running Python Array Case")
# # # pressures = [1000 + i*40 for i in range(25)] # pressures from 1000 to 2000
# # # temperatures = []
# # # for pressure in pressures:
# # #   problem.set_pressure(pressure)
# # #   data = problem.run()
# # #   temperatures.append(data.c_t) # append chamber temperature

# # # plt.plot(pressures, temperatures)
# # # plt.title("Python Arrays Pressure vs Temperature")
# # # plt.xlabel("Pressure (psi)")
# # # plt.ylabel("Chamber Temperature (K)")
# # # plt.show()


# # # ## Example 3: Using numpy arrays
# # # print("Running Numpy Array Case")
# # # arr_size = 25 # 25 runs of CEA
# # # pressures = np.linspace(1000, 2000, arr_size) # pressures from 1000 to 2000
# # # temperatures = np.zeros(arr_size) # initialize with 0s
# # # for i, pressure in enumerate(pressures):
# # #   problem.set_pressure(pressure)
# # #   data = problem.run()
# # #   temperatures[i] = data.c_t # set current chamber temperature

# # # plt.plot(pressures, temperatures)
# # # plt.title("Numpy Pressure vs Temperature")
# # # plt.xlabel("Pressure (psi)")
# # # plt.ylabel("Chamber Temperature (K)")
# # # plt.show()


# # # ## Example 4: Terrible no good using numpy arrays to get all your properties
# # # print("Running terrible Numpy Array Case")
# # # arr_size = 30 # runs of CEA
# # # pressures = np.linspace(1000, 2000, arr_size) # pressures from 1000 to 2000
# # # # Define our empty arrays for every property
# # # # It would be the same for python arrays
# # # t = np.zeros(arr_size)
# # # isp = np.zeros(arr_size)
# # # cf = np.zeros(arr_size)
# # # gamma = np.zeros(arr_size)
# # # cstar = np.zeros(arr_size)
# # # mach = np.zeros(arr_size)
# # # exit_cp = np.zeros(arr_size)
# # # chamber_cp = np.zeros(arr_size)
# # # percent_hcl = np.zeros(arr_size)
# # # percent_alumina = np.zeros(arr_size)
# # # # Run the problem at different pressures
# # # for i, pressure in enumerate(pressures):
# # #   problem.set_pressure(pressure)
# # #   data = problem.run()
# # #   t[i] = data.c_t # chamber temperature
# # #   isp[i] = data.ivac # vacuum isp
# # #   cf[i] = data.cf # exit thrust coefficient
# # #   gamma[i] = data.gamma # exit real ratio of specific heats
# # #   cstar[i] = data.cstar # characteristic velocity
# # #   mach[i] = data.mach # exit mach number
# # #   exit_cp[i] = data.cp # exit specific heat
# # #   chamber_cp[i] = data.c_cp # chamber specific heat
# # #   percent_hcl[i] = data.prod_e.HCL
# # #   try: # Fun fact: there may not be any liquid alumina in the exhaust products, so you have to do this
# # #        #    For every single product you want to look at.
# # #        #    blech
# # #     percent_alumina[i] = data.prod_e["AL2O3(L)"]
# # #   except KeyError:
# # #     percent_alumina[i] = 0
# # # # I'm not going to plot these, but you get the idea.


# # # ## Example 5: Using the awesome DataCollector objects to make your life easy
# # # print("Running the awesome super cool Data Collector Case")
# # # pressures = np.linspace(1000, 2000, 30) # pressures from 1000 to 2000
# # # # Define a collector to collect all these properties. Also get composition at the exit for these product species
# # # #   If you wanted to define keys for the chamber, use "chamber_keys" instead
# # # #   NOTE: You cannot have chamber and exit keys in the same collector. If you want both, use multiple collectors
# # # collector = DataCollector("c_t", "ivac", "cf", "gamma", "cstar", "mach", "cp", "c_cp", exit_keys=["HCL", "AL2O3(L)"])
# # # for pressure in pressures:
# # #   problem.set_pressure(pressure)
# # #   collector.add_data(problem.run()) # adds all desired variables to collector
# # # # And that's it! Now we can access our array of chamber temperatures with
# # # collector.c_t
# # # # And our mol_ratios of HCL in the exhaust with
# # # collector.HCL
# # # # The really cool thing is that we don't need to worry about species not existing, because they will automatically be
# # # #   set to 0 in the correct position of the array
# # # # Fun thing! You can also write your collectors to csv
# # # collector.to_csv("looper.csv")


# # # ## Example 6: Varying ratios of materials
# # # print("Running various aluminum contents (may take a bit)")
# # # percent_aluminum = np.linspace(0, 25, 250) # run percentage of aluminum from 0% to 15%
# # # # reminder: 12% HTPB, and we'll reduce the amount of AP to compensate
# # # collector = DataCollector("c_t", "ivac") # Show chamber temperature and isp dependence on % aluminum

# # # start_time = time()
# # # for al_percent in percent_aluminum:
# # #   aluminum.wt = al_percent
# # #   # NOTE: CEA doesn't like it when a material has 0%, so at 0% the material is not entered into the .inp file
# # #   ap.wt = (100-12-al_percent)
# # #   problem.set_absolute_o_f() # change our o/f to reflect situation
# # #   collector.add_data(problem.run())
# # # end_time = time()
# # # print("Completed in {}s! {} CEA calls per second".format(end_time-start_time, 250/(end_time-start_time)))

# # # # Adapted from https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
# # # fig, ax1 = plt.subplots()
# # # color = 'tab:red'
# # # ax1.set_xlabel('Percentage Aluminum (%)')
# # # ax1.set_ylabel('Temperature', color=color)
# # # ax1.plot(percent_aluminum, collector.c_t, color=color)
# # # ax1.tick_params(axis='y', labelcolor=color)
# # # ax2 = ax1.twinx()
# # # color = 'tab:blue'
# # # ax2.set_ylabel('Vacuum Isp (s)', color=color)
# # # ax2.plot(percent_aluminum, collector.ivac, color=color)
# # # ax2.tick_params(axis='y', labelcolor=color)
# # # fig.tight_layout()  # otherwise the right y-label is slightly clipped
# # # plt.show()

# # # # Example 7: Trying the same thing threaded
# # # print("Running super-fast multi-threaded case")
# # # from concurrent.futures import ThreadPoolExecutor

# # # collector = DataCollector("c_t", "ivac") # Show chamber temperature and isp dependence on % aluminum

# # # def inner_function(al_percent): # This function is just the inside of the previous loop
# # #   # It is wise to re-define our materials and function for each call to this function, so that different runs do not over-write each other's material amounts
# # #   aluminum = Fuel("AL(cr)", wt=12) # (cr) for "crystalline" or condensed phase
# # #   htpb = Fuel("HTPB", wt=14) # This was added at Purdue so doesn't include (cr) in the name
# # #   ap = Oxidizer("NH4CLO4(I)", wt=74) # ammonium perchlorate (form I, specified at room temperature)
# # #   aluminum.wt = al_percent
# # #   # NOTE: CEA doesn't like it when a material has 0%, so at 0% the material is not entered into the .inp file
# # #   ap.wt = (100-12-al_percent)
# # #   # We also need to re-define our problem in each function so that we do not accidentally over-write problem components in other threads
# # #   problem = RocketProblem(materials=[aluminum, htpb, ap])
# # #   problem.set_absolute_o_f() # change our o/f to reflect situation
# # #   collector.add_data(problem.run(), al_percent) # Because the threaded cases may run out of order, we add our independent variable to our data collector, so we can sort later

# # # start_time = time()
# # # with ThreadPoolExecutor() as thread_pool:
# # #   thread_pool.map(inner_function, percent_aluminum)
# # # collector.sort() # Sort our data collector by our independent variable
# # # end_time = time()
# # # print("Completed in {}s! {} CEA calls per second".format(end_time-start_time, 250/(end_time-start_time)))


# # # # # Adapted from https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html
# # # # fig, ax1 = plt.subplots()
# # # # color = 'tab:red'
# # # # ax1.set_xlabel('Percentage Aluminum (%)')
# # # # ax1.set_ylabel('Temperature', color=color)
# # # # ax1.plot(percent_aluminum, collector.c_t, color=color)
# # # # ax1.tick_params(axis='y', labelcolor=color)
# # # # ax2 = ax1.twinx()
# # # # color = 'tab:blue'
# # # # ax2.set_ylabel('Vacuum Isp (s)', color=color)
# # # # ax2.plot(percent_aluminum, collector.ivac, color=color)
# # # # ax2.tick_params(axis='y', labelcolor=color)
# # # # fig.tight_layout()  # otherwise the right y-label is slightly clipped
# # # # plt.show()