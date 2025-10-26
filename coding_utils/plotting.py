import numpy as np
import matplotlib.pyplot as plt
import coding_utils.constants as c

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import inputs


def PlotColorMaps(x_axis_name, y_axis_name, variable_inputs_array, output_names, output_array, show_copv_limiting_factor):
    num_outputs = len(output_names)
    
    # Create a 2x2 grid
    square_grid_length = int(np.ceil(np.sqrt(num_outputs) - 0.0001)) # minus small number to avoid floating point rounding bs
    fig, axes = plt.subplots(square_grid_length, square_grid_length, figsize=(12, 10))  
    
    if num_outputs == 1:
        axes = [axes]  # make it iterable
    else:   
        # Flatten axes to iterate
        axes = axes.flatten()

    for ax, output_name in zip(axes, output_names):
        X, Y, Z = SetupArrays(variable_inputs_array, x_axis_name, y_axis_name, output_name, output_array)
        PlotColorMap(X, Y, Z, x_axis_name, y_axis_name, output_name, show_copv_limiting_factor, ax=ax)

    # Hide any unused subplots
    for ax in axes[num_outputs:]:
        ax.set_visible(False)

    plt.tight_layout()
    
    
    plt.show()
    
def SetupArrays(variable_inputs_array, x_axis_name, y_axis_name, output_name, output_array):
    x = np.array(variable_inputs_array[0, :][y_axis_name])
    y = np.array(variable_inputs_array[:, 0][x_axis_name])
    z = np.array(output_array[output_name])
    
    Y, X = np.meshgrid(x, y) # I don't know why you have to swap X and Y but you do!
    Z = z.reshape(len(x), len(y))
    
    return (X, Y, Z)


def PlotColorMap(X, Y, output_values, x_axis_name, y_axis_name, output_name, show_copv_limiting_factor, ax=None):
    if ax is None:
        ax = plt.gca()  # default to current axes
        
        
    axis_label_list, axis_values_list, output_label, output_values, color_scheme = FormatPlot([x_axis_name, y_axis_name], [X, Y], output_name, output_values, show_copv_limiting_factor)
    
    ax.set_xlabel(axis_label_list[0], fontsize=8)
    ax.set_ylabel(axis_label_list[1], fontsize=8)

    X, Y = *axis_values_list,
    
    if show_copv_limiting_factor:
        mesh = ax.pcolormesh(X, Y, output_values, cmap=color_scheme, vmin=0, vmax=1*c.N2LBF)
    else:
        mesh = ax.pcolormesh(X, Y, output_values, cmap=color_scheme)
        # mesh = ax.contourf(X, Y, Z, 100, cmap=color_scheme)

        
    ax.set_title(f"{output_name.title()} of {inputs.constant_inputs['FUEL_NAME'][0].title()}", fontsize=12)
    ax.set_facecolor("lightgray")
    plt.colorbar(mesh, label=output_label)



# if you want to continuously update a colormap plot as each value is calculated
def UpdateContinuousColorMap(X, Y, Z, color_variable_label="this dumbass did not change the label"):
    
    try:
        mesh.set_array(Z.ravel())
        mesh.set_clim(np.min(Z), np.max(Z))
    except NameError:
        plt.ion()
        fig, ax = plt.subplots()
        mesh = ax.pcolormesh(X, Y, Z, cmap='Spectral_r')
        plt.xlabel('OF Ratio', fontsize=12)
        plt.ylabel('Chamber Pressure [psi]', fontsize=12)
        # plt.title(f"ISP of {inputs.constant_inputs['FUEL_NAME'].item().title()} For Different {x_axis} and OF Ratios", fontsize=20)
        plt.colorbar(mesh, label=color_variable_label)
        
    plt.draw()
    plt.pause(0.5)




def PlotColorMaps3D(axis_names, variable_inputs_array, output_names, output_array, show_copv_limiting_factor):
    num_outputs = len(output_names)
    
    x_axis_name, y_axis_name, z_axis_name = axis_names[0], axis_names[1], axis_names[2]
    
    # Create a 2x2 grid
    square_grid_length = int(np.ceil(np.sqrt(num_outputs) - 0.0001)) # minus small number to avoid floating point rounding bs
    fig, axes = plt.subplots(square_grid_length, square_grid_length, figsize=(12, 10))  
    
    if num_outputs == 1:
        axes = [axes]  # make it iterable
    else:   
        # Flatten axes to iterate
        axes = axes.flatten()

    for ax, output_name in zip(axes, output_names):
        X, Y, Z, values = SetupArrays3D(variable_inputs_array, x_axis_name, y_axis_name, z_axis_name, output_name, output_array)
        PlotColorMap3D(X, Y, Z, values, x_axis_name, y_axis_name, z_axis_name, output_name, show_copv_limiting_factor, ax=ax)
    # Hide any unused subplots if there are fewer than 4 outputs
    for ax in axes[num_outputs:]:
        ax.set_visible(False)

    plt.tight_layout()
    plt.show()


def SetupArrays3D(variable_inputs_array, x_axis_name, y_axis_name, z_axis_name, output_name, output_array):
    
    # type shit !
    x = np.unique(variable_inputs_array[x_axis_name])
    y = np.unique(variable_inputs_array[y_axis_name])
    z = np.unique(variable_inputs_array[z_axis_name])

    # make 3D meshgrid
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

    # reshape output array into 3D
    values = np.array(output_array[output_name]).reshape(len(x), len(y), len(z))

    return (X, Y, Z, values)

def PlotColorMap3D(X, Y, Z, output_values, x_axis_name, y_axis_name, z_axis_name, output_name, show_copv_limiting_factor, ax=None):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    
    axis_label_list, axis_values_list, output_label, output_values, color_scheme = FormatPlot([x_axis_name, y_axis_name, z_axis_name], [X, Y, Z], output_name, output_values, show_copv_limiting_factor)

    
    # print("X values:", np.unique(X))
    # print("Y values:", np.unique(Y))

    X, Y, Z  = *axis_values_list,

    # scatter points with color mapped to values
    sc = ax.scatter(X.flatten(), Y.flatten(), Z.flatten(),
                    c=output_values.flatten(), cmap=color_scheme, marker='o')

    # choose color scheme
    cmap = "RdYlGn" if show_copv_limiting_factor else "RdBu_r"
    
    ax.set_xlabel(axis_label_list[0], fontsize=8)
    ax.set_ylabel(axis_label_list[1], fontsize=8)
    ax.set_zlabel(axis_label_list[2], fontsize=8)

    fig.colorbar(sc, ax=ax, label=output_label)

    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
def FormatPlot(axis_name_list, axis_values_list, output_name, output_values, show_copv_limiting_factor):

    axis_label_list = [""] * len(axis_name_list)

    for count, axis_name in enumerate(axis_name_list):    
        axis_values_factor = 1 # in case no factor is needed
        if axis_name == "OF_RATIO":
            axis_label = "OF Ratio"
        elif axis_name == "FUEL_TANK_LENGTH":
            axis_values_factor = c.M2IN
            axis_label = "Fuel Tank Length [in]"
        elif axis_name == "CONTRACTION_RATIO":
            axis_label = "Chamber to Throat Contraction Ratio"
        elif axis_name == "CHAMBER_PRESSURE":
            axis_values_factor = c.PA2PSI
            axis_label = "Chamber Pressure [psi]"
        else:
            raise ValueError("axis name not recognized for plotting")

        axis_label_list[count] = axis_label
        axis_values_list[count] = axis_values_list[count] * axis_values_factor
    
    output_values_factor = 1 # in case no factor is needed
    contour_lines = -1        
    if output_name == "JET_THRUST":
        output_values_factor = c.N2LBF
        output_label="Jet Thrust [lbf]"
    elif output_name == "MASS_FLOW_RATE":
        output_label="Mass Flow Rate [kg/s]"
    elif output_name == "ISP":
        # num_lines = 8
        # power = 1/4
        # contour_lines = np.max(output_array[output_name]) * 0.995 / (num_lines**power) * np.linspace(1, num_lines, num_lines)**power
        output_label="isp [s]"
    elif output_name == "CHAMBER_TEMPERATURE":
        output_label="Chamber Temperature [k]"
    elif output_name == "TANK_PRESSURE":
        output_values_factor = c.PA2PSI
        output_label="Tank Pressure [psi]"
    
    
    
    elif output_name == "CHAMBER_DIAMETER":
        output_values_factor = c.M2IN
        output_label="Chamber Diameter [in]"
    elif output_name == "THROAT_DIAMETER":
        output_values_factor = c.M2IN
        output_label="Throat Diameter [in]"
    
    elif output_name == "TOTAL_IMPULSE":
        output_label="Total Impulse [newtons-seconds]"
    elif output_name == "APOGEE":
        output_values_factor = c.M2FT
        # altitude_limit = ax.contour(X, Y, Z, levels=[10000], colors='red', linewidths=2)
        # ax.clabel(altitude_limit, fmt='%d')
        output_label="Estimated Apogee [ft]"
    elif output_name == "TAKEOFF_TWR":
        output_label="Takeoff TWR"
    elif output_name == "RAIL_EXIT_TWR":
        output_label="Rail Exit TWR"
    elif output_name == "WET_MASS":
        output_values_factor = c.KG2LB
        output_label="Wet Rocket Mass [lbm]"
    elif output_name == "DRY_MASS":
        output_values_factor = c.KG2LB
        output_label="Dry Rocket Mass [lbm]"
    elif output_name == "BURN_TIME":
        output_label="Burn Time [s]"
    elif output_name == "RAIL_EXIT_VELOCITY":
        output_label="Rail Exit Velocity [m/s]"
    elif output_name == "RAIL_EXIT_ACCELERATION":
        output_values_factor = 1 / c.GRAVITY
        output_label="Rail Exit Acceleration [G's]"
    elif output_name == "MAX_ACCELERATION":
        output_values_factor = 1 / c.GRAVITY
        output_label="Max Acceleration [G's]"
    elif output_name == "MAX_VELOCITY":
        output_values_factor = 1 / 343 # [m/s] 343 is da speed of sound
        output_label="Max Velocity [Mach]"
    
    elif output_name == "TOTAL_LENGTH":
        output_values_factor = c.M2FT
        output_label="Total Length [ft]"
    
    elif output_name == "OXIDIZER_TANK_LENGTH":
        output_values_factor = c.M2FT
        output_label="Oxidizer Tank Length [ft]"
    
    elif output_name == "OXIDIZER_TANK_VOLUME":
        output_values_factor = c.M32L
        output_label="Oxidizer Tank Volume [liters]"
        
    elif output_name == "OXIDIZER_TOTAL_MASS":
        output_values_factor = c.KG2LB
        output_label="Oxidizer Tank Mass [lbm]"
    
    elif output_name == "FUEL_TANK_VOLUME":
        output_values_factor = c.M32L
        output_label="Fuel Tank Volume [liters]"
        
    elif output_name == "FUEL_TOTAL_MASS":
        output_values_factor = c.KG2LB
        output_label="Fuel Tank Mass [lbm]"        
    
    elif output_name == "CHAMBER_LENGTH":
        output_values_factor = c.M2IN
        output_label="CHAMBER_LENGTH [in]"        
        
    else:
        raise ValueError(f"{output_name} not recognized for plotting")


    output_values = output_values * output_values_factor
    
    # if contour_lines == -1:
    #     ax.contour(X, Y, Z)
    # else:
    #     ax.contour(X, Y, Z, contour_lines)

    
    if show_copv_limiting_factor:
        color_scheme = "RdYlGn"
        
    else:
        color_scheme = "RdBu_r"
        "Spectral_r"
    
    return (axis_label_list, axis_values_list, output_label, output_values, color_scheme)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def SetupHolyFuckArrays(variable_inputs_array, x_axis_name, y_axis_name, output_name, output_array):
    x = np.array(variable_inputs_array[0, :][y_axis_name])
    y = np.array(variable_inputs_array[:, 0][x_axis_name])
    z = np.array(output_array[output_name])
    
    Y, X = np.meshgrid(x, y) # I don't know why you have to swap X and Y but you do
    Z = z.reshape(len(x), len(y))
    
    return (X, Y, Z)

    
    
def HolyFuck(X, Y, Z):
    from matplotlib import cm
    from mpl_toolkits.mplot3d import axes3d
    
    

    ax = plt.figure().add_subplot(projection='3d')
    X, Y, Z = axes3d.get_test_data(0.05)

    ax.contour(X, Y, Z, cmap=cm.coolwarm)  # Plot contour curves

    plt.show()
    
if __name__ == "__main__":
    HolyFuck(1,1,1)