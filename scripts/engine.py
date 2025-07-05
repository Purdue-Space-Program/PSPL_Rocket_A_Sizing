import CEA_Wrap
import numpy as np
import coding_utils.constants as c

"""we need to input
  chamberPressure : float
        Pressure within the combustion chamber [Pa].
    exitPressure : float
        Pressure at the nozzle exit [Pa].
    fuel : str
        Name of the fuel under CEA naming conventions (e.g., "methane", "ethanol") [N/A].
    oxidizer : str
        Name of the oxidizer under CEA naming conventions (e.g., "O2") [N/A].
    mixRatio : float
        Mixture ratio of oxidizer to fuel by mass [-]."""

""" and return 
cstar : float
        Characteristic velocity of combustion products, reduced by efficiency factor [m/s].
    specificImpulse : float
        Specific impulse (Isp) of the engine, reduced by efficiency factor squared [s].
    expansionRatio : float
        Nozzle expansion ratio, area of exit to throat [-].
    fuelTemp : float
        Temperature of the fuel at the injection point [K].
    oxTemp : float
        Temperature of the oxidizer at the injection point [K].
    characteristicLength : float
        Characteristic length of the combustion chamber, based on propellant choice [m].
"""
def radius_to_area(radius):
    area = np.pi * (radius**2)
    return area

def calculate_chamber_length(throat_radius, chamber_radius, fuel_name, oxidizer_name):
    L_star = find_L_star(fuel_name, oxidizer_name)
    throat_area = radius_to_area(throat_radius)

def find_L_star(fuel_name, oxidizer_name):
    L_star = None
    if (oxidizer_name == "Liquid Oxygen"):
        if (fuel_name == "Ethanol"):
            # L_star = 40
            raise Exception("No value for L*")
        if (fuel_name == "Kerosene"):
            L_star = 50
    return L_star


