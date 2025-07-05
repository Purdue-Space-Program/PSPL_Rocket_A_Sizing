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


import numpy as np

chamberpressure = input("What is your chamber pressure? ")
exitpressure = input("What is your exit pressure? ")
fuel = input("What is your fuel type? ")
oxidizer = input("What oxidizer are you using? ")
fuelmixratio = input("What is your fuel mix ratio? ")


def contraction_ratio_to_nozzle_area():
        print("Hello World")
contraction_ratio_to_nozzle_area()

def diameter_to_area(diameter):
    area = np.pi*((diameter/2)**2)
    return area

print(diameter_to_area(3))
