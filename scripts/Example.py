# Import the things we need to do our task. "F" and "O" are aliases for fuel and oxidizer
from CEA_Wrap import Fuel, Oxidizer, RocketProblem

#############################################################################
## Example 1: Simple 1 fuel 1 oxidizer liquid rocket
#############################################################################

# Cyrogenic fuels
h2 = Fuel("H2(L)", temp=20) # Liquid H2, Temp in Kelvin
lox = Oxidizer("O2(L)", temp=90)
# Rocket at 2000psi and supersonic area ratio of 5
problem1 = RocketProblem(pressure=150, materials=[h2, lox], phi=1, sup=5)
results = problem1.run()

# For a full listing of available members, see the documentation at https://github.com/civilwargeeky/CEA_Wrap
print("Stoichiometric, cryogenic rocket")
exit_pressure    = results.p
chamber_pressure = results.c_p
exit_cp          = results.cp
chamber_cp       = results.c_cp
exit_isp         = results.isp
throat_isp       = results.t_isp
print("Pressures (bar):", exit_pressure, chamber_pressure)
print("Cp (kJ/(kg*K):", exit_cp, chamber_cp)
print("Isp (s):", exit_isp, throat_isp)

# We can also access the exhaust products (in default mol fraction)
percent_water = results.prod_e.H2O # Can also do results.prod_e["H2O"]
print("Percent Water in exhaust:", percent_water)

# Now, let's increase our propellant temperature and see how that impacts isp
# Because we are going above the material boiling points, we will have to switch to gaseous hydrogen and oxygen
h2 = Fuel("H2") # Default temperature is 297
o2 = Oxidizer("O2")
problem1.set_materials([h2, o2])
results = problem1.run()
print("Hotter Isp:", results.isp, results.t_isp)

# Now let's increase our propellant temperature even more!
# We can just modify the materials in-place since they are already gas phase
h2.set_temp(800) # 500C
o2.set_temp(800)
results = problem1.run()
print("Even Hotter Isp:", results.isp, results.t_isp)
print("Wow, that didn't change very much...")
