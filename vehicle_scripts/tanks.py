from inputs import USE_FAKE_TANKS_DATA


# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# import coding_utils.constants as c


if USE_FAKE_TANKS_DATA == False:
    from CoolProp.CoolProp import PropsSI
# else:
#     from coding_utils.constants import PropsSI

import coding_utils.constants as c
import numpy as np



def GoFluids(PROPELLANT_TANK_INNER_DIAMETER, 
             FUEL_TANK_LENGTH, 
             CHAMBER_PRESSURE,  
             OXIDIZER_NAME, 
             FUEL_NAME, 
             OF_RATIO, 
             total_mass_flow_rate):
    
    tank_pressure = CalculateTankPressure(CHAMBER_PRESSURE)
    
    fuel_density = FindPropellantDensity(FUEL_NAME, tank_pressure)
    oxidizer_density = FindPropellantDensity(OXIDIZER_NAME, tank_pressure)
    # print(f"fuel_density: {fuel_density}")
    # print(f"oxidizer_density: {oxidizer_density}")
    
    fuel_total_tank_volume = TankDimensionsToTotalTankVolume(PROPELLANT_TANK_INNER_DIAMETER, FUEL_TANK_LENGTH)

    # 0% of the tank volume is intentionally left empty for an initial ullage volume
    fuel_total_propellant_volume = fuel_total_tank_volume * 1
    
    # 10% of the that propellant is assumed to be unused due to residuals 
    fuel_usable_propellant_volume = fuel_total_propellant_volume * 0.9

    fuel_usable_propellant_mass = fuel_usable_propellant_volume * fuel_density
    
    
    oxidizer_usable_propellant_mass = fuel_usable_propellant_mass * OF_RATIO
    
    oxidizer_usable_propellant_volume = oxidizer_usable_propellant_mass / oxidizer_density
    
    # 10% of the that propellant is assumed to be unused due to residuals 
    oxidizer_total_propellant_volume = oxidizer_usable_propellant_volume / 0.9
    
    # 10% of the tank volume is intentionally left empty for an initial ullage volume 
    oxidizer_total_tank_volume = oxidizer_total_propellant_volume / 0.9

    oxidizer_tank_length = TotalTankVolumeToTankDimensions(PROPELLANT_TANK_INNER_DIAMETER, oxidizer_total_tank_volume)

    # useful shit
    total_usable_propellant_mass = fuel_usable_propellant_mass + oxidizer_usable_propellant_mass
    engine_burn_time = total_usable_propellant_mass / total_mass_flow_rate
    # print(f"engine_burn_time: {engine_burn_time},  total_usable_propellant_mass: {total_usable_propellant_mass}, total_mass_flow_rate: {total_mass_flow_rate}")



    # COPV shit stolen from hugo
    
    # worst case from: https://docs.google.com/spreadsheets/d/1r7DucPdWUhxp2y30QmzvK9DFTFOnPvq5XJ1A3TCKh4o/edit?usp=sharing
    copv_pressure = 4300 * c.PSI2PA
    copv_volume = 1.6 * c.L2M3
    
    COPV_TEMP_1 = c.T_AMBIENT + 15  # [K] Assumed initial COPV pressurant temperature

    CFC_OX = 3 # [1] Oxidizer tank cumulative collapse factor
    CFC_FUEL = 1 # [1] Fuel tank cumulative collapse factor

    # pressurant = "helium"
    pressurant = "nitrogen"
    
    if pressurant == "helium":
        gas_constant = c.HE_GAS_CONSTANT
    elif pressurant == "nitrogen":
        gas_constant = c.N2_GAS_CONSTANT
    
    pressurantCv = PropsSI("CVMASS", "P", 1 * c.ATM2PA, "T", c.T_AMBIENT, pressurant)  # [J/kgK] Constant-volume specific heat of pressurant at STP (assumed constant)

    copvPressure1 = copv_pressure  # [Pa] COPV initial pressure
    copvPressure2 = (
        c.BURNOUT_PRESSURE_RATIO * tank_pressure
    )  # [Pa] COPV burnout pressure

    copvEntropy1 = PropsSI(
        "S", "P", copvPressure1, "T", COPV_TEMP_1, pressurant
    )  # [J/kgK] COPV initial specific entropy
    copvEntropy2 = copvEntropy1  # [J/kgK] COPV burnout specific entropy (assumed isentropic expansion)

    copvDensity1 = PropsSI(
        "D", "P", copvPressure1, "T", COPV_TEMP_1, pressurant
    )  # [kg/m^3] COPV initial density
    copvDensity2 = PropsSI(
        "D", "P", copvPressure2, "S", copvEntropy2, pressurant
    )  # [kg/m^3] COPV burnout density

    copvEnergy1 = PropsSI(
        "U", "P", copvPressure1, "T", COPV_TEMP_1, pressurant
    )  # [J/kg] COPV initial specific energy
    copvEnergy2 = PropsSI(
        "U", "P", copvPressure2, "S", copvEntropy2, pressurant
    )  # [J/kg] COPV burnout specific energy


    tank_volume_ratio =  oxidizer_total_tank_volume / fuel_total_tank_volume


    max_fuel_tank_volume = (
        ((copvDensity1 * copv_volume * copvEnergy1) - (copvDensity2 * copv_volume * copvEnergy2))
    / 
        (
        (CFC_OX * tank_pressure * tank_volume_ratio * pressurantCv / gas_constant)
        + (CFC_OX * tank_pressure * tank_volume_ratio)
        + (CFC_FUEL * tank_pressure * pressurantCv / gas_constant)
        + (CFC_FUEL * tank_pressure)
        )
    )
    
    if fuel_total_tank_volume > max_fuel_tank_volume:
        tanks_too_big = True
    else:
        tanks_too_big = False

    return(total_usable_propellant_mass, engine_burn_time, oxidizer_tank_length, tanks_too_big)


def CalculateTankPressure(CHAMBER_PRESSURE):
    # assume engine pressure to chamber pressure ratio is 60% based off old rockets https://purdue-space-program.atlassian.net/wiki/x/koFOLg 
    
    # CHAMBER_PRESSURE / tank_pressure = 0.6
    tank_pressure = CHAMBER_PRESSURE / 0.6

    return tank_pressure

def TankDimensionsToTotalTankVolume(tank_inner_diameter, tank_length):
    total_volume = np.pi * ((tank_inner_diameter/2)**2) * tank_length
    return total_volume

def TotalTankVolumeToTankDimensions(tank_inner_diameter, total_tank_volume):
    
    tank_length = total_tank_volume / (np.pi * ((tank_inner_diameter/2)**2))
    
    return tank_length

def FindPropellantDensity(propellant_name, tank_pressure):    
    if propellant_name == "ethanol":
        propellant_density = PropsSI('D', 'P', tank_pressure, 'T', c.T_AMBIENT, "Ethanol")
    elif propellant_name == "kerosene":
        propellant_density = PropsSI('D', 'P', tank_pressure, 'T', c.T_AMBIENT, "n-Dodecane")
    elif propellant_name == "ipa":
        # propellant_density = PropsSI('D', 'P', tank_pressure, 'T', c.T_AMBIENT, "Isopropanol")
        propellant_density = 786 # No support for IPA in CoolProp :(
    elif propellant_name == "liquid oxygen":
        propellant_density = PropsSI('D', 'P', tank_pressure, 'T', 90, "Oxygen") # 90 K is temperature of oxidizer upon injection into combustion (same as copperhead's sizing)
    else:
        raise ValueError("No Density Found")

    return (propellant_density)