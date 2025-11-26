# This code reflects the vehicle parameters as stated on the vehicle parameters page: https://purdue-space-program.atlassian.net/wiki/x/Aw5qYw
# Import this file into your script as a way to easily and reliably pull parameters. 
# Author: David Gustafsson

from dataclasses import dataclass, fields
from typing import Iterator
import coding_utils.constants as c
import matplotlib.pyplot as plt
import numpy as np

def calculate_mass(fuel_tank_length, 
                   oxidizer_tank_length, 
                   propellant_tank_outer_diameter, 
                   propellant_tank_inner_diameter, 
                   fuel_total_propellant_mass, 
                   oxidizer_total_propellant_mass,
                   ):


    def CalcCylinderVolume(diameter, length):
        radius = diameter/2
        volume = 3.14159265358979 * (radius**2) * length # off the dome!
        return volume

    def CalcTubeVolume(OD, ID, length):
        volume = CalcCylinderVolume(OD, length) - CalcCylinderVolume(ID, length)
        return volume

    engine_length = 1 * c.FT2M
    injector_length = 2 * c.IN2M
    lower_length = 1 * c.FT2M

    bulkhead_length = 3 * c.IN2M

    upper_length = 0.5 * c.FT2M
    helium_bay_length = 20 * c.IN2M

    avionics_bay_length = 0.25 * c.FT2M
    recovery_bay_length = 0.5 * c.FT2M
    nosecone_length = 1 * c.FT2M

    panels_outer_diameter = propellant_tank_outer_diameter
    panels_inner_diameter = propellant_tank_inner_diameter

    engine_wall_thickness = 0.25 * c.IN2M
    engine_OD = propellant_tank_outer_diameter
    engine_ID = engine_OD - (2 * engine_wall_thickness)
    engine_mass = c.DENSITY_SS316 * CalcTubeVolume(engine_OD, engine_ID, engine_length)
    # print(f"engine_mass: {engine_mass * c.KG2LB} [lbm]")

    injector_mass = c.DENSITY_SS316 * CalcCylinderVolume(propellant_tank_outer_diameter, injector_length)

    valves_mass = 2 * 3.26 * c.LB2KG # fuel and ox 3/4 inch valve https://habonim.com/wp-content/uploads/2020/08/C47-BD_C47__2023_VO4_28-06-23.pdf
    lower_panels_mass = c.DENSITY_AL * CalcTubeVolume(panels_outer_diameter, panels_inner_diameter, lower_length)
    lower_mass = valves_mass + lower_panels_mass

    bulkhead_wall_thickness = 0.25 * c.IN2M
    bulkhead_top_thickness = 0.76 * c.IN2M

    bulkhead_mass =  c.DENSITY_AL * (
        (CalcCylinderVolume(propellant_tank_outer_diameter, bulkhead_length) - 
        CalcCylinderVolume(propellant_tank_outer_diameter - (2 * bulkhead_wall_thickness), bulkhead_length - bulkhead_top_thickness))
    )

    fuel_tank_wall_mass = c.DENSITY_AL * CalcTubeVolume(propellant_tank_outer_diameter, propellant_tank_inner_diameter, fuel_tank_length)
    fuel_tank_wet_mass = fuel_tank_wall_mass + fuel_total_propellant_mass
    oxidizer_tank_wall_mass = c.DENSITY_AL * CalcTubeVolume(propellant_tank_outer_diameter, propellant_tank_inner_diameter, oxidizer_tank_length)
    oxidizer_tank_wet_mass = oxidizer_tank_wall_mass + oxidizer_total_propellant_mass

    regulator_mass = 1.200 # regulator https://valvesandregulators.aquaenvironment.com/item/high-flow-reducing-regulators-2/873-d-high-flow-dome-loaded-reducing-regulators/item-1659
    upper_panels_mass = c.DENSITY_AL * CalcTubeVolume(panels_outer_diameter, panels_inner_diameter, upper_length)
    upper_mass = regulator_mass + upper_panels_mass

    copv_mass = 2.9 
    helium_bay_panels_mass = c.DENSITY_AL * CalcTubeVolume(panels_outer_diameter, panels_inner_diameter, helium_bay_length)
    helium_bay_mass = copv_mass + helium_bay_panels_mass

    avionics_bay_panels_mass = c.DENSITY_AL * CalcTubeVolume(panels_outer_diameter, panels_inner_diameter, avionics_bay_length)
    avionics_bay_mass = avionics_bay_panels_mass + (1 * c.LB2KG) # avionics doesn't weigh anything...

    recovery_bay_panels_mass = c.DENSITY_AL * CalcTubeVolume(panels_outer_diameter, panels_inner_diameter, recovery_bay_length)
    parachute_mass = 8 * c.LB2KG  # [kg] 1/3 cuz 1/3 of dry mass compared to --> https://github.com/Purdue-Space-Program/PSPL_Rocket_4_Sizing/blob/2b15e1dc508a56731056ff594a3c6b5afb639b4c/scripts/structures.py#L75
    recovery_bay_mass = recovery_bay_panels_mass + parachute_mass

    nose_cone_mass = c.DENSITY_AL * CalcTubeVolume(panels_outer_diameter, panels_inner_diameter, nosecone_length) # guess



    structures = 15 * c.LB2KG # structures !
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures
    structures



    @dataclass(frozen=True)
    class MassComponent:
        name : str                # name of the component [string]
        mass: float               # [kilograms]
        bottom_distance_from_aft: float   # distance from the bottom of the rocket to the bottom of the mass component [meters]
        length: float              # [meters]
        
        def StartAfter(self): # A mass object that directly after another
            return(self.bottom_distance_from_aft + self.length)

    @dataclass(frozen=True)
    class MassDistribution:
        components: list[MassComponent]

        def __iter__(self):
            return iter(self.components)

        # def __iter__(self) -> Iterator[MassComponent]:
        #     """Automatically iterate over all MassComponent attributes."""
        #     for f in fields(self):
        #         yield getattr(self, f.name)


    engine =                  MassComponent(name = 'engine',                      mass = engine_mass,            bottom_distance_from_aft = 0,                                                length = engine_length)
    injector =                MassComponent(name = 'injector',                    mass = injector_mass,          bottom_distance_from_aft = engine.StartAfter(),                              length = injector_length)
    lower =                   MassComponent(name = 'lower',                       mass = lower_mass,             bottom_distance_from_aft = injector.StartAfter(),                            length = lower_length)

    lower_fuel_bulkhead =     MassComponent(name = 'lower_fuel_bulkhead',         mass = bulkhead_mass,          bottom_distance_from_aft = lower.StartAfter(),                               length = bulkhead_length)
    fuel_tank =               MassComponent(name = 'fuel_tank',                   mass = fuel_tank_wet_mass,     bottom_distance_from_aft = lower_fuel_bulkhead.StartAfter(),                 length = fuel_tank_length)
    upper_fuel_bulkhead =     MassComponent(name = 'upper_fuel_bulkhead',         mass = bulkhead_mass,          bottom_distance_from_aft = fuel_tank.StartAfter() - (bulkhead_length),       length = bulkhead_length)

    lower_oxidizer_bulkhead = MassComponent(name = 'lower_oxidizer_bulkhead',     mass = bulkhead_mass,          bottom_distance_from_aft = upper_fuel_bulkhead.StartAfter(),                 length = bulkhead_length)
    oxidizer_tank =           MassComponent(name = 'oxidizer_tank',               mass = oxidizer_tank_wet_mass, bottom_distance_from_aft = lower_oxidizer_bulkhead.StartAfter(),             length = oxidizer_tank_length)
    upper_oxidizer_bulkhead = MassComponent(name = 'upper_oxidizer_bulkhead',     mass = bulkhead_mass,          bottom_distance_from_aft = oxidizer_tank.StartAfter() - (bulkhead_length),   length = bulkhead_length)

    upper =                   MassComponent(name = 'upper',                       mass = upper_mass,             bottom_distance_from_aft = upper_oxidizer_bulkhead.StartAfter(),             length = upper_length)
    helium_bay =              MassComponent(name = 'helium_bay',                  mass = helium_bay_mass,        bottom_distance_from_aft = upper.StartAfter(),                               length = helium_bay_length)
    avionics_bay =            MassComponent(name = 'avionics_bay',                mass = avionics_bay_mass,      bottom_distance_from_aft = helium_bay.StartAfter(),                          length = avionics_bay_length)
    recovery_bay =            MassComponent(name = 'recovery_bay',                mass = recovery_bay_mass,      bottom_distance_from_aft = avionics_bay.StartAfter(),                        length = recovery_bay_length)

    nosecone =                MassComponent(name = 'nosecone',                    mass = nose_cone_mass,         bottom_distance_from_aft = recovery_bay.StartAfter(),                        length=nosecone_length)


    mass_distribution = MassDistribution(components=
        [
        engine,
        injector,
        lower,
        
        lower_fuel_bulkhead,
        fuel_tank,
        upper_fuel_bulkhead,
        
        lower_oxidizer_bulkhead,
        oxidizer_tank,
        upper_oxidizer_bulkhead,
        
        upper,
        helium_bay,
        
        avionics_bay,
        recovery_bay,
        nosecone,
        ]
    )



    num_points = 500
    length_along_rocket_linspace = np.linspace(mass_distribution.components[0].bottom_distance_from_aft, mass_distribution.components[-1].StartAfter(), num_points)

    # x = np.linspace(0, nosecone.StartAfter(), num_points_per_component * np.size(mass_distribution))
    # y = np.zeros(num_points_per_component * len(mass_distribution))

    linear_density_array = np.zeros(num_points)

    for component in mass_distribution.components:
        
        linear_density = (component.mass / component.length) # The average mass in the length of the component
        
        for index, length_along_rocket in enumerate(length_along_rocket_linspace):
            above_component_bottom = length_along_rocket >= component.bottom_distance_from_aft
            below_component_top = length_along_rocket <= (component.bottom_distance_from_aft + component.length)
            
            if (above_component_bottom and below_component_top):
                linear_density_array[index] += linear_density

    panels_mass = lower_panels_mass + upper_panels_mass + helium_bay_panels_mass + avionics_bay_panels_mass + recovery_bay_panels_mass

        
        # component_range = np.linspace(component.bottom_distance_from_aft, component.bottom_distance_from_aft + component.length, num_points_per_component, endpoint=False)
        
        # for point in component_range:
        #     point_nearest = 999999999999999999999
        #     for potential_nearest_point in x:
        #         if (abs(potential_nearest_point - point) < point_nearest):
        #             point_nearest = potential_nearest_point
                
        #         if (x != []) and (abs((point - point_nearest)) <= 0.000000001):
        #             while point < sorted(x)[i]:
        #                 i += 1
        #             y[i-1] += average_mass
        #         else:
        #             x.append(point)
        #             y.append(average_mass)
                    
                    
        
        # x.extend(component_range)
        # y.extend([] * len(component_range))





    # num_points = 1000  # high resolution along rocket length
    # x = np.linspace(0, nosecone.StartAfter(), num_points)
    # y = np.zeros_like(x)

    # for component in mass_distribution:
    #     component_range_mask = (x >= component.bottom_distance_from_aft) & (x <= component.bottom_distance_from_aft + component.length)
    #     y[component_range_mask] += component.mass / component.length
    
    wet_mass = sum(component.mass for component in mass_distribution)
    dry_mass = wet_mass - (fuel_total_propellant_mass + oxidizer_total_propellant_mass)
    total_length = mass_distribution.components[-1].StartAfter()
    return(dry_mass, wet_mass, total_length)


if __name__ == "__main__":
    mass_distribution, length_along_rocket_linspace, linear_density_array, panels_mass = calculate_mass()
    
    print(f"total mass: {sum(component.mass for component in mass_distribution) * c.KG2LB} lbm")
    print(f"engine mass: {mass_distribution.components.engine.mass * c.KG2LB:.2f} lbm")
    print(f"injector mass: {mass_distribution.components.injector.mass * c.KG2LB:.2f} lbm")

    print(f"panels mass: {panels_mass * c.KG2LB:.2f} lbm")

    plt.plot(length_along_rocket_linspace * c.M2FT, (linear_density_array * c.KG2LB / c.M2FT))
    plt.xlabel("length [feet]")
    plt.ylabel("mass density [lbs/feet]")
    plt.show()


    