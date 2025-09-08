import numpy as np
import matplotlib.pyplot as plt
import coding_utils.constants as c
import inputs

def PlotColorMaps(x_axis_name, y_axis_name, variable_inputs_array, output_names, output_array):
    num_outputs = len(output_names)
    
    if num_outputs == 1:
        axes = [axes]  # make it iterable
        
    # Create a 2x2 grid
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))  

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
    if y_axis_name == "CHAMBER_PRESSURE":
        Y = Y * c.PA2PSI
        ax.set_ylabel('Chamber Pressure [psi]', fontsize=8)
        
    if output_name == "JET_THRUST":
        Z = Z * c.N2LBF
        colorbar_label="Jet Thrust [lbf]"
        ax.contour(X, Y, Z)
    elif output_name == "MASS_FLOW_RATE":
        colorbar_label="Mass Flow Rate [kg/s]"
        ax.contour(X, Y, Z)
    elif output_name == "ISP":
        num_lines = 8
        power = 1/4
        contour_lines = np.max(output_array[output_name]) * 0.995 / (num_lines**power) * np.linspace(1, num_lines, num_lines)**power

        ax.contour(X, Y, Z, contour_lines)
        colorbar_label="isp [s]"
    elif output_name == "APOGEE":
        Z = Z * c.M2FT
        ax.contour(X, Y, Z)
        altitude_limit = plt.contour(X, Y, Z, levels=[10000], colors='red', linewidths=2)
        ax.clabel(altitude_limit, fmt='%d')
        colorbar_label="Estimated Apogee [ft]"
    
    
    
    mesh = ax.pcolormesh(X, Y, Z, cmap='Spectral_r')
    # plt.contourf(X, Y, Z, 100, cmap='Spectral_r')
    ax.set_title(f"{output_name.title()} of {inputs.constant_inputs['FUEL_NAME'][0].title()} For Different {x_axis_name.title()}s and {y_axis_name.title()}s", fontsize=13)
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
        plt.xlabel('OF Ratio', fontsize=14)
        plt.ylabel('Chamber Pressure [psi]', fontsize=14)
        # plt.title(f"ISP of {inputs.constant_inputs['FUEL_NAME'].item().title()} For Different {x_axis} and OF Ratios", fontsize=20)
        plt.colorbar(mesh, label=color_variable_label)
        
    plt.draw()
    plt.pause(0.5)