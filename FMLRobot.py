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
        self.wheel_distance = 0.165 # m
        self.wheel_circumference = 2*np.pi*self.wheel_radius # m 
        self.gear_ratio = 24.0/8.0 # teeth_wheel/teeth_motor
        
        # global position of the robot within the coordinate system [x,y,phi]
        self.position = np.array([0,0,0]) 
        
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
        dis_right = None
        dis_left = None
        # update the encoder values 
        self.encoder_left = None
        self.encoder_right = None

        return (dis_left,dis_right) # delta s_r delta s_l
    
    # odometrie
    def update_position(self):
        delta_s_left, delta_s_right = self.get_distance_from_encoder()
        delta_s = None

        delta_x = None
        delta_y = None
        delta_phi = None
        
        # update the position
        self.position[0]= None # X
        self.position[1]= None # Y
        self.position[2]= None # phi
        
    
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
        

    # To be implemented in 2.1
    def get_distance_front(self):
        try:
            # read sensor 
            distance = self.BP.get_sensor(self.front_sensor)
        except brickpi3.SensorError as error:
            # Default wert
            distance = -1 # defaults to None
            print(f"Error during get_distance_front(): {error}")
    
        return distance
    
    # To be implemented in 2.1
    def get_color_left(self):
        try:
            color = None #TODO Read in sensor
        # If brickpy sensor throws error set default value
        except brickpi3.SensorError as error:
            color = None # Default Value and print error
            print(f"Error during get_color_left(): {error}")
    
        return self.colors[color]
    
    # To be implemented in 2.1    
    def get_color_right(self):
        try:
            color = None #TODO Read in sensor
        except brickpi3.SensorError as error:
            color = None 
            print(f"Error during get_color_right(): {error}")
    
        return self.colors[color]

     
    ## Actor stuff

    # To be implemented in 2.3g
    def lift_fork(self):
        self.move_fork(1)


     # To be implemented in 2.3
    def drop_fork(self):
        self.move_fork(-1)

    # to be implemented in 2.3
    def move_fork(self,degrees):
        # TODO Move fork motor
        # wait on the motor and check if it finished moving
        time.sleep(0.4)
        # read motor veloctiy until zero --> fork lift at position
        while self.BP.get_motor_status(self.fork_motor)[3] != 0:
            time.sleep(0.02)



    ## Higher level functions

    ## Followers:
    def follower_line(self, velocity, controller):
        while True:
            # TODO Get reflected light of right sensor
            current_sensor_value = None
            # TODO Calculate steering using Controller algorithm
            u = 0
            
            # Limit u to 500
            if velocity + abs(u) > 500:
                if u >= 0:
                    u = 500 - velocity
                else:
                    u = velocity - 500

            # Run motors with correction
            if u >= 0:
                self.BP.set_motor_dps(self.right_motor,velocity - abs(u))
                self.BP.set_motor_dps(self.left_motor,velocity + abs(u))
            else:
                self.BP.set_motor_dps(self.right_motor,velocity + abs(u))
                self.BP.set_motor_dps(self.left_motor,velocity - abs(u))
            
            time.sleep(0.01)
        
    
    def follower_distance(self, velocity, controller, colors_to_stop=[]):
        pass
    

    # read and display the current voltages
    def print_battery_status(self):
        print("Battery voltage: %6.3f  9v voltage: %6.3f  5v voltage: %6.3f  3.3v voltage: %6.3f" % (self.BP.get_voltage_battery(), self.BP.get_voltage_9v(), self.BP.get_voltage_5v(), self.BP.get_voltage_3v3())) 

       
        
