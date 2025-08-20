# import CEA_Wrap
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import coding_utils.constants as c

os.environ["CEA_USE_LEGACY"] = "1" # https://github.com/civilwargeeky/CEA_Wrap/issues/8
import CEA_Wrap as CEA
import numpy as np


EFFICIENCY_FACTOR = 0.9  # Efficiency factor for cstar and specific impulse

def RunCEA(
    chamber_pressure,
    fuel,
    oxidizer,
    OF_Ratio,
):
    # convert regular string for propellants to what CEA_wrap uses
    if fuel.lower() == "ethanol":
        fuel = CEA.Fuel("C2H5OH(L)", temp=c.T_AMBIENT)
    elif fuel.lower() == "jet-a":
        fuel = CEA.Fuel("Jet-A(L)", temp=c.T_AMBIENT)

    if oxidizer.lower() == "liquid oxygen":
        oxidizer = CEA.Oxidizer("O2(L)", temp=90) # 90 K is temperature of oxidizer upon injection into combustion (same as copperhead's sizing)


    pressure_ratio = chamber_pressure / 10 # assume exit pressure is a constantly at the pressure of air a bit above sea level

    rocket = CEA.RocketProblem(
        pressure =       chamber_pressure,
        pip =            pressure_ratio, # pip is "Pressure ratio of chamber pressure to exit pressure." github.com/civilwargeeky/CEA_Wrap/blob/main/README.md#rocket-problem-constructor-additional-parameters
        materials =      [fuel, oxidizer],
        o_f =            OF_Ratio,
        pressure_units = "psi",
    )

    cea_results = rocket.run()
    
    
    
    return(cea_results.isp)




def size_engine(chamber_radius, fuel_name, oxidizer_name, contraction_ratio):
    chamber_area = radius_to_area(chamber_radius)
    throat_area = chamber_area / contraction_ratio
    throat_radius = area_to_radius(throat_area)
    chamber_length = calculate_chamber_length(throat_area, chamber_area, fuel_name, oxidizer_name)
    return (chamber_radius, chamber_length, throat_radius)

def area_to_radius(area):
    radius = (area/np.pi)**0.5
    return radius

def radius_to_area(radius):
    area = np.pi * (radius**2)
    return area

def calculate_chamber_length(throat_area, chamber_area, fuel_name, oxidizer_name):
    L_star = find_L_star(fuel_name, oxidizer_name)
    chamber_length = (throat_area * L_star) / (chamber_area)
    return chamber_length

def find_L_star(fuel_name, oxidizer_name):
    L_star = None
    if (oxidizer_name == "Liquid Oxygen"):
        if (fuel_name == "Ethanol"):
            # L_star = ??? * c.IN2M
            raise ValueError("No value for L*")

        if (fuel_name == "Jet-A"):
            L_star = 45 * c.IN2M # page 87 of nasa sp-125 https://ntrs.nasa.gov/citations/19710019929
    return L_star

def find_mass_flow_rate(throat_area, characteristic_velocity, chamber_pressure):
    mass_flow_rate = (chamber_pressure * throat_area) / (characteristic_velocity)
    return mass_flow_rate


if __name__ == "__main__":
    print(RunCEA(500, "ethanol", "liquid oxygen", 1.1)) # should be 255.433231397