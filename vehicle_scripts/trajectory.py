import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import coding_utils.constants as c


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


ATMOSPHERE_DATA = pd.read_csv("atmosphere.csv")
ATMOSPHERE_DATA = np.array(ATMOSPHERE_DATA)

def calculate_trajectory(
    wet_mass,
    dry_mass,
    full_mass_flow_rate,
    jetThrust,
    tankOD,
    finNumber,
    finHeight,
    exitArea,
    exitPressure,
    burnTime,
    totalLength,
    show_plot,
):
    """
    _summary_

    Parameters
    ----------
    wetMass : float
        Wet mass of the rocket [kg].
    full_mass_flow_rate : float
        Total mass flow rate of the engine [kg/s].
    jetThrust : float
        Engine thrust [N].
    tankOD : float
        Outer diameter of the tank [m].
    finNumber : int
        Number of fins [-].
    finHeight : float
        Fin semi-span [m].
    exitArea : float
        Exit area of the nozzle [m^2].
    exitPressure : float
        Exit pressure of the nozzle [Pa].
    burnTime : float
        Burn time of the engine [s].
    totalLength : float
        Total Length of Rocket [m].
    plots : bool
        Boolean for plotting, 1 = on, 0 = off [-].

    Returns
    -------
    altitude : float
        Final altitude of the rocket [m].
    maxMach : float
        Maximum Mach number of the rocket [-].
    maxAccel : float
        Maximum acceleration of the rocket [m/s^2].
    exitVelo : float
        Exit velocity of the rocket [m/s].
    totalImpulse : float
        Total impulse of the rocket [Ns].
    """
    
    target_TWR = 1.5 
    throttle_to_constant_TWR = True

    # Rocket Properties
    reference_area = (np.pi * (tankOD) ** 2 / 4) + finNumber * finHeight * c.FIN_THICKNESS # [m^2] reference area of the rocket
    current_mass = wet_mass  # [kg] initial mass of the rocket

    cD = 0.5
    ascent_drag_coefficient = cD * (totalLength / 6.35) * (tankOD / 0.203)

    # Initial Conditions
    altitude = c.INDIANA_ALTITUDE  # [m] initial altitude of the rocket
    velocity = 0  # [m/s] initial velocity of the rocket
    initial_acceleration = ((jetThrust + (exitPressure - ATMOSPHERE_DATA[(0, 1)]) * exitArea) - (c.GRAVITY * wet_mass)) / wet_mass  # [m/s] initial acceleration of the rocket
    time = 0  # [s] initial time of the rocket
    dt = 0.05  # [s] time step of the rocket

    # Array Initialization:
    altitude_array = [altitude]
    velocity_array = [velocity]
    acceleration_array = [initial_acceleration]
    # accelArray = [((jetThrust - (c.GRAVITY*wetMass))/wetMass) * 0.1]
    time_array = [time]
    
    totalImpulse = 0  # Initialize total impulse

    acceleration = initial_acceleration
    while (velocity >= 0) or (acceleration > 0):

        altitude_index = int(altitude // 10)  # Divide altitude by 10 to find index

        if altitude_index < 0:
            pressure = ATMOSPHERE_DATA[(0, 1)]
            rho = ATMOSPHERE_DATA[(0, 2)]  # Return first row if below range
        elif altitude_index >= len(ATMOSPHERE_DATA):
            pressure = ATMOSPHERE_DATA[(-1, 1)]
            rho = ATMOSPHERE_DATA[(-1, 2)]  # Return last row if above range
        else:
            pressure = ATMOSPHERE_DATA[(altitude_index, 1)]
            rho = ATMOSPHERE_DATA[(altitude_index, 2)]
        
        # if time < burnTime:
        if current_mass > dry_mass:
            full_thrust = (
                jetThrust + (exitPressure - pressure) * exitArea
            )  # [N] force of thrust, accounting for pressure thrust

            current_weight = c.GRAVITY * current_mass
            constant_TWR_thrust = current_weight * target_TWR

            constant_TWR_mass_flow_rate = full_mass_flow_rate * (constant_TWR_thrust / jetThrust)

            # if (constant_TWR_thrust / jetThrust) > 1:
            #     pass
            
            if throttle_to_constant_TWR and ((constant_TWR_thrust / jetThrust) < 1):
                current_mass = current_mass - constant_TWR_mass_flow_rate * dt  # [kg] mass of the rocket
                current_thrust = (
                    constant_TWR_thrust + (exitPressure - pressure) * exitArea
                )  # [N] force of thrust, accounting for pressure thrust
            else:
                current_mass = current_mass - full_mass_flow_rate * dt  # [kg] mass of the rocket
                current_thrust = (
                    jetThrust + (exitPressure - pressure) * exitArea
                )  # [N] force of thrust, accounting for pressure thrust

            totalImpulse += current_thrust * dt  # Accumulate impulse
            if current_mass < 0:
                raise ValueError("youre a dumbass, CHECK IF TANK DATA IS FAKE OR NOT!!!!!!!!!!!!!")
        else:
            current_thrust = 0  # [N] total thrust of the rocket

        drag_force = (
            0.5 * rho * velocity**2 * ascent_drag_coefficient * reference_area
        )  # [N] force of drag
        weight = c.GRAVITY * current_mass  # [N] downward force due to gravity
        da_TWR = current_thrust / weight  # acceleration equation of motion

        acceleration = (current_thrust - drag_force - weight) / current_mass  # acceleration equation of motion
        if acceleration > 700:
            raise
        acceleration_array.append(acceleration)

        velocity += acceleration * dt  # velocity integration
        velocity_array.append(velocity)

        altitude += velocity * dt  # position integration
        altitude_array.append(altitude)

        time = time + dt  # time is inevitable
        time_array.append(time)
                
    # Find the closest altitude to the TRAILER_RAIL_HEIGHT

    off_the_rail_velocity, off_the_rail_acceleration, off_the_rail_time = 0, 0, 0
    for time_step_index in range(len(altitude_array)):
        if altitude_array[time_step_index] >= c.TRAILER_RAIL_HEIGHT + c.INDIANA_ALTITUDE:
            off_the_rail_velocity = velocity_array[time_step_index]
            off_the_rail_acceleration = acceleration_array[time_step_index]
            off_the_rail_time = (time_step_index/len(altitude_array)) * time_array[-1]
            break
    if altitude_array[-1] * c.M2FT > 200000:
        print(f"time end: {time_array[-1]}")
        
    estimated_apogee = altitude * 0.651 # what the fuck is this for

    if show_plot == True:
        plt.plot(
                 time_array, 
                 np.array(acceleration_array, dtype=float) * c.M2FT,
                 label="Acceleration (any direction) [ft/s^2]",
                 )
      
        plt.plot(
                 time_array, 
                 np.array(velocity_array, dtype=float) * c.M2FT,
                 label="Velocity (any direction) [ft/s]",
                 )
   
        
        plt.plot(time_array,
                 np.array(altitude_array, dtype=float) * c.M2FT * 0.651,
                label="Height [ft]"
                )
        plt.title("Height, Velocity, Acceleration v. Time")
        plt.legend()
        
        plt.ylabel("Height [ft], Velocity (any direction) [ft/s], Acceleration (any direction) [ft/s^2]")
        plt.xlabel("Time [s]")
        
        
        # plot estimated apogee
        # plt.axhline(y=estimated_apogee * c.M2FT, color='r', linestyle='--', label="Estimated Apogee")
        
        # # compare with OpenRocket trajectory
        # OR_df = pd.read_csv('open_rocket_altitude_data.csv', comment='#')
        # OR_time = OR_df.iloc[:, 0]
        # OR_altitude = OR_df.iloc[:, 1]
        # plt.plot(OR_time, OR_altitude + (c.INDIANA_ALTITUDE * c.M2FT))


        plt.grid()
        plt.show()


    max_velocity = velocity_array[np.argmax(np.abs(velocity_array))] # account for positive or negative max
    max_acceleration = acceleration_array[np.argmax(np.abs(acceleration_array))] # account for positive or negative max
    
    
    return (
        float(estimated_apogee),
        max_acceleration,
        max_velocity,
        float(off_the_rail_velocity),
        float(off_the_rail_acceleration),
        float(totalImpulse),
        float(off_the_rail_time),
    )