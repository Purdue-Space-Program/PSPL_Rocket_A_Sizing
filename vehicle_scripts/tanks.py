from CoolProp.CoolProp import PropsSI
import coding_utils.constants as c
import numpy as np



def GoFluids(PROPELLANT_TANK_INNER_DIAMETER, FUEL_TANK_LENGTH, tank_pressure, OXIDIZER_NAME, FUEL_NAME):
    
    total_tank_volume = TankDimensionsToTankVolumeToUsableVolume(PROPELLANT_TANK_INNER_DIAMETER, FUEL_TANK_LENGTH)
    
    # 10% of the tank volume is intentionally left empty  
    propellant_volume = total_tank_volume * 0.9
    
    # 10% of the that propellant is assumed to be unused due to residuals 
    usable_propellant_volume = propellant_volume * 0.9
    

    if FUEL_NAME == "ethanol":
        fuel_density = PropsSI('H', 'P', tank_pressure, 'T', c.T_AMBIENT, "Ethanol")
    elif FUEL_NAME == "kerosene":
        fuel_density = PropsSI('H', 'P', tank_pressure, 'T', c.T_AMBIENT, "Kerosene")

    if OXIDIZER_NAME == "liquid oxygen":
        fuel_density = PropsSI('H', 'P', tank_pressure, 'T', 90, "Oxygen") # 90 K is temperature of oxidizer upon injection into combustion (same as copperhead's sizing)

    
    
    return(total_tank_volume, propellant_volume, usable_propellant_volume)


def TankDimensionsToTankVolumeToUsableVolume(tank_inner_diameter, tank_length):
    total_volume = np.pi * ((tank_inner_diameter/2)**2) * tank_length
    return total_volume



