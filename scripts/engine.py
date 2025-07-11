# import CEA_Wrap
import numpy as np


def size_engine(chamber_radius, fuel_name, oxidizer_name, contraction_ratio):
    chamber_area = radius_to_area(chamber_radius)
    throat_area = chamber_area / contraction_ratio
    throat_radius = area_to_radius(throat_area)
    chamber_length = calculate_chamber_length(throat_area, chamber_area, fuel_name, oxidizer_name)
    return (chamber_radius, chamber_length, throat_radius)

def area_to_radius(area):
    radius = (area/np.pi)**0.5
    return radius

def radius_to_area(radius):
    area = np.pi * (radius**2)
    return area

def calculate_chamber_length(throat_area, chamber_area, fuel_name, oxidizer_name):
    L_star = find_L_star(fuel_name, oxidizer_name)
    chamber_length = (throat_area * L_star) / (chamber_area)
    return chamber_length

def find_L_star(fuel_name, oxidizer_name):
    L_star = None
    if (oxidizer_name == "Liquid Oxygen"):
        if (fuel_name == "Ethanol"):
            # L_star = 40
            raise ValueError("No value for L*")
        if (fuel_name == "Kerosene"):
            L_star = 50
    return L_star

if __name__ == "__main__":
    import coding_utils.draw_tool as draw
    draw.DrawEngine(3,5,1.5,2,2,6,10)