import brickpi3
import time
import math
import numpy as np
from FMLController import PIController
class FMLRobot:
    def _init_motors(self):
        self.left_motor = self.BP.PORT_D
        self.right_motor = self.BP.PORT_A
        self.fork_motor = self.BP.PORT_B
        self.BP.set_motor_limits(self.left_motor, dps = 300)
        self.BP.set_motor_limits(self.right_motor, dps = 300)
        self.BP.set_motor_limits(self.fork_motor, dps = 400)

    def _init_sensors(self):
        self.left_sensor = self.BP.PORT_4
        self.right_sensor = self.BP.PORT_3
        self.front_sensor = self.BP.PORT_1
        self.side_sensor = self.BP.PORT_2
        self.BP.set_sensor_type(self.front_sensor, self.BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
        self.BP.set_sensor_type(self.side_sensor, self.BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
        self.BP.set_sensor_type(self.right_sensor, self.BP.SENSOR_TYPE.EV3_COLOR_REFLECTED)
        #self.BP.set_sensor_type(self.BP.PORT_3, self.BP.SENSOR_TYPE.EV3_COLOR_COLOR)
        self.BP.set_sensor_type(self.left_sensor, self.BP.SENSOR_TYPE.EV3_COLOR_COLOR)

    def _init_constants(self):
        self.colors = { 0:"None", 1:"Black", 2:"Blue", 3:"Green", 4:"Yellow", 5:"Red", 6:"White", 7:"Brown" }
    

    # To be implemented in 01 - Kinematik
    def _init_kinematik(self):
        self.wheel_radius = 0.0691/2.0 # m
        self.wheel_distance = 0.165 * 0.91 # m
        self.wheel_circumference = 2*np.pi*self.wheel_radius # m 
        self.gear_ratio = 24.0/8.0 # teeth_wheel/teeth_motor
        
        # global position of the robot within the coordinate system [x,y,phi]
        self.position = np.array([0.0, 0.0, 0.0]) 
        
        # last encoder values are saved in the object (read out the encoder when starting the robot)
        self.encoder_left = self.BP.get_motor_encoder(self.left_motor)
        self.encoder_right= self.BP.get_motor_encoder(self.right_motor)

    # Constructor (gets called on object creation -> FMLRobot())
    def __init__(self):
        self.BP = brickpi3.BrickPi3()
        self._init_motors()
        self._init_sensors()
        self._init_constants()
        time.sleep(4.0)
        self._init_kinematik()


    # context manager entry point
    def __enter__(self):
        return self

    # context manager exit point --> gets called on exit of with block
    def __exit__(self, exc_type, exc_value, traceback):
        # Stop the motors and reset the sensors etc
        self.BP.reset_all()
    
    

    def get_distance_from_encoder(self):
        # read out encoder
        new_encoder_left = self.BP.get_motor_encoder(self.left_motor)
        new_encoder_right = self.BP.get_motor_encoder(self.right_motor)
        # compute the difference
        encdelta_right =  new_encoder_right-self.encoder_right 
        encdelta_left = new_encoder_left- self.encoder_left
        #calculating driven distance
        dis_right = encdelta_right*self.wheel_circumference/(360*self.gear_ratio)
        dis_left = encdelta_left*self.wheel_circumference/(360*self.gear_ratio)
        # update the encoder values 
        self.encoder_left = new_encoder_left
        self.encoder_right = new_encoder_right

        return (dis_left,dis_right) # delta s_r delta s_l
    
    # odometrie
    def update_position(self):
        delta_s_left, delta_s_right = self.get_distance_from_encoder()
        delta_s = (delta_s_right + delta_s_left)/2.0

        delta_x = delta_s * math.cos(self.position[2])
        delta_y = delta_s * math.sin(self.position[2])
        delta_phi = (delta_s_right - delta_s_left) / self.wheel_distance
        
        # update the position
        self.position[0] += delta_x # X
        self.position[1] += delta_y # Y
        self.position[2] += delta_phi # phi
        
    
    def stop(self):
        self.BP.set_motor_dps(self.left_motor, 0)
        self.BP.set_motor_dps(self.right_motor, 0)
       

    # To be implemented in 1.1
    def turn(self,degree):
        # needed motor rotation to achieve movement 
        deg = degree * np.pi * self.gear_ratio * self.wheel_distance / self.wheel_circumference
        deg_right = -deg
        deg_left = deg
        #turning
        self.BP.set_motor_position_relative(self.left_motor, deg_left)
        self.BP.set_motor_position_relative(self.right_motor, deg_right)
        
        # give motors some time to spin
        time.sleep(0.5)

        # read motor veloctiy until zero --> robot stands -> we can return from the function
        while self.BP.get_motor_status(self.left_motor)[3] != 0:
            time.sleep(0.02)

        self.update_position()
        

    # To be implemented in 1.1
    def drive(self, distance):
        # needed motor rotation to achieve movement
        delta_angle = (distance * self.gear_ratio * 360) / self.wheel_circumference
        # add angle to current motor position
        self.BP.set_motor_position_relative(self.left_motor, delta_angle)
        self.BP.set_motor_position_relative(self.right_motor, delta_angle)
        
        # give motors some time to spin
        time.sleep(0.5)
        # read motor veloctiy until zero --> robot stands -> we can return from the function
        while self.BP.get_motor_status(self.left_motor)[3] != 0:
            time.sleep(0.02)

        self.update_position()
        

    # To be implemented in 2.1
    def get_distance_front(self):
        try:
            # read sensor 
            distance = self.BP.get_sensor(self.front_sensor)
            distance = distance + 1 # Distance correction
        except brickpi3.SensorError as error:
            # Default wert
            distance = -1 # defaults to None
            print(f"Error during get_distance_front(): {error}")
    
        return distance
    
    def get_distance_right(self):
        try:
            # read sensor 
            distance = self.BP.get_sensor(self.right_sensor)
            distance = distance + 1 # Distance correction
        except brickpi3.SensorError as error:
            # Default wert
            distance = -1 # defaults to None
            print(f"Error during get_distance_front(): {error}")

        return distance

    
    # To be implemented in 2.1
    def get_color_left(self):
        try:
            color = self.BP.get_sensor(self.left_sensor) # Read in sensor
        # If brickpy sensor throws error set default value
        except brickpi3.SensorError as error:
            color = None # Default Value and print error
            print(f"Error during get_color_left(): {error}")
    
        return self.colors[color]
    
    # To be implemented in 2.1    
    def get_color_right(self):
        try:
            color = self.BP.get_sensor(self.right_sensor) # Read in sensor
        except brickpi3.SensorError as error:
            color = None 
            print(f"Error during get_color_right(): {error}")
    
        return self.colors[color]

     
    ## Actor stuff

    # To be implemented in 2.3g
    def lift_fork(self):
        self.move_fork(1080)


     # To be implemented in 2.3
    def drop_fork(self):
        self.move_fork(-1080)

    # to be implemented in 2.3
    def move_fork(self,degrees):
        self.BP.set_motor_position_relative(self.fork_motor, degrees) # Move fork motor
        # wait on the motor and check if it finished moving
        time.sleep(0.4)
        # read motor veloctiy until zero --> fork lift at position
        while self.BP.get_motor_status(self.fork_motor)[3] != 0:
            time.sleep(0.02)



    ## Higher level functions

    ## Followers:
    def follower_line(self, velocity, controller):
        while True:
            try:
                # Get reflected light from the right sensor for line tracking
                current_sensor_value = self.BP.get_sensor(self.right_sensor)
                
                # Get the color detected by the left sensor (for checking ground)
                ground_color = self.BP.get_sensor(self.left_sensor)
                
                if not (ground_color == 0 or ground_color == 1 or ground_color == 6):
                    print(f"Non-black/white ground detected (color code: {ground_color}). Stopping.")
                    self.stop()
                    break

                # Check if an obstacle is detected by the front distance sensor
                front_distance = self.get_distance_front()
                if front_distance != -1 and front_distance < 10:  # Stop if the obstacle is too close
                    print("Obstacle detected. Stopping.")
                    self.stop()
                    self.drop_fork()
                    time.sleep(0.5)
                    self.lift_fork()
                    time.sleep(0.5)
                    break

                # Calculate steering using the Controller algorithm
                u = controller.get_u(current_sensor_value)
                
                # Limit u to 500
                if velocity + abs(u) > 500:
                    if u >= 0:
                        u = 500 - velocity
                    else:
                        u = velocity - 500

                # Run motors with correction
                if u >= 0:
                    self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
                    self.BP.set_motor_dps(self.left_motor, velocity + abs(u))
                else:
                    self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
                    self.BP.set_motor_dps(self.left_motor, velocity - abs(u))
                
                time.sleep(0.01)

            except brickpi3.SensorError as error:
                print(f"Error during sensor reading: {error}")
                continue

        
    
    def follower_distance(self, desired_distance, controller, velocity=200):
        avoiding_obstacle = False
        initial_right_distance = None

        while True:
            try:
                # Get reflected light from the right sensor for line tracking
                current_sensor_value = self.BP.get_sensor(self.right_sensor)

                # Get the color detected by the left sensor (for line detection)
                ground_color = self.BP.get_sensor(self.left_sensor)

                # Get front and right distance values
                front_distance = self.get_distance_front() 
                right_distance = self.get_distance_right()

                # Start obstacle avoidance if the front sensor detects an obstacle within the desired distance
                if front_distance != -1 and front_distance < desired_distance and not avoiding_obstacle:
                    print("Obstacle detected in front. Starting obstacle avoidance.")
                    avoiding_obstacle = True
                    self.turn(-90)  # Turn 90 degrees to the left
                    self.drive(0.3)
                    continue  # Re-check the sensors after this movement

                if avoiding_obstacle:
                    # Adjust the right sensor detection threshold here by using a multiplier for sensitivity
                    adjusted_distance = desired_distance * 2  # Increase detection threshold by 50%

                    # Move forward until the right sensor no longer detects the obstacle within the adjusted distance
                    if right_distance > adjusted_distance or right_distance == -1:
                        print("Obstacle no longer detected on the right. Starting slow left turn.")

                        # Start turning slowly left until the obstacle is detected again
                        while right_distance > adjusted_distance or right_distance == -1:
                            self.BP.set_motor_dps(self.left_motor, 50)  # Slow left turn
                            self.BP.set_motor_dps(self.right_motor, -50)
                            right_distance = self.get_distance_right()
                            time.sleep(0.05)

                        print("Obstacle detected again on the right. Moving forward.")
                        self.BP.set_motor_dps(self.left_motor, velocity)
                        self.BP.set_motor_dps(self.right_motor, velocity)

                    # Check if the black line is detected and return to line tracking mode
                    if ground_color == 1:  # 1 is Black
                        print("Black line detected. Returning to line tracking mode.")
                        avoiding_obstacle = False

                if not avoiding_obstacle:
                    # Normal line following using the PI controller
                    u = controller.get_u(current_sensor_value)

                    # Limit u to 500
                    if velocity + abs(u) > 500:
                        if u >= 0:
                            u = 500 - velocity
                        else:
                            u = velocity - 500

                    # Run motors with correction for line following
                    if u >= 0:
                        self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
                        self.BP.set_motor_dps(self.left_motor, velocity + abs(u))
                    else:
                        self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
                        self.BP.set_motor_dps(self.left_motor, velocity - abs(u))

                time.sleep(0.01)

            except brickpi3.SensorError as error:
                print(f"Error during sensor reading: {error}")
                continue

   

    # read and display the current voltages
    def print_battery_status(self):
        print("Battery voltage: %6.3f  9v voltage: %6.3f  5v voltage: %6.3f  3.3v voltage: %6.3f" % (self.BP.get_voltage_battery(), self.BP.get_voltage_9v(), self.BP.get_voltage_5v(), self.BP.get_voltage_3v3())) 
