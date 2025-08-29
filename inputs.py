import coding_utils.constants as c
import numpy as np

step_size = 30 # number of values to use for each variable input

# A dictionary used to define the possible definitions where each key is an input (constant or variable)
# and each value is either the constant value or a range of values

# rocket_definition_inputs_scope = {

variable_inputs = {
    # "FUEL_NAME":                  ["Ethanol", "Kerosene"],

    # "CONTRACTION_RATIO":          np.linspace(3, 6, step_size), # [dimensionless] area ratio of chamber to throat (3 to 6 recommended by textbook)
    "OF_RATIO":                   np.linspace(0.1, 5, step_size), # [dimensionless] ratio of oxygen to fuel by mass

    "CHAMBER_PRESSURE":           np.linspace(40, 1000, step_size), # [psi] pressure in the chamber during combustion
    
    # "OXIDIZER_ON_TOP_FUEL_ON_BOTTOM": [True, False], # [boolean (true or false)] whether the oxidizer tank is above the fuel tank or not
    # "FUEL_TANK_LENGTH":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # [meters] possible speedy metals pipe lengths: speedymetals.com/changethelinkbro
    
    # "a":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # stress testing
    # "b":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # stress testing
    # "c":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # stress testing
    # "d":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # stress testing
    # "e":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # stress testing
    # "f":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # stress testing
    # "g":   np.linspace(6 * c.IN2M, 288 * c.IN2M, step_size), # stress testing
}

constant_inputs = {
    # "CHAMBER_PRESSURE":                         200, # [psi] pressure in the chamber during combustion
    
    "CONTRACTION_RATIO":                        4, # [dimensionless] area ratio of chamber to throat (3 to 6 recommended by textbook)
    "FUEL_NAME":                                "Ethanol",
    # "FUEL_NAME":                                "Kerosene",
    
    "OXIDIZER_NAME":                            "Liquid Oxygen",

    "PROPELLANT_TANK_OUTER_DIAMETER":           6 * c.IN2M, # [meters] from speedy metals pipe (link above)
    "PROPELLANT_TANK_THICKNESS":              0.125 * c.IN2M,   # [meters] from speedy metals pipe (link above)
    # "PROPELLANT_TANK_INNER_DIAMETER":         5.75  * c.IN2M, # [meters] from speedy metals pipe (link above)

    # "ALUMINUM_ENGINE_COVER_OUTER_DIAMETER":   4.5   * c.IN2M, # [meters] from speedy metals pipe (link above)
    # "ALUMINUM_ENGINE_COVER_INNER_DIAMETER":   4.25  * c.IN2M, # [meters] from speedy metals pipe (link above)
    # "ALUMINUM_ENGINE_COVER_THICKNESS":        0.125 * c.IN2M, # [meters] from speedy metals pipe (link above)
    # "GRAPHITE_CHAMBER_OUTER_DIAMETER":        4.25  * c.IN2M, # [meters] the same diameter as "ALUMINUM_ENGINE_COVER_INNER_DIAMETER" since they're touching
    # "GRAPHITE_CHAMBER_INNER_DIAMETER":        4.00  * c.IN2M, # [meters] this will be the diameter of the volume where combustion occurs
    # "GRAPHITE_CHAMBER_THICKNESS":             0.125 * c.IN2M, # [meters]
}

constant_inputs["PROPELLANT_TANK_INNER_DIAMETER"] = constant_inputs["PROPELLANT_TANK_OUTER_DIAMETER"] - (2 * constant_inputs["PROPELLANT_TANK_THICKNESS"])



if __name__ == "__main__":
    pass