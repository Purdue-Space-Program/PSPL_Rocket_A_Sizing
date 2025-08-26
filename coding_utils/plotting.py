import numpy as np
import matplotlib.pyplot as plt

def PlotColorMap(variable_inputs_array, constant_inputs_array, color_variable_map, color_variable_label="this dumbass did not change the label"):

    x = np.array(variable_inputs_array[0, :]["CHAMBER_PRESSURE"])
    y = np.array(variable_inputs_array[:, 0]["OF_RATIO"])
    z = np.array(color_variable_map)

    Y, X = np.meshgrid(x, y) # I don't know why you have to swap X and Y but you do
    Z = z.reshape(len(x), len(y))

    num_lines = 8
    power = 1/4
    contour_lines = max(color_variable_map) * 0.995 / (num_lines**power) * np.linspace(1, num_lines, num_lines)**power
    plt.contour(X, Y, Z, contour_lines)
    
    plt.pcolormesh(X, Y, Z, cmap='Spectral_r')
    # plt.contourf(X, Y, Z, 100, cmap='Spectral_r')
    
    plt.colorbar(label=color_variable_label)

    plt.xlabel('OF Ratio', fontsize=14)
    plt.ylabel('Chamber Pressure [psi]', fontsize=14)
    plt.title(f"ISP of {constant_inputs_array['FUEL_NAME'].item().title()} For Different Chamber Pressures and OF Ratios", fontsize=20)
    plt.show()



x = np.array(variable_inputs_array[0, :]["CHAMBER_PRESSURE"])
y = np.array(variable_inputs_array[:, 0]["OF_RATIO"])
z = np.array(isp_map)

Y, X = np.meshgrid(x, y) # I don't know why you have to swap X and Y but you do
Z = z.reshape(len(x), len(y))
plt.pcolormesh(X, Y, Z, cmap='Spectral_r')
if count == 0:
    plt.ion()
    fig, ax = plt.subplots()
    mesh = ax.pcolormesh(X, Y, Z, cmap='Spectral_r')
    plt.xlabel('OF Ratio', fontsize=14)
    plt.ylabel('Chamber Pressure [psi]', fontsize=14)
    plt.title(f"ISP of {constant_inputs_array['FUEL_NAME'].item().title()} For Different Chamber Pressures and OF Ratios", fontsize=20)
    plt.colorbar(mesh, label='isp [s]')
else:
    mesh.set_array(Z.ravel())
    mesh.set_clim(np.min(Z), np.max(Z))
plt.draw()
plt.pause(0.05)