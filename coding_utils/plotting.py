import numpy as np
import matplotlib.pyplot as plt
import coding_utils.constants as c




def SetupArrays(variable_inputs_array, color_variable_map):
    x = np.array(variable_inputs_array[0, :]["CHAMBER_PRESSURE"]) * c.PA2PSI
    y = np.array(variable_inputs_array[:, 0]["OF_RATIO"])
    z = np.array(color_variable_map)

    Y, X = np.meshgrid(x, y) # I don't know why you have to swap X and Y but you do
    Z = z.reshape(len(x), len(y))
    
    return (X, Y, Z)


def PlotColorMap(X, Y, Z, color_variable_map, color_variable_label="this dumbass did not change the label"):
    num_lines = 8
    power = 1/4
    contour_lines = max(color_variable_map) * 0.995 / (num_lines**power) * np.linspace(1, num_lines, num_lines)**power
    plt.contour(X, Y, Z, contour_lines)
    # plt.contour(X, Y, Z)
    
    plt.pcolormesh(X, Y, Z, cmap='Spectral_r')
    # plt.contourf(X, Y, Z, 100, cmap='Spectral_r')
    
    plt.colorbar(label=color_variable_label)

    plt.xlabel('OF Ratio', fontsize=14)
    plt.ylabel('Chamber Pressure [psi]', fontsize=14)
    # plt.title(f"ISP of {constant_inputs_array["FUEL_NAME"].item().title()} For Different Chamber Pressures and OF Ratios", fontsize=18)
    plt.show()


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
        # plt.title(f"ISP of {constant_inputs_array['FUEL_NAME'].item().title()} For Different Chamber Pressures and OF Ratios", fontsize=20)
        plt.colorbar(mesh, label=color_variable_label)
        
    plt.draw()
    plt.pause(0.5)