import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import coding_utils.constants as c
import vehicle_scripts.numpy_ndarray_handler as NNH

os.environ["CEA_USE_LEGACY"] = "1" # https://github.com/civilwargeeky/CEA_Wrap/issues/8
import CEA_Wrap as CEA
import numpy as np


def ThrustyBusty(FUEL_NAME, OXIDIZER_NAME, PROPELLANT_TANK_OUTER_DIAMETER, CONTRACTION_RATIO, OF_RATIO, CHAMBER_PRESSURE):
# def ThrustyBusty(FUEL_NAME, OXIDIZER_NAME, PROPELLANT_TANK_OUTER_DIAMETER, CONTRACTION_RATIO, OF_RATIO, CHAMBER_PRESSURE, cea_results):

    cea_results = RunCEA(CHAMBER_PRESSURE, FUEL_NAME, OXIDIZER_NAME, OF_RATIO)
    
    expected_isp = CalculateExpectedISP(cea_results["isp"])
    chamber_temperature = cea_results["c_t"]

    expected_exhaust_velocity = expected_isp * c.GRAVITY
    
    chamber_radius, chamber_length, throat_radius = CalculateEngineDimensions(PROPELLANT_TANK_OUTER_DIAMETER, FUEL_NAME, OXIDIZER_NAME, CONTRACTION_RATIO)
    expected_total_mass_flow_rate = CalculateMassFlowRate(throat_radius, CHAMBER_PRESSURE, cea_results["c_mw"], cea_results["c_gamma"], chamber_temperature)

    expected_jet_thrust = CalculateExpectedThrust(expected_isp, expected_total_mass_flow_rate)

    # print(expected_total_mass_flow_rate, expected_exhaust_velocity)
    # return(expected_thrust, expected_isp, total_mass_flow_rate, chamber_radius, chamber_length, throat_radius)
    return(expected_jet_thrust, expected_isp, expected_total_mass_flow_rate, chamber_temperature)


def CreateMassiveCEAArray(constant_inputs_array, variable_inputs_array):
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


    it = np.nditer(variable_inputs_array, flags=["multi_index"], op_flags=["readonly"])
    for variable_input_combination in it: 
        # ((it.multi_index, variable_input_combination.copy()))
        
        cea_results = RunCEA(NNH.GetFrom_ndarray("CHAMBER_PRESSURE", CIA, VIA[it.multi_index]), 
                             NNH.GetFrom_ndarray("FUEL_NAME", CIA, VIA[it.multi_index]),
                             NNH.GetFrom_ndarray("OXIDIZER_NAME", CIA, VIA[it.multi_index]), 
                             NNH.GetFrom_ndarray("OF_RATIO", CIA, VIA[it.multi_index]), 
                            )
        
        hardcoded_cea_results = np.zeros(1, dtype=fields_dtype)
        help = [cea_results.c_t, cea_results.c_mw, cea_results.c_gamma, cea_results.isp] # i am dumb
        
        for count, (name, _) in enumerate(fields_dtype):
            hardcoded_cea_results[name] = help[count]

        CEAArray[it.multi_index] = hardcoded_cea_results

    return(CEAArray)


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

def CalculateExpectedThrust(expected_isp, total_mass_flow_rate):
    
    expected_jet_exhaust_velocity = expected_isp * c.GRAVITY
    expected_jet_thrust = total_mass_flow_rate * expected_jet_exhaust_velocity
    
    return(expected_jet_thrust)

def CalculateExpectedISP(ideal_isp):
    expected_c_star_efficiency = 0.9 # value used for CMS
    expected_nozzle_efficiency = 0.9 # value used for CMS
        
    expected_isp = ideal_isp * expected_c_star_efficiency * expected_nozzle_efficiency
    
    return(expected_isp)

# fixed :)
def CalculateMassFlowRate(throat_radius, chamber_pressure, chamber_molar_mass, chamber_gamma, T_c): # eq (1-19) on page 7 of sp-125 https://ntrs.nasa.gov/citations/19710019929
    y = chamber_gamma # for readability
    
    R = 8.314 / (chamber_molar_mass/1000) # R is the specific gas constant here
    # R /= 1000
    
    radicand = (y/(R*T_c)) * ( (2/(y+1)) ** (((y+1) / (y-1))) )
    
    throat_area = RadiusToArea(throat_radius)
    expected_total_mass_flow_rate = throat_area * chamber_pressure * (radicand**0.5)
    
    expected_c_star_efficiency = 0.9 # value used for CMS
    expected_total_mass_flow_rate *= expected_c_star_efficiency
    return expected_total_mass_flow_rate

def CalculateEngineDimensions(PROPELLANT_TANK_OUTER_DIAMETER, fuel_name, oxidizer_name, contraction_ratio):
    chamber_radius = (PROPELLANT_TANK_OUTER_DIAMETER/2) - (1 * c.IN2M) # lowkey a guess
    chamber_area = RadiusToArea(chamber_radius)
    
    throat_area = chamber_area/contraction_ratio
    throat_radius = AreaToRadius(throat_area)
    
    chamber_length = CalculateChamberLength(throat_area, chamber_area, fuel_name, oxidizer_name)
    return (chamber_radius, chamber_length, throat_radius)

def AreaToRadius(area):
    radius = (area/np.pi)**0.5
    return radius

def RadiusToArea(radius):
    area = np.pi*(radius**2)
    return area

def CalculateChamberLength(throat_area, chamber_area, fuel_name, oxidizer_name):
    L_star = FindLstar(fuel_name, oxidizer_name)
    chamber_length = (throat_area * L_star) / (chamber_area)
    return chamber_length

def FindLstar(fuel_name, oxidizer_name):
    if (oxidizer_name == "liquid oxygen"):
        if (fuel_name == "ethanol"):
            L_star = 45 * c.IN2M # source:  my asshole
        elif (fuel_name == "kerosene"):
            L_star = 45 * c.IN2M # table 4-1 on page 87 of nasa sp-125 https://ntrs.nasa.gov/citations/19710019929
        elif (fuel_name == "ipa"):
            L_star = 10000000000 * c.IN2M # 
        else:
            raise ValueError("No L* Found")
    else:
        raise ValueError("No L* Found")
        
    return L_star



if __name__ == "__main__":
    print(RunCEA(500 * c.PSI2PA, "ethanol", "liquid oxygen", 1.1).isp) # should be ?????