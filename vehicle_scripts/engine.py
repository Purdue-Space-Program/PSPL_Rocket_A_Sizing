import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import coding_utils.constants as c
import vehicle_scripts.numpy_ndarray_handler as NNH

os.environ["CEA_USE_LEGACY"] = "1" # https://github.com/civilwargeeky/CEA_Wrap/issues/8
import CEA_Wrap as CEA
import numpy as np
from tqdm import tqdm

from concurrent.futures import ThreadPoolExecutor, as_completed
from scipy.optimize import fsolve


def ThrustyBusty(FUEL_NAME, OXIDIZER_NAME, PROPELLANT_TANK_OUTER_DIAMETER, CONTRACTION_RATIO, OF_RATIO, CHAMBER_PRESSURE, CEA_Array_Result=None):
# def ThrustyBusty(FUEL_NAME, OXIDIZER_NAME, PROPELLANT_TANK_OUTER_DIAMETER, CONTRACTION_RATIO, OF_RATIO, CHAMBER_PRESSURE, cea_results):

    if CEA_Array_Result == None:
        cea_results = RunCEA(CHAMBER_PRESSURE, FUEL_NAME, OXIDIZER_NAME, OF_RATIO)
    else:
        cea_results = CEA_Array_Result
    
    expected_isp = CalculateExpectedISP(cea_results["isp"])
    chamber_temperature = cea_results["c_t"]

    expected_exhaust_velocity = expected_isp * c.GRAVITY
    
    chamber_radius, chamber_length, throat_radius, injector_to_throat_length = CalculateEngineDimensions(PROPELLANT_TANK_OUTER_DIAMETER, FUEL_NAME, OXIDIZER_NAME, CONTRACTION_RATIO)
    expected_total_mass_flow_rate = CalculateMassFlowRate(throat_radius, CHAMBER_PRESSURE, cea_results["c_mw"], cea_results["c_gamma"], chamber_temperature)

    expected_jet_thrust = CalculateExpectedThrust(expected_isp, expected_total_mass_flow_rate)

    M_straight_wall = CalculateMachNumber(cea_results["gamma"], CONTRACTION_RATIO, 0.02)

    heat_transfer_coefficient = CalculateHeatTransferCoefficient(
        Dt = chamber_radius*2,  # local diameter
        Rt = ((1.5 * throat_radius) + (0.382 *throat_radius)) / 2,     #radius of throat curve (m)
        Pr = cea_results["pran"], #Prandtl number of the combustion gas (n/a)
        gamma = cea_results["gamma"], #specific heat ratio of the combustion gas (n/a)
        c_star = cea_results.cstar, #characteristic exhaust velocity (m/s)
        T0 = cea_results["c_t"], #stagnation temperature of the combustion gas ((K))
        Twg = CalculateRecoveryTemperature( #recovery temperature at the wall
            T_static = cea_results["c_t"] / (1 + (((cea_results["gamma"] - 1)/2) * M_straight_wall**2)),
            gamma = cea_results["gamma"],
            M = M_straight_wall,
            Pr = cea_results["pran"]
        ),
        Cp = cea_results["cp"] * 1000, #specific heat at constant pressure of the combustion
        P0 = CHAMBER_PRESSURE, #chamber pressure (Pascals)
        mu = CalculateViscosity(
            T = cea_results["c_t"] / (1 + (((cea_results["gamma"] - 1)/2) * M_straight_wall**2)), #static temperature at the local axial point (K)
            T_ref = cea_results["c_t"], #stagnation temperature from CEA (K)
            mu_ref = cea_results["visc"], #dynamic viscosity from CEA at the stagnation temperature (Pascal - seconds)
            S = 110.4 #Sutherland's constant for combustion gases (K)
        ), #dynamic viscosity of the combustion gas (Pascal - seconds)
        M = M_straight_wall, #Mach number at the local axial point (no units)
        local_Area_ratio = CONTRACTION_RATIO #area ratio at the local axial point (no units)
    )
    print(heat_transfer_coefficient)

    # print(expected_total_mass_flow_rate, expected_exhaust_velocity)
    # return(expected_thrust, expected_isp, total_mass_flow_rate, chamber_radius, chamber_length, throat_radius)
    return(expected_jet_thrust, expected_isp, expected_total_mass_flow_rate, chamber_temperature, chamber_radius, throat_radius, chamber_length, injector_to_throat_length)


def CreateMassiveCEAArray(constant_inputs_array, variable_inputs_array):
    # not faster :(
    
    CIA = constant_inputs_array
    VIA = variable_inputs_array


    # fields_dtype.append((output_name, np.float32))
    fields_dtype = [
    # ("massf", np.bool),
    # ("p", np.float32),
    # ("t_p", np.float32),
    # ("c_p", np.float32),
    # ("t", np.float32),
    # ("t_t", np.float32),
    ("c_t", np.float32),
    # ("h", np.float32),
    # ("t_h", np.float32),
    # ("c_h", np.float32),
    # ("rho", np.float32),
    # ("t_rho", np.float32),
    # ("c_rho", np.float32),
    # ("son", np.float32),
    # ("t_son", np.float32),
    # ("c_son", np.float32),
    # ("visc", np.float32),
    # ("t_visc", np.float32),
    # ("c_visc", np.float32),
    # ("cond", np.float32),
    # ("t_cond", np.float32),
    # ("c_cond", np.float32),
    # ("pran", np.float32),
    # ("t_pran", np.float32),
    # ("c_pran", np.float32),
    # ("mw", np.float32),
    # ("t_mw", np.float32),
    ("c_mw", np.float32),
    # ("m", np.float32),
    # ("t_m", np.float32),
    # ("c_m", np.float32),
    # ("condensed", np.bool),
    # ("t_condensed", np.bool),
    # ("c_condensed", np.bool),
    # ("cp", np.float32),
    # ("t_cp", np.float32),
    # ("c_cp", np.float32),
    # ("gammas", np.float32),
    # ("t_gammas", np.float32),
    # ("c_gammas", np.float32),
    # ("gamma", np.float32),
    # ("t_gamma", np.float32),
    ("c_gamma", np.float32),
    ("isp", np.float32),
    # ("t_isp", np.float32),
    # ("ivac", np.float32),
    # ("t_ivac", np.float32),
    # ("cf", np.float32),
    # ("t_cf", np.float32),
    
    # ("cstar", np.float32),
    # ("mach", np.float32),
    # ("o_f", np.float32),
    # ("phi", np.float32),
    # ("ae", np.float32),
    # ("t_ae", np.float32),
    # ("pip", np.float32),
    # ("t_pip", np.float32),
    ]
    
    # for output_name in output_names:
    #     fields_dtype.append((output_name, np.float32))

    CEAArray = np.zeros(variable_inputs_array.size, dtype=np.dtype(fields_dtype))
    CEAArray = CEAArray.reshape(variable_inputs_array.shape)

    # Make a list of all indices to parallelize over
    indices = list(np.ndindex(variable_inputs_array.shape))

    def inner_function(multi_index):
        cea_results = RunCEA(
                        NNH.GetFrom_ndarray("CHAMBER_PRESSURE", CIA, VIA[multi_index]), 
                        NNH.GetFrom_ndarray("FUEL_NAME", CIA, VIA[multi_index]),
                        NNH.GetFrom_ndarray("OXIDIZER_NAME", CIA, VIA[multi_index]), 
                        NNH.GetFrom_ndarray("OF_RATIO", CIA, VIA[multi_index]), 
                    )
        
        hardcoded_cea_results = np.zeros(1, dtype=fields_dtype)
        help = [cea_results.c_t, cea_results.c_mw, cea_results.c_gamma, cea_results.isp] # i am dumb
        for count, (name, _) in enumerate(fields_dtype):
            hardcoded_cea_results[name] = help[count]

        CEAArray[multi_index] = hardcoded_cea_results

    with ThreadPoolExecutor() as thread_pool:
        thread_pool.map(inner_function, indices)
        list(tqdm(
            thread_pool.map(inner_function, indices),
            total=len(indices),
            desc="Creating Massive CEA Array"
        ))
        
    return(CEAArray)

    
    # for variable_input_combination in tqdm(it, total=it.itersize, desc="Creating Massive CEA Array"): 
        
    #     cea_results = RunCEA(NNH.GetFrom_ndarray("CHAMBER_PRESSURE", CIA, VIA[it.multi_index]), 
    #                          NNH.GetFrom_ndarray("FUEL_NAME", CIA, VIA[it.multi_index]),
    #                          NNH.GetFrom_ndarray("OXIDIZER_NAME", CIA, VIA[it.multi_index]), 
    #                          NNH.GetFrom_ndarray("OF_RATIO", CIA, VIA[it.multi_index]), 
    #                         )
        
    #     hardcoded_cea_results = np.zeros(1, dtype=fields_dtype)
    #     help = [cea_results.c_t, cea_results.c_mw, cea_results.c_gamma, cea_results.isp] # i am dumb
        
    #     for count, (name, _) in enumerate(fields_dtype):
    #         hardcoded_cea_results[name] = help[count]

    #     CEAArray[it.multi_index] = hardcoded_cea_results

    # return(CEAArray)


def RunCEA(
    chamber_pressure,
    fuel_name,
    oxidizer_name,
    OF_Ratio,
):
    # convert regular string for propellants to what CEA_wrap uses
    if fuel_name == "ethanol":
        CEA_fuel_name = CEA.Fuel("C2H5OH(L)", temp=c.T_AMBIENT)
    elif fuel_name == "kerosene":
        CEA_fuel_name = CEA.Fuel("Jet-A(L)", temp=c.T_AMBIENT)
    elif fuel_name == "ipa":
        CEA_fuel_name = CEA.Fuel("C3H8O,2propanol", temp=c.T_AMBIENT)
    else:
        raise ValueError(f"{fuel_name} not supported")

    if oxidizer_name == "liquid oxygen":
        CEA_oxidizer_name = CEA.Oxidizer("O2(L)", temp=90) # 90 K is temperature of oxidizer upon injection into combustion (same as copperhead's sizing)
    elif oxidizer_name == "nitrous":
        CEA_oxidizer_name = CEA.Oxidizer("N2O(L),298.15", temp=c.T_AMBIENT)
    else:
        raise ValueError(f"{oxidizer_name} not supported")


    pressure_ratio = chamber_pressure / (15 * c.PSI2PA) # assume exit pressure is a constantly at the pressure of air a bit above sea level

    rocket = CEA.RocketProblem(
        pressure =       chamber_pressure * c.PA2PSI,
        pip =            pressure_ratio, # pip is "Pressure ratio of chamber pressure to exit pressure." github.com/civilwargeeky/CEA_Wrap/blob/main/README.md#rocket-problem-constructor-additional-parameters
        materials =      [CEA_fuel_name, CEA_oxidizer_name],
        o_f =            OF_Ratio,
        pressure_units = "psi",
    )

    cea_results = rocket.run()

    return(cea_results)

def CalculateHeatTransferCoefficient(Dt, Rt, Pr, gamma, c_star, T0, Twg, Cp, P0, mu, M, local_Area_ratio):
    # sigma (Bartz correction)
    sigma_parentheses1 = ((0.5 * (Twg / T0) * (1 + (((gamma - 1) * M**2)/2))) + 0.5) ** 0.68
    sigma_parentheses2 = (1 + (((gamma - 1)/2) * (M**2))) ** 0.12
    sigma = 1.0 / (sigma_parentheses1 * sigma_parentheses2)

    # Bartz core terms 
    heat_transfer_term1 = 0.026 / (Dt ** 0.2)
    heat_transfer_term2 = ((mu ** 0.2) * Cp) / (Pr ** 0.6)
    heat_transfer_term3 = (P0 / (c_star)) ** 0.8
    heat_transfer_term4 = (Dt / Rt) ** 0.1

    # using inverse of local_Area_ratio so heat goes up as A goes down 
    area_factor = (1/local_Area_ratio) ** 0.9

    heat_transfer_coefficient = heat_transfer_term1 * heat_transfer_term2 * heat_transfer_term3 * heat_transfer_term4 * area_factor * sigma

    return heat_transfer_coefficient

def CalculateRecoveryTemperature(T_static, gamma, M, Pr):
    r = Pr ** (1/2)
    T_r = T_static * (1 + ((r*(gamma-1)/2) * M**2))
    return T_r

def CalculateViscosity(T, T_ref, mu_ref, S):
    mu = mu_ref * ((T / T_ref) ** 1.5) * ((T_ref + S) / (T + S))
    return mu

def CalculateMachNumber(gamma, area_ratio_value, initial_guess):
    def f(M):
        Mach_function_part1 = ((gamma + 1)/2)**(-(gamma + 1)/(2*(gamma-1)))
        Mach_function_part2 = (1/M) * ((1 + (((gamma - 1)/2) * M**2)) ** ((gamma + 1)/(2*(gamma-1))))
        Mach_function = (Mach_function_part1 * Mach_function_part2) - area_ratio_value
        return Mach_function
    guess = initial_guess
    guess = min(0.8, max(0.05, guess))
    M_solution = fsolve(f, guess)
    return float(M_solution[0])

def CalculateExpectedThrust(expected_isp, total_mass_flow_rate):
    
    expected_jet_exhaust_velocity = expected_isp * c.GRAVITY
    expected_jet_thrust = total_mass_flow_rate * expected_jet_exhaust_velocity
    
    # print(f"expected_jet_exhaust_velocity: {expected_jet_exhaust_velocity:.2f} m/s")
    
    return(expected_jet_thrust)

def CalculateExpectedISP(ideal_isp):
    expected_c_star_efficiency = 1.0#0.9 # value used for CMS
    expected_nozzle_efficiency = 1.0#0.9 # value used for CMS
        
    expected_isp = ideal_isp * expected_c_star_efficiency * expected_nozzle_efficiency
    
    return(expected_isp)

# fixed :)
def CalculateMassFlowRate(throat_radius, chamber_pressure, chamber_molar_mass, chamber_gamma, T_c): # eq (1-19) on page 7 of sp-125 https://ntrs.nasa.gov/citations/19710019929
    y = chamber_gamma # for equation readability
    
    R = 8.314 / (chamber_molar_mass/1000) # R is the specific gas constant here
    
    radicand = (y/(R*T_c)) * ( (2/(y+1)) ** (((y+1) / (y-1))) )
    
    throat_area = RadiusToArea(throat_radius)
    expected_total_mass_flow_rate = throat_area * chamber_pressure * (radicand**0.5)
    
    expected_c_star_efficiency = 1.0#0.9 # value used for CMS
    expected_total_mass_flow_rate *= expected_c_star_efficiency
    return expected_total_mass_flow_rate

def CalculateEngineDimensions(PROPELLANT_TANK_OUTER_DIAMETER, fuel_name, oxidizer_name, contraction_ratio):
    chamber_wall_thickness = 0.25 * c.IN2M # kinda vibed out
    # chamber_wall_thickness = 0.5 * c.IN2M # kinda vibed out
    
    flange_thickness = 0.3 * c.IN2M # kinda vibed out
    
    # chamber_radius = (PROPELLANT_TANK_OUTER_DIAMETER/2) - (2 * chamber_wall_thickness) - (2 * flange_thickness)
    # chamber_radius = (PROPELLANT_TANK_OUTER_DIAMETER/2) - chamber_wall_thickness - flange_thickness
    chamber_radius = 1.0 * c.IN2M 
    # chamber_radius = (PROPELLANT_TANK_OUTER_DIAMETER/2) - (1 * c.IN2M) # lowkey a guess
    
    chamber_area = RadiusToArea(chamber_radius)

    throat_area = chamber_area/contraction_ratio
    throat_radius = AreaToRadius(throat_area)
    
    chamber_length, injector_to_throat_length = CalculateChamberLength(throat_area, chamber_area, fuel_name, oxidizer_name)
    return (chamber_radius, chamber_length, throat_radius, injector_to_throat_length)

def AreaToRadius(area):
    radius = (area/np.pi)**0.5
    return radius

def RadiusToArea(radius):
    area = np.pi*(radius**2)
    return area

def CalculateChamberLength(throat_area, cylinder_area, fuel_name, oxidizer_name):
    #L_star = FindLstar(fuel_name, oxidizer_name)
    L_star = 56 * c.IN2M
    #cylinder_volume = (L_star * throat_area)
    
    #pintle_length = 1 * c.IN2M
    #converging_section_effective_length = 1.887355326317635 * c.IN2M # the effective length that the converging section contributes to residence time
    #non_straight_wall_before_throat_length =  3.1744 * c.IN2M # [inches] constant from chamber contour script
    
    #straight_wall_length = (cylinder_volume / cylinder_area) + pintle_length - converging_section_effective_length
    #injector_to_throat_length = straight_wall_length + non_straight_wall_before_throat_length
    
    straight_wall_length = 2.0 * c.IN2M
    injector_to_throat_length = 3.5 * c.IN2M
    
    return straight_wall_length, injector_to_throat_length

def FindLstar(fuel_name, oxidizer_name):
    if (oxidizer_name == "liquid oxygen"):
        if (fuel_name == "ethanol"):
            L_star = 45 * c.IN2M # source: my asshole (brazil)
        elif (fuel_name == "kerosene"):
            L_star = 45 * c.IN2M # table 4-1 on page 87 of nasa sp-125 https://ntrs.nasa.gov/citations/19710019929
        elif (fuel_name == "ipa"):
            L_star = 45 * c.IN2M # best source i got... https://docs.google.com/presentation/d/1BgoW4NsStkoPDfLUcNBo5q-SOjZwojqc4FWam491l4I/edit?slide=id.g21452e51da0_0_25#slide=id.g21452e51da0_0_25
        else:
            raise ValueError("No L* Found")
    else:
        raise ValueError("No L* Found")
        
    return L_star



if __name__ == "__main__":
    print(RunCEA(500 * c.PSI2PA, "ethanol", "liquid oxygen", 1.1).isp) # should be ?????