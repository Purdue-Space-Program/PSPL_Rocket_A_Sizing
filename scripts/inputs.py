import coding_utils.constants as c


#### CHANGING INPUTS ####

FUEL_NAME = "Ethanol"
FUEL_TEMPERATUE = 270 # [kelvin] a brisk cold day in west lafayette, indiana




#### CONSTANT INPUTS ####

OXIDIZER_NAME = "Liquid Oxygen"
OXIDIZER_TEMPERATURE = 80 # [kelvin] probably someting else in reality but good enough: https://en.wikipedia.org/wiki/Liquid_oxygen

TANK_OUTER_DIAMETER = 4.5 * c.IN2M # [meters] from speedy metals pipe: https://www.speedymetals.com/pc-4624-8371-4-12-od-x-125-wall-tube-6061-t6-aluminum.aspx
CHAMBER_ALLUMINUM_OUTER_DIAMETER = 4.5 * c.IN2M # [meters] from speedy metals pipe: https://www.speedymetals
CHAMBER_ALLUMINUM_INNER_DIAMETER = 4.25 * c.IN2M # [meters] from speedy metals pipe: https://www.speedymetals
CHAMBER_GRAPHITE_OUTER_DIAMETER = CHAMBER_ALLUMINUM_INNER_DIAMETER # [meters]
CHAMBER_GRAPHITE_INNER_DIAMETER = 4 * c.IN2M # [meters]
