import numpy as np
from tqdm import tqdm
import inputs

import numpy
from concurrent.futures import ThreadPoolExecutor, as_completed

from vehicle_scripts import numpy_ndarray_handler
from coding_utils import constants as c
from inputs import constant_inputs as constant_inputs_dict

def ThreadedRun(run_rocket_function, variable_inputs_array, output_names, USE_AI_SLOP):

    fields_dtype = [] # datatype for output array

    for output_name in output_names:
        fields_dtype.append((output_name, np.float32))
    
    output_array = np.zeros(variable_inputs_array.size, dtype=np.dtype(fields_dtype))
    output_array = output_array.reshape(variable_inputs_array.shape)
    

    if USE_AI_SLOP:

        jobs = []
        it = np.nditer(variable_inputs_array, flags=["multi_index"], op_flags=["readonly"])
        for variable_input_combination in it: 
            jobs.append((it.multi_index, variable_input_combination.copy()))


        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(run_rocket_function, idx, v) for idx, v in jobs]
            for f in tqdm(as_completed(futures), total=len(futures), desc="Computing rocket performance"):
                idx, output_list = f.result()
              
                output_array[idx] = output_list

    else:

        # Iterate while keeping the structure
        it = np.nditer(variable_inputs_array, flags=["multi_index"], op_flags=["readonly"])
        
        # for variable_input_combination in tqdm(it, total=len(it), desc="Computing..."):
        for count, variable_input_combination in enumerate(it):
            
            idx = 1
            idx, thrust_newton, mass_flow_kg, isp, estimated_apogee = run_rocket_function(idx, variable_input_combination,)
            
            thrust_map[count] = (thrust_newton * c.N2LBF)
            mass_flow_map[count] = mass_flow_kg
            isp_map[count] = isp
            estimated_apogee_map[count] = estimated_apogee
            
            print(f"{it.multi_index}: {variable_input_combination} -> {thrust_newton * c.N2LBF}")
            
            # X, Y, Z = p.SetupArrays(variable_inputs_array, isp_map)
            # p.UpdateContinuousColorMap(X, Y, Z, constant_inputs_array)

    return (output_array)