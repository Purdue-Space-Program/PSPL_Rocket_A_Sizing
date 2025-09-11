
# import os
# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# import coding_utils.constants as c

from CoolProp.CoolProp import PropsSI

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


    best_case_tanks_too_big, worst_case_tanks_too_big = CalculateIfTanksTooBig(tank_pressure, oxidizer_total_tank_volume, fuel_total_tank_volume)
   
    return(total_usable_propellant_mass, engine_burn_time, oxidizer_tank_length, best_case_tanks_too_big, worst_case_tanks_too_big)


def CalculateIfTanksTooBig(tank_pressure, oxidizer_total_tank_volume, fuel_total_tank_volume):
     # COPV shit stolen from hugo
    
    # pressurant = "helium"
    pressurant = "nitrogen"
    
    if pressurant == "helium":
        gas_constant = c.HE_GAS_CONSTANT
    elif pressurant == "nitrogen":
        gas_constant = c.N2_GAS_CONSTANT

    # worst case from: https://docs.google.com/spreadsheets/d/1r7DucPdWUhxp2y30QmzvK9DFTFOnPvq5XJ1A3TCKh4o/edit?usp=sharing
    COPV_pressure = 4300 * c.PSI2PA
    COPV_volume = 3 * c.L2M3

    COPV_TEMP_1 = c.T_AMBIENT + 15  # [K] Assumed initial COPV pressurant temperature

    density_before_collapse = PropsSI("D", "P", COPV_pressure, "T", c.T_AMBIENT + 15, "nitrogen")
    density_after_collapse = PropsSI("D", "P", tank_pressure, "Q", 0, "nitrogen")

    worst_case_CFC_LOx = density_after_collapse/density_before_collapse # assuming all pressurant becomes a saturated vapor
    # print(worst_case_CFC_LOx)
    best_case_CFC_LOx = 1.75 # copperhead sizing for LOx-Helium collapse
    # best_case_CFC_LOx = 1 # copperhead sizing for LOx-Helium collapse
    
    CFC_FUEL = 1 # [1] Fuel tank cumulative collapse factor

    
    pressurantCv = PropsSI("CVMASS", "P", 1 * c.ATM2PA, "T", c.T_AMBIENT, pressurant)  # [J/kgK] Constant-volume specific heat of pressurant at STP (assumed constant)

    copvPressure1 = COPV_pressure  # [Pa] COPV initial pressure
    copvPressure2 = (c.BURNOUT_PRESSURE_RATIO * tank_pressure)  # [Pa] COPV burnout pressure

    copvEntropy1 = PropsSI("S", "P", copvPressure1, "T", COPV_TEMP_1, pressurant)  # [J/kgK] COPV initial specific entropy
    copvEntropy2 = copvEntropy1  # [J/kgK] COPV burnout specific entropy (assumed isentropic expansion)

    copvDensity1 = PropsSI("D", "P", copvPressure1, "T", COPV_TEMP_1, pressurant)  # [kg/m^3] COPV initial density
    copvDensity2 = PropsSI("D", "P", copvPressure2, "S", copvEntropy2, pressurant)  # [kg/m^3] COPV burnout density

    copvEnergy1 = PropsSI("U", "P", copvPressure1, "T", COPV_TEMP_1, pressurant)  # [J/kg] COPV initial specific energy
    copvEnergy2 = PropsSI("U", "P", copvPressure2, "S", copvEntropy2, pressurant)  # [J/kg] COPV burnout specific energy


    tank_volume_ratio =  oxidizer_total_tank_volume / fuel_total_tank_volume
    total_tanks_volume = fuel_total_tank_volume + oxidizer_total_tank_volume


    best_case_max_both_tank_volume = (
        ((copvDensity1 * COPV_volume * copvEnergy1) - (copvDensity2 * COPV_volume * copvEnergy2))
    / 
        (
        (best_case_CFC_LOx * tank_pressure * tank_volume_ratio * pressurantCv / gas_constant)
        + (best_case_CFC_LOx * tank_pressure * tank_volume_ratio)
        + (CFC_FUEL * tank_pressure * pressurantCv / gas_constant)
        + (CFC_FUEL * tank_pressure)
        )
    )
    
    worst_case_max_both_tank_volume = (
        ((copvDensity1 * COPV_volume * copvEnergy1) - (copvDensity2 * COPV_volume * copvEnergy2))
    / 
        (
        (worst_case_CFC_LOx * tank_pressure * tank_volume_ratio * pressurantCv / gas_constant)
        + (worst_case_CFC_LOx * tank_pressure * tank_volume_ratio)
        + (CFC_FUEL * tank_pressure * pressurantCv / gas_constant)
        + (CFC_FUEL * tank_pressure)
        )
    )
    
    worst_case_tanks_too_big = np.nan
    if total_tanks_volume > best_case_max_both_tank_volume:
        best_case_tanks_too_big = True
        worst_case_tanks_too_big = True
    elif (total_tanks_volume < best_case_max_both_tank_volume) and (total_tanks_volume > worst_case_max_both_tank_volume):
        best_case_tanks_too_big = False
        worst_case_tanks_too_big = True
    elif (total_tanks_volume < worst_case_max_both_tank_volume): 
        best_case_tanks_too_big = False
        worst_case_tanks_too_big = False
    else:
        raise ValueError("what")
    
    return (best_case_tanks_too_big, worst_case_tanks_too_big)



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