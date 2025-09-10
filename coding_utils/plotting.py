import numpy as np
import matplotlib.pyplot as plt
import coding_utils.constants as c

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import inputs


def PlotColorMaps(x_axis_name, y_axis_name, variable_inputs_array, output_names, output_array):
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
        PlotColorMap(X, Y, Z, x_axis_name, y_axis_name, output_name, output_array, ax=ax)

    # Hide any unused subplots if there are fewer than 4 outputs
    for ax in axes[num_outputs:]:
        ax.set_visible(False)

    plt.tight_layout()
    
    
    plt.show()
    
def SetupArrays(variable_inputs_array, x_axis_name, y_axis_name, output_name, output_array):
    x = np.array(variable_inputs_array[0, :][y_axis_name]) # what the fuck !
    y = np.array(variable_inputs_array[:, 0][x_axis_name]) # what the fuck !
    z = np.array(output_array[output_name])
    
    Y, X = np.meshgrid(x, y) # I don't know why you have to swap X and Y but you do
    Z = z.reshape(len(x), len(y))
    
    return (X, Y, Z)


def PlotColorMap(X, Y, Z, x_axis_name, y_axis_name, output_name, output_array, ax=None):
    if ax is None:
        ax = plt.gca()  # default to current axes
        
    if x_axis_name == "OF_RATIO":
        ax.set_xlabel('OF Ratio', fontsize=8)
    elif x_axis_name == "FUEL_TANK_LENGTH":
        X = X * c.M2IN
        ax.set_xlabel('Fuel Tank Length [in]', fontsize=8)
    elif x_axis_name == "WET_MASS_TO_USABLE_PROPELLANT_MASS_RATIO":
        ax.set_xlabel('Wet Mass to Usable Propellant Mass Ratio', fontsize=8)
    elif x_axis_name == "CONTRACTION_RATIO":
        ax.set_xlabel('Chamber to Throat Contraction Ratio', fontsize=8)
    
    if y_axis_name == "CHAMBER_PRESSURE":
        Y = Y * c.PA2PSI
        ax.set_ylabel('Chamber Pressure [psi]', fontsize=8)
    elif y_axis_name == "FUEL_TANK_LENGTH":
        Y = Y * c.M2IN
        ax.set_ylabel('Fuel Tank Length [in]', fontsize=8)
    elif y_axis_name == "WET_MASS_TO_USABLE_PROPELLANT_MASS_RATIO":
        ax.set_ylabel('Wet Mass to Usable Propellant Mass Ratio', fontsize=8)
    elif y_axis_name == "CONTRACTION_RATIO":
        ax.set_ylabel('Chamber to Throat Contraction Ratio', fontsize=8)
        
        
    contour_lines = -1        
    if output_name == "JET_THRUST":
        Z = Z * c.N2LBF
        colorbar_label="Jet Thrust [lbf]"
    elif output_name == "MASS_FLOW_RATE":
        colorbar_label="Mass Flow Rate [kg/s]"
    elif output_name == "ISP":
        num_lines = 8
        power = 1/4
        contour_lines = np.max(output_array[output_name]) * 0.995 / (num_lines**power) * np.linspace(1, num_lines, num_lines)**power
        colorbar_label="isp [s]"
    elif output_name == "APOGEE":
        Z = Z * c.M2FT
        altitude_limit = ax.contour(X, Y, Z, levels=[10000], colors='red', linewidths=2)
        ax.clabel(altitude_limit, fmt='%d')
        colorbar_label="Estimated Apogee [ft]"
    elif output_name == "TAKEOFF_TWR":
        colorbar_label="Takeoff TWR"
    elif output_name == "RAIL_EXIT_TWR":
        colorbar_label="Rail Exit TWR"
    elif output_name == "WET_MASS":
        Z = Z * c.KG2LB
        colorbar_label="Wet Rocket Mass [lbm]"
    elif output_name == "BURN_TIME":
        colorbar_label="Burn Time [s]"
    elif output_name == "RAIL_EXIT_VELOCITY":
        colorbar_label="Rail Exit Velocity [m/s]"
    elif output_name == "MAX_ACCELERATION":
        # Z = Z / c.GRAVITY
        colorbar_label="Max Acceleration [G's]"
    elif output_name == "CHAMBER_TEMPERATURE":
        colorbar_label="Chamber Temperature [k]"
    elif output_name == "OXIDIZER_TANK_LENGTH":
        Z = Z * c.M2FT
        colorbar_label="Oxidizer Tank Length [ft]"
    elif output_name == "TOTAL_LENGTH":
        Z = Z * c.M2FT
        colorbar_label="Total Length [ft]"
    else:
        raise ValueError("output name not recognized for plotting")

    # if contour_lines == -1:
    #     ax.contour(X, Y, Z)
    # else:
    #     ax.contour(X, Y, Z, contour_lines)

    
    
    mesh = ax.pcolormesh(X, Y, Z, cmap='Spectral_r')
    # mesh = ax.contourf(X, Y, Z, 100, cmap='Spectral_r')
    # ax.set_title(f"{output_name.title()} of {inputs.constant_inputs['FUEL_NAME'][0].title()} For Different {x_axis_name.title()}s and {y_axis_name.title()}s", fontsize=8)
    ax.set_title(f"{output_name.title()} of {inputs.constant_inputs['FUEL_NAME'][0].title()}", fontsize=12)
    ax.set_facecolor("lightgray")
    plt.colorbar(mesh, label=colorbar_label)

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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def SetupHolyFuckArrays(variable_inputs_array, x_axis_name, y_axis_name, output_name, output_array):
    x = np.array(variable_inputs_array[0, :][y_axis_name]) # what the fuck !
    y = np.array(variable_inputs_array[:, 0][x_axis_name]) # what the fuck !
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