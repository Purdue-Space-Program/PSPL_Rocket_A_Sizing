import numpy as np
from tqdm import tqdm
import inputs



from vehicle_scripts import engine


import numpy
from concurrent.futures import ThreadPoolExecutor, as_completed

from vehicle_scripts import numpy_ndarray_handler
from coding_utils import constants as c
from inputs import constant_inputs as constant_inputs_dict

def ThreadedRun(run_rocket_function, constant_inputs_array, variable_inputs_array, USE_AI_SLOP):

    if USE_AI_SLOP:

        jobs = []
        it = np.nditer(variable_inputs_array, flags=["multi_index"], op_flags=["readonly"])
        for variable_input_combination in it: 
            jobs.append((it.multi_index, variable_input_combination.copy()))

        thrust_map = np.zeros(variable_inputs_array.size)
        mass_flow_map = np.zeros(variable_inputs_array.size)
        isp_map = np.zeros(variable_inputs_array.size)

        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(run_rocket_function, idx, v) for idx, v in jobs]
            for f in tqdm(as_completed(futures), total=len(futures), desc="Computing thrust"):
                idx, thrust_lbf, mass_flow, isp = f.result()
                thrust_map[(idx[0])*inputs.step_size + idx[1]] = thrust_lbf
                mass_flow_map[(idx[0])*inputs.step_size + idx[1]] = mass_flow
                isp_map[(idx[0])*inputs.step_size + idx[1]] = isp
                
                # print(f"{idx}: {variable_inputs_array[idx]} -> {thrust}")
                
                # # goofy
                # X, Y, Z = p.SetupArrays(variable_inputs_array, isp_map)            
                # p.UpdateContinuousColorMap(X, Y, Z, constant_inputs_array, color_variable_label="this dumbass did not change the label")


    else:
        thrust_map = []
        mass_flow_map = []
        # isp_map = []
        isp_map = np.zeros(variable_inputs_array.size)

        # Iterate while keeping the structure
        it = np.nditer(variable_inputs_array, flags=["multi_index"], op_flags=["readonly"])
        
        # for variable_input_combination in tqdm(it, total=len(it), desc="Computing..."):
        for count, variable_input_combination in enumerate(it):
            
            idx = 1
            idx, thrust_newton, mass_flow_kg, isp = run_rocket_function(idx, variable_input_combination,)
            
             
            
            thrust_map.append(thrust_newton * c.N2LBF)
            mass_flow_map.append(mass_flow_kg)
            isp_map[count] = isp
            
            print(f"{it.multi_index}: {variable_input_combination} -> {thrust_newton * c.N2LBF}")
            
            # X, Y, Z = p.SetupArrays(variable_inputs_array, isp_map)
            # p.UpdateContinuousColorMap(X, Y, Z, constant_inputs_array)

    return (thrust_map, isp_map, mass_flow_map)