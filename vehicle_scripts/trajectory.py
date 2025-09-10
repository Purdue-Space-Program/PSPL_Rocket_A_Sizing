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
from numba import njit


ATMOSPHERE_DATA = pd.read_csv("atmosphere.csv")
ATMOSPHERE_DATA = np.array(ATMOSPHERE_DATA)

def calculate_trajectory(
    wetMass,
    mDotTotal,
    jetThrust,
    tankOD,
    finNumber,
    finHeight,
    exitArea,
    exitPressure,
    burnTime,
    totalLength,
    plots,
):
    """
    _summary_

    Parameters
    ----------
    wetMass : float
        Wet mass of the rocket [kg].
    mDotTotal : float
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

    # Rocket Properties
    referenceArea = (np.pi * (tankOD) ** 2 / 4) + finNumber * finHeight * c.FIN_THICKNESS # [m^2] reference area of the rocket
    mass = wetMass  # [kg] initial mass of the rocket

    cD = 0.5
    ascentDragCoeff = cD * (totalLength / 6.35) * (tankOD / 0.203)

    # Initial Conditions
    altitude = c.INDIANA_ALTITUDE  # [m] initial altitude of the rocket
    velocity = 0  # [m/s] initial velocity of the rocket
    time = 0  # [s] initial time of the rocket
    dt = 0.01  # [s] time step of the rocket

    # Array Initialization:
    altitudeArray = np.array(altitude)
    velocityArray = np.array(velocity)
    # accelArray = np.array(((jetThrust - (c.GRAVITY*wetMass))/wetMass) * 0.1)
    accelArray = np.array(0)
    timeArray = np.array(time)
    # print(f"velocity: {velocity}")
    # print(f"velocity >= 0: {velocity >= 0}")

    totalImpulse = 0  # Initialize total impulse

    while velocity >= 0:

        index = int(altitude // 10)  # Divide altitude by 10 to find index

        if index < 0:
            pressure = ATMOSPHERE_DATA[(0, 1)]
            rho = ATMOSPHERE_DATA[(0, 2)]  # Return first row if below range
        elif index >= len(ATMOSPHERE_DATA):
            pressure = ATMOSPHERE_DATA[(-1, 1)]
            rho = ATMOSPHERE_DATA[(-1, 2)]  # Return last row if above range
        else:
            pressure = ATMOSPHERE_DATA[(index, 1)]
            rho = ATMOSPHERE_DATA[(index, 2)]

        # print(f"mass: {mass}, expected mass: {wetMass - mDotTotal*time}, time: {time}")
        
        if time < burnTime:
            mass = mass - mDotTotal * dt  # [kg] mass of the rocket
            thrust = (
                jetThrust + (exitPressure - pressure) * exitArea
            )  # [N] force of thrust, accounting for pressure thrust
            # print(f"jetThrust: {jetThrust}, exitPressure: {exitPressure}, pressure: {pressure}, exitArea: {exitArea}")
            # print(f"ACTUAL thrust: {jetThrust + (exitPressure - pressure) * exitArea}")
            totalImpulse += thrust * dt  # Accumulate impulse
            if mass < 0:
                raise ValueError("youre a dumbass, CHECK IF TANK DATA IS FAKE OR NOT!!!!!!!!!!!!!")
        else:
            thrust = 0  # [N] total thrust of the rocket

        drag = (
            0.5 * rho * velocity**2 * ascentDragCoeff * referenceArea
        )  # [N] force of drag
        gravity_force = c.GRAVITY * mass  # [N] force of gravity

        # print(f"thrust: {thrust}, drag: {drag}, gravity_force: {gravity_force}")
        accel = (thrust - drag - gravity_force) / mass  # acceleration equation of motion
        accelArray = np.append(accelArray, accel)

        velocity += accel * dt  # velocity integration
        velocityArray = np.append(velocityArray, velocity)

        altitude = altitude + velocity * dt  # position integration
        altitudeArray = np.append(altitudeArray, altitude)

        timeArray = np.append(timeArray, time)
        time = time + dt  # time step
        # print(f"velocity: {velocity}")
        # print(f"velocity >= 0: {velocity >= 0}")

    # Find the closest altitude to the TRAILER_RAIL_HEIGHT
    exitVelo, exitAccel = 0, 0
    
    # avoid TWR < 1 rockets
    if altitudeArray.size > 1:
        for i, _ in enumerate(altitudeArray):
            if altitudeArray[i] >= c.TRAILER_RAIL_HEIGHT + c.INDIANA_ALTITUDE:
                exitVelo = velocityArray[i]
                exitAccel = accelArray[i]
                break

    estimated_apogee = altitude * 0.651 # what the fuck is this for

    if plots == True:
        plt.figure(1)
        # plt.plot(timeArray, np.array(altitudeArray, dtype=float) * c.M2FT)
        # plt.title("Height v. Time")
        # plt.ylabel("Height [ft]")
        # plt.xlabel("Time [s]")
        
        # plot estimated apogee
        # plt.axhline(y=estimated_apogee * c.M2FT, color='r', linestyle='--', label="Estimated Apogee")
        
        plt.plot(timeArray, np.array(accelArray, dtype=float))
        plt.title("Acceleration v. Time")
        plt.ylabel("Acceleration [m/s^2]")
        plt.xlabel("Time [s]")
        
        # # compare with OpenRocket trajectory
        # OR_df = pd.read_csv('open_rocket_altitude_data.csv', comment='#')
        # OR_time = OR_df.iloc[:, 0]
        # OR_altitude = OR_df.iloc[:, 1]
        # plt.plot(OR_time, OR_altitude + (c.INDIANA_ALTITUDE * c.M2FT))

        # print(accelArray[np.argmax(np.abs(accelArray))])
        plt.grid()
        plt.show()
    

    return (
        float(estimated_apogee),
        accelArray[np.argmax(np.abs(accelArray))],
        float(exitVelo),
        float(exitAccel),
        float(totalImpulse),
    )