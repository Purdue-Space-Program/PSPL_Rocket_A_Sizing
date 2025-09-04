# from CoolProp.CoolProp import PropsSI
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
    oxidizer_total_tank_volume = oxidizer_total_propellant_volume /  0.9

    oxidizer_tank_length = TotalTankVolumeToTankDimensions(PROPELLANT_TANK_INNER_DIAMETER, oxidizer_total_tank_volume)

    # useful shit
    total_usable_propellant_mass = fuel_usable_propellant_mass + oxidizer_usable_propellant_mass
    engine_burn_time = total_usable_propellant_mass / total_mass_flow_rate
    # print(f"engine_burn_time: {engine_burn_time},  total_usable_propellant_mass: {total_usable_propellant_mass}, total_mass_flow_rate: {total_mass_flow_rate}")

    return(total_usable_propellant_mass, engine_burn_time, oxidizer_tank_length)


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
        propellant_density = PropsSI('D', 'P', tank_pressure, 'T', c.T_AMBIENT, "Kerosene")
    elif propellant_name == "liquid oxygen":
        propellant_density = PropsSI('D', 'P', tank_pressure, 'T', 90, "Oxygen") # 90 K is temperature of oxidizer upon injection into combustion (same as copperhead's sizing)
    else:
        raise ValueError("No Density Found")

    return (propellant_density)