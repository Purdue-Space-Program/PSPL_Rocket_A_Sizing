# import CEA_Wrap
import numpy as np
from scipy import constants
from scipy.constants import gas_constant
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
            # L_star = 40
            raise ValueError("No value for L*")
        if (fuel_name == "Kerosene"):
            L_star = 50
    return L_star


def get_characteristic_velocity(Oxidizer, Fuel):
    if(Oxidizer == "Liquid Oxygen"):
        if(Fuel == "Ethanol"):
            return 1700
        if(Fuel == "Kerosene"):
            return 1800
    raise Exception("Put in a value")

def find_mass_flow_rate(throat_area, characteristic_velocity, chamber_pressure):
    mass_flow_rate = (chamber_pressure * throat_area) / (characteristic_velocity)
    return mass_flow_rate

def get_y(Oxidizer, Fuel):
    if(Oxidizer == "Liquid Oxygen"):
        if(Fuel == "Kerosene"):
            return 1.24
        if(Fuel == "Methane"):
            return 1.069

def find_exaust_velocity(Oxidizer, Fuel, Tc, Pe, Pc,):
    g = constants.g
    R = gas_constant
    y = get_y(Oxidizer, Fuel)
    exaust_velocity = ((2*g*y)/(y-1))(R*Tc)((1-(Pe/Pc))**((y-1)/y))
    return exaust_velocity