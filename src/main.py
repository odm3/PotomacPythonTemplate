# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       oscarmccullough                                              #
# 	Created:      Thu Sep 15 2022                                              #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# define threewireport, makes defining threewireports easier
ThreeWirePort = brain.three_wire_port

#toggle variable example 
pneumaticsToggle = False
# define all motors and devices here

# motors example
# name = Motor(PORT, GearSetting, reversed)
frontLeft = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
backLeft = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
frontRight = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
backRight = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)

# use motor_groups to group together motors on the same side
leftDrive = MotorGroup(frontLeft, backLeft)
rightDrive = MotorGroup(frontRight, backRight)

# controller example - controller = Controller(ControllerType.PRIMARY | PARTNER )
controller = Controller(ControllerType.PRIMARY)

# inertial sensor example - imu = Inertial(PORT)
imu = Inertial(Ports.PORT15)

# pneumatics example pneu1 = Pneumatics(ThreeWirePort)
pneu1 = Pneumatics(ThreeWirePort.a)

# RotationSensor Example rot1 = Rotation(PORT)
rot1 = Rotation(Ports.PORT12)

# function callbacks - useful for button.pressed
def toggle_pneumatics(): 
    global pneumaticsToggle
    pneumaticsToggle = not pneumaticsToggle

# define callbacks for when a button is pressed
controller.buttonL1.pressed(toggle_pneumatics)

brain.screen.print("Hello V5\n")

# When using an inertial sensor, you need to calibrate it
def imu_calibrate():
    global imu
    #start calibrating
    imu.calibrate()
    while imu.is_calibrating():
        wait(50, MSEC)

# pre-autonomous function - this runs before a match starts and is where sensors are initialized, rezeroed, etc. 
def pre_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Entering Pre-Auton\n")
    # Call our IMU Sensor Calibration
    imu_calibrate()

# autonomous function - this runs your autonomous code, the 15 seconds at the start of the match 
def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Autonomous...\n")

# usercontrol - this runs your driver code, or the last 1:45 of the match
def user_control():
    brain.screen.clear_screen()

    # add a while loop to ensure everything stays running 
    while True:

        # Tank Drive, independent control of left and right side
        # Axis 3 - Y-Axis on Left Joystick, Axis 2 - Y-Axis on Right Joystick

        leftDrive.spin(FORWARD, controller.axis3.position(), VelocityUnits.PERCENT)
        rightDrive.spin(FORWARD, controller.axis2.position(), VelocityUnits.PERCENT)

        # Arcade Drive - Y-Axis controls vertical movement, X-Axis controls horizontal
        # Axis 4 - X-Axis on Left Joystick, Axis 1 - X-Axis on Right Joystick
        # define variables for vertical and horizontal movement 
        # uncomment these lines if you want to use arcade drive
        # vertical = controller.axis3.position()
        # horizontal = controller.axis1.position()
        # leftDrive.spin(FORWARD, vertical - horizontal, VelocityUnits.PERCENT)
        # rightDrive.spin(FORWARD, vertical + horizontal, VelocityUnits.PERCENT)

        # running pneumatics with toggle and callback
        if pneumaticsToggle:
            pneu1.open
        else:
            pneu1.close
        wait(10, MSEC)

# Define competition control instance
comp = Competition(user_control, autonomous)
pre_autonomous()




        
