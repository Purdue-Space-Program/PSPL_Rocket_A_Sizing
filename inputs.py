import coding_utils.constants as c
import numpy as np

step_size = 10 # number of values to use for each variable input

# A dictionary used to define the possible definitions where each key is an input (constant or variable)
# and each value is either the constant value or a range of values

# rocket_definition_inputs_scope = {

# MAXIMUM OF 40 STEPS (variable_inputs_using_step_size * step_size) OR YOUR COMPUTER WILL CRASH !!!!!!!!
variable_inputs = {
    "FUEL_NAME":                  ["Ethanol", "Kerosene"],

    "CONTRACTION_RATIO":          np.linspace(3, 6, step_size), # area ratio of chamber to throat (3 to 6 recommended by textbook)
    "OF_RATIO":                   np.linspace(2, 3, step_size), # ratio of oxygen to fuel by mass

    # "OXIDIZER_ON_TOP_FUEL_ON_BOTTOM": [True, False], # [boolean (true or false)] whether the oxidizer tank is above the fuel tank or not
    # "FUEL_TANK_LENGTH":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # [meters] possible speedy metals pipe lengths: speedymetals.com/pc-4624-8371-4-12-od-x-125-wall-tube-6061-t6-aluminum.aspx
    # "a":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # testing
    # "b":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # testing
    # "c":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # testing
    # "d":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # testing
    # "e":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # testing
    # "f":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # testing
    # "g":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # testing
}

constant_inputs = {

    "OXIDIZER_NAME":                           "Liquid Oxygen",
    "OXIDIZER_TEMPERATURE":                     80, # [kelvin] probably something else in reality but good enough for now: wikipedia.org/wiki/Liquid_oxygen

    "PROPELLANT_TANK_OUTER_DIAMETER":           4.50  * c.IN2M, # [meters] from speedy metals pipe (link above)
    # "PROPELLANT_TANK_INNER_DIAMETER":         4.25  * c.IN2M, # [meters] from speedy metals pipe (link above)
    # "PROPELLANT_TANK_THICKNESS":              0.125 * c.IN2M,   # [meters] from speedy metals pipe (link above)

    # "ALUMINUM_ENGINE_COVER_OUTER_DIAMETER":   4.5   * c.IN2M, # [meters] from speedy metals pipe (link above)
    # "ALUMINUM_ENGINE_COVER_INNER_DIAMETER":   4.25  * c.IN2M, # [meters] from speedy metals pipe (link above)
    # "ALUMINUM_ENGINE_COVER_THICKNESS":        0.125 * c.IN2M, # [meters] from speedy metals pipe (link above)
    # "GRAPHITE_CHAMBER_OUTER_DIAMETER":        4.25  * c.IN2M, # [meters] the same diameter as "ALUMINUM_ENGINE_COVER_INNER_DIAMETER" since they're touching
    # "GRAPHITE_CHAMBER_INNER_DIAMETER":        4.00  * c.IN2M, # [meters] this will be the diameter of the volume where combustion occurs
    # "GRAPHITE_CHAMBER_THICKNESS":             0.125 * c.IN2M, # [meters]
}


if __name__ == "__main__":
    pass