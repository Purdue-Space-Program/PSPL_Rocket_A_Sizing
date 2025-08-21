import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import coding_utils.constants as c

os.environ["CEA_USE_LEGACY"] = "1" # https://github.com/civilwargeeky/CEA_Wrap/issues/8
import CEA_Wrap as CEA
import numpy as np

def ThrustyBusty(FUEL_NAME, OXIDIZER_NAME, PROPELLANT_TANK_OUTER_DIAMETER, CONTRACTION_RATIO, OF_RATIO, CHAMBER_PRESSURE):
    
    cea_results = RunCEA(CHAMBER_PRESSURE, FUEL_NAME, OXIDIZER_NAME, OF_RATIO)
    expected_isp = CalculateExpectedISP(cea_results.isp)

    expected_exhaust_velocity = expected_isp * c.GRAVITY
    
    chamber_radius, chamber_length, throat_radius = CalculateEngineDimensions(PROPELLANT_TANK_OUTER_DIAMETER, FUEL_NAME, OXIDIZER_NAME, CONTRACTION_RATIO)
    total_mass_flow_rate = CalculateMassFlowRate(throat_radius, CHAMBER_PRESSURE, cea_results.c_mw, cea_results.c_gamma, cea_results.c_t)

    expected_thrust = CalculateExpectedThrust(expected_isp, total_mass_flow_rate)

    # return(expected_thrust, expected_isp, total_mass_flow_rate, chamber_radius, chamber_length, throat_radius)
    return(expected_thrust.item())


def RunCEA(
    chamber_pressure,
    fuel_name,
    oxidizer_name,
    OF_Ratio,
):
    # convert regular string for propellants to what CEA_wrap uses
    if fuel_name == "ethanol":
        CEA_fuel_name = CEA.Fuel("C2H5OH(L)", temp=c.T_AMBIENT)
    elif fuel_name == "kerosene":
        CEA_fuel_name = CEA.Fuel("Jet-A(L)", temp=c.T_AMBIENT)

    if oxidizer_name == "liquid oxygen":
        cea_oxidizer_name = CEA.Oxidizer("O2(L)", temp=90) # 90 K is temperature of oxidizer upon injection into combustion (same as copperhead's sizing)


    pressure_ratio = chamber_pressure / 10 # assume exit pressure is a constantly at the pressure of air a bit above sea level

    rocket = CEA.RocketProblem(
        pressure =       chamber_pressure,
        pip =            pressure_ratio, # pip is "Pressure ratio of chamber pressure to exit pressure." github.com/civilwargeeky/CEA_Wrap/blob/main/README.md#rocket-problem-constructor-additional-parameters
        materials =      [CEA_fuel_name, cea_oxidizer_name],
        o_f =            OF_Ratio,
        pressure_units = "psi",
    )

    cea_results = rocket.run()
    
    return(cea_results)

def CalculateExpectedThrust(expected_isp, total_mass_flow_rate):
    
    expected_jet_exhaust_velocity = expected_isp * c.GRAVITY
    expected_thrust = total_mass_flow_rate * expected_jet_exhaust_velocity
    
    return(expected_thrust)

def CalculateExpectedISP(ideal_isp):
    expected_c_star_efficiency = 0.9 # value used for CMS
    expected_nozzle_efficiency = 0.9 # value used for CMS
        
    expected_isp = ideal_isp * expected_c_star_efficiency * expected_nozzle_efficiency
    
    return(expected_isp)



# fixed :)
def CalculateMassFlowRate(throat_radius, chamber_pressure, chamber_molar_mass, chamber_gamma, T_c): # eq (1-19) on page 7 of sp-125 https://ntrs.nasa.gov/citations/19710019929
    y = chamber_gamma # for readability
    
    R = 8.314 / chamber_molar_mass # R is the specific gas constant here
    
    radicand = (y/(R*T_c)) * (( 2/(y+1) ) ** ((y+1) / (y-1)))
    
    throat_area = RadiusToArea(throat_radius)
    mass_flow_rate = throat_area * chamber_pressure * (radicand**0.5)
    return mass_flow_rate

def CalculateEngineDimensions(PROPELLANT_TANK_OUTER_DIAMETER, fuel_name, oxidizer_name, contraction_ratio):
    chamber_radius = (PROPELLANT_TANK_OUTER_DIAMETER/2) - 0.5 # lowkey a guess
    chamber_area = RadiusToArea(chamber_radius)
    
    throat_area = chamber_area/contraction_ratio
    throat_radius = AreaToRadius(throat_area)
    
    chamber_length = CalculateChamberLength(throat_area, chamber_area, fuel_name, oxidizer_name)
    return (chamber_radius, chamber_length, throat_radius)

def AreaToRadius(area):
    radius = (area/np.pi)**0.5
    return radius

def RadiusToArea(radius):
    area = np.pi*(radius**2)
    return area

def CalculateChamberLength(throat_area, chamber_area, fuel_name, oxidizer_name):
    L_star = FindLstar(fuel_name, oxidizer_name)
    chamber_length = (throat_area * L_star) / (chamber_area)
    return chamber_length

def FindLstar(fuel_name, oxidizer_name):
    if (oxidizer_name == "liquid oxygen"):
        if (fuel_name == "ethanol"):
            L_star = 45 * c.IN2M # source: from my asshole
        elif (fuel_name == "kerosene"):
            L_star = 45 * c.IN2M # table 4-1 on page 87 of nasa sp-125 https://ntrs.nasa.gov/citations/19710019929
        else:
            raise ValueError("No L* Found")
    else:
        raise ValueError("No L* Found")
        
    return L_star




if __name__ == "__main__":
    print(RunCEA(500, "ethanol", "liquid oxygen", 1.1).isp) # should be 255.433231397