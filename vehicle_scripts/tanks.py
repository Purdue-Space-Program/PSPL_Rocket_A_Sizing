
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

    fuel_total_tank_volume = TankDimensionsToTotalTankVolume(PROPELLANT_TANK_INNER_DIAMETER, FUEL_TANK_LENGTH)

    # 0% of the tank volume is intentionally left empty for an initial ullage volume
    fuel_total_propellant_volume = fuel_total_tank_volume * 1
    fuel_total_propellant_mass = fuel_total_propellant_volume * fuel_density
    
    # 10% of the that propellant is assumed to be unused due to residuals 
    fuel_usable_propellant_volume = fuel_total_propellant_volume * 0.9

    fuel_usable_propellant_mass = fuel_usable_propellant_volume * fuel_density
    
    
    oxidizer_total_propellant_mass = fuel_total_propellant_mass * OF_RATIO
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
   
    return(total_usable_propellant_mass, engine_burn_time, oxidizer_tank_length, oxidizer_total_tank_volume, oxidizer_total_propellant_mass, fuel_total_tank_volume, fuel_total_propellant_mass, best_case_tanks_too_big, worst_case_tanks_too_big, tank_pressure)


def CalculateIfTanksTooBig(tank_pressure, oxidizer_total_tank_volume, fuel_total_tank_volume):
    
    collapse_method = "copperhead shit"

    # COPV: https://a.co/d/brRSB7G
    COPV_pressure_1 = 4500 * c.PSI2PA
    COPV_temp_1 = c.T_AMBIENT + 15
    COPV_volume = 4.7 * c.L2M3 

    # pressurant = "helium"
    pressurant = "nitrogen"
    
    if pressurant == "helium":
        gas_constant = c.HE_GAS_CONSTANT
    elif pressurant == "nitrogen":
        gas_constant = c.N2_GAS_CONSTANT
    
    
    worst_case_CFC_LOx = 3
    best_case_CFC_LOx = 1.75 # copperhead sizing for LOx-Helium collapse    
    CFC_FUEL = 1 # [1] Fuel tank cumulative collapse factor

    tank_volume_ratio =  oxidizer_total_tank_volume / fuel_total_tank_volume
    total_tanks_volume = fuel_total_tank_volume + oxidizer_total_tank_volume
    


    if collapse_method == "my dumb shit":
        # innocent until proven guilty 🦅🦅🦅🦅🛢️🛢️🛢️🛢️🗽🔔 
        best_case_tanks_too_big = False
        worst_case_tanks_too_big = False

        COPV_density_1 = PropsSI("D", "P", COPV_pressure_1, "T", COPV_temp_1, "nitrogen")
        # print(f"COPV_density_1: {COPV_density_1:.2f}")
        COPV_mass_1 = COPV_density_1 * COPV_volume
        # print(f"COPV_mass_1: {COPV_mass_1:.2f}")
        COPV_entropy_1 = PropsSI("S", "P", COPV_pressure_1, "T", COPV_temp_1, "nitrogen")
        # print(f"COPV_entropy_1: {COPV_entropy_1:.2f}")


        ox_tank_density = PropsSI("D", "P", tank_pressure, "Q", 1, "nitrogen")
        # print(f"ox_tank_density: {ox_tank_density:.2f}")
        ox_tank_mass = ox_tank_density * oxidizer_total_tank_volume
        # print(f"ox_tank_mass: {ox_tank_mass:.2f}")

        if (COPV_mass_1 - ox_tank_mass) <= 0.01: # adding small amount for  floating point bs!
            # raise ValueError("you ran out of pressurant :(")
            best_case_tanks_too_big = True
            worst_case_tanks_too_big = True
            return (best_case_tanks_too_big, worst_case_tanks_too_big)
            

        COPV_mass_2 = COPV_mass_1 - ox_tank_mass
        COPV_density_2 = COPV_mass_2 / COPV_volume
        COPV_entropy_2 = COPV_entropy_1 # isentropic expansion
        COPV_pressure_2 = PropsSI("P", "D", COPV_density_2, "S", COPV_entropy_2, "nitrogen")
        COPV_temp_2 = PropsSI("T", "D", COPV_density_2, "S", COPV_entropy_2, "nitrogen")
        # print(f"COPV_pressure_2: {COPV_pressure_2:.2f}")
        # print(f"COPV_temp_2: {COPV_temp_2 - 273.15:.2f}")

        # COPV_temp_3 = 0 # initial value to start the while loop that is certainly below the copv real temp
        # fuel_tank_temp_guess = COPV_temp_2 # initial guess that is certainly above the real fuel temp
        # fuel_tank_temp_actual = 0 # the temperature the nitrogen in fuel tank would be if the initial guess is true
        
        
        fuel_tank_mass_guess = 0.0001 # initial guess that is less than the real fuel mass
        
        while fuel_tank_mass_guess < fuel_tank_temp_actual:
        
            fuel_tank_density = fuel_tank_mass_guess / fuel_total_tank_volume
            fuel_tank_enthalpy = PropsSI("H", "P", tank_pressure, "D", fuel_tank_density, "nitrogen")
            
            if (COPV_mass_2 - (fuel_tank_mass)) <= 0.01:  # check if under a small amount (instead of zero) for  floating point bs!
                # raise ValueError("you ran out of pressurant :(")
                best_case_tanks_too_big = True
                worst_case_tanks_too_big = True
                return (best_case_tanks_too_big, worst_case_tanks_too_big)
            else:
                COPV_mass_3 = COPV_mass_2 - fuel_tank_mass
        
            

            COPV_density_3 = COPV_mass_3 / COPV_volume
            COPV_entropy_3 = COPV_entropy_2 # isentropic expansion
            COPV_pressure_3 = PropsSI("P", "D", COPV_density_3, "S", COPV_entropy_3, "nitrogen")
        
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        # WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK WHAT THE FUCK
        
        
        
        
        
        
        
        
        
            fuel_tank_density = PropsSI("D", "P", tank_pressure, "T", fuel_tank_temp_guess, "nitrogen")
            # print(f"fuel_tank_density: {fuel_tank_density:.2f}")
            fuel_tank_mass = fuel_tank_density * fuel_total_tank_volume
            # print(f"fuel_tank_mass: {fuel_tank_mass:.2f}")
            # print(f"\nCOPV_temp_3: {COPV_temp_3:.2f}")
            # print(f"fuel_tank_temp: {fuel_tank_temp_guess:.2f}")
            
            if (COPV_mass_2 - (fuel_tank_mass)) <= 0.01:  # check if under a small amount (instead of zero) for  floating point bs!
                # raise ValueError("you ran out of pressurant :(")
                best_case_tanks_too_big = True
                worst_case_tanks_too_big = True
                return (best_case_tanks_too_big, worst_case_tanks_too_big)
            
            COPV_mass_3 = COPV_mass_2 - fuel_tank_mass
            # print(f"COPV_mass_3: {COPV_mass_3:.2f}")
            COPV_density_3 = COPV_mass_3 / COPV_volume
            COPV_entropy_3 = COPV_entropy_2 # isentropic expansion
            COPV_pressure_3 = PropsSI("P", "D", COPV_density_3, "S", COPV_entropy_3, "nitrogen")

            fuel_tank_temp_actual = PropsSI("T", "P", tank_pressure, "S", COPV_entropy_3, "nitrogen") # isentropic expansion of nitrogen in COPV to be in fuel tank

            fuel_tank_temp_guess -= 4
            if fuel_tank_temp_guess < 63: # nitrogen freezing point
                raise ValueError

            fuel_tank_temp_real = fuel_tank_temp_guess

            if (COPV_pressure_3 * 2) < tank_pressure:
                # raise ValueError("you ran out of pressurant :(")
                best_case_tanks_too_big = True
                worst_case_tanks_too_big = True
                return (best_case_tanks_too_big, worst_case_tanks_too_big)

    
    
    
    elif collapse_method == "copperhead shit modified":
        
        # COPV shit stolen from hugo
        

        # worst case from: https://docs.google.com/spreadsheets/d/1r7DucPdWUhxp2y30QmzvK9DFTFOnPvq5XJ1A3TCKh4o/edit?usp=sharing


        pressurant_in_COPV_density = PropsSI("D", "P", COPV_pressure_1, "T", COPV_temp_1, "nitrogen")
        pressurant_in_COPV_entropy = PropsSI("S", "P", COPV_pressure_1, "T", COPV_temp_1, "nitrogen")
        pressurant_in_fuel_tank_entropy = pressurant_in_COPV_entropy

        pressurant_in_ox_density = PropsSI("D", "P", tank_pressure, "Q", 1, "nitrogen")
        pressurant_in_fuel_density = PropsSI("D", "P", tank_pressure, "S", pressurant_in_fuel_tank_entropy, "nitrogen")

        pressurant_in_ox_tank_before_collapse_density = PropsSI("D", "P", tank_pressure, "S", pressurant_in_fuel_tank_entropy, "nitrogen")
        pressurant_in_ox_tank_after_collapse_density = PropsSI("D", "P", tank_pressure, "Q", 1, "nitrogen")


        pressurant_in_COPV_to_in_ox_density_ratio = pressurant_in_COPV_density/pressurant_in_ox_density
        pressurant_in_COPV_to_in_fuel_density_ratio = pressurant_in_COPV_density/pressurant_in_fuel_density

        # print(f"pressurant_in_COPV_to_in_ox_density_ratio: {pressurant_in_COPV_to_in_ox_density_ratio:.2f}")
        # print(f"pressurant_in_COPV_to_in_fuel_density_ratio: {pressurant_in_COPV_to_in_fuel_density_ratio:.2f}")

        needed_COPV_volume_for_ox =  (oxidizer_total_tank_volume + (COPV_volume * 2))/pressurant_in_COPV_to_in_ox_density_ratio
        needed_COPV_volume_for_fuel =  (fuel_total_tank_volume + (COPV_volume * 2))/pressurant_in_COPV_to_in_fuel_density_ratio

        needed_COPV_volume = needed_COPV_volume_for_ox + needed_COPV_volume_for_fuel

        # print(f"need_copv_volume: {needed_COPV_volume * c.M32L:.2f}")
            
        
        
        if needed_COPV_volume > COPV_volume:
            best_case_tanks_too_big = True
            worst_case_tanks_too_big = True
        elif needed_COPV_volume < COPV_volume:
            best_case_tanks_too_big = False
            worst_case_tanks_too_big = False

        else:
            raise ValueError("what")
        
    
    elif collapse_method == "copperhead shit":
        pressurantCv = PropsSI("CVMASS", "P", 1 * c.ATM2PA, "T", c.T_AMBIENT, pressurant)  # [J/kgK] Constant-volume specific heat of pressurant at STP (assumed constant)

        copvPressure2 = (c.BURNOUT_PRESSURE_RATIO * tank_pressure)  # [Pa] COPV burnout pressure

        copvEntropy1 = PropsSI("S", "P", COPV_pressure_1, "T", COPV_temp_1, pressurant)  # [J/kgK] COPV initial specific entropy
        copvEntropy2 = copvEntropy1  # [J/kgK] COPV burnout specific entropy (assumed isentropic expansion)

        copvDensity1 = PropsSI("D", "P", COPV_pressure_1, "T", COPV_temp_1, pressurant)  # [kg/m^3] COPV initial density
        copvDensity2 = PropsSI("D", "P", copvPressure2, "S", copvEntropy2, pressurant)  # [kg/m^3] COPV burnout density

        copvEnergy1 = PropsSI("U", "P", COPV_pressure_1, "T", COPV_temp_1, pressurant)  # [J/kg] COPV initial specific energy
        copvEnergy2 = PropsSI("U", "P", copvPressure2, "S", copvEntropy2, pressurant)  # [J/kg] COPV burnout specific energy

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
    
    else:
        raise ValueError("choose some dumb shit")
    
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