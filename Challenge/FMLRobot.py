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
    def drive(self, distance, velocity):

        # self.BP.set_motor_dps(self.right_motor, velocity)
        # self.BP.set_motor_dps(self.left_motor, velocity)

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
        self.stop()
        self.update_position()
        
    def drive_stop_at_color(self, velocity):

        self.BP.set_motor_dps(self.right_motor, velocity)
        self.BP.set_motor_dps(self.left_motor, velocity)

        while True:
            # needed motor rotation to achieve movement
            distance = 1
            delta_angle = (distance * self.gear_ratio * 360) / self.wheel_circumference
            # add angle to current motor position
            self.BP.set_motor_position_relative(self.left_motor, delta_angle)
            self.BP.set_motor_position_relative(self.right_motor, delta_angle)

            ground_cam_left = self.get_ground_cam_left()

            if not (ground_cam_left == 0 or ground_cam_left == 1 or ground_cam_left == 6):
                # print(f"Non-black/white ground detected (color code: {ground_cam_left}). Stopping.")
                self.stop()
                break
            
            # give motors some time to spin
            time.sleep(0.1)
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
    
    def get_distance_side(self):
        try:
            # read sensor 
            distance = self.BP.get_sensor(self.side_sensor)
            distance = distance + 1 # Distance correction
        except brickpi3.SensorError as error:
            # Default wert
            distance = -1 # defaults to None
            print(f"Error during get_distance_front(): {error}")

        return distance

    
    # # To be implemented in 2.1
    # def get_ground_cam_left(self):
    #     try:
    #         color = self.BP.get_sensor(self.left_sensor) # Read in sensor
    #     # If brickpy sensor throws error set default value
    #     except brickpi3.SensorError as error:
    #         color = None # Default Value and print error
    #         print(f"Error during get_ground_cam_left(): {error}")
    
    #     return self.colors[color]

    def get_ground_cam_left(self):
            consecutive_color_count = 0
            stable_color = None

            # Initialize with a reasonable limit for number of consecutive reads
            stability_threshold = 20

            try:
                # Continuously read the sensor until the stability threshold is met
                while consecutive_color_count < stability_threshold:
                    # Read the sensor value
                    color = self.BP.get_sensor(self.left_sensor)

                    # Map the color index to its name
                    color_name = self.colors.get(color, 'unknown')

                    # Check if the stable color is the same as the currently read color
                    if stable_color == color_name:
                        consecutive_color_count += 1
                    else:
                        # Reset counter and update stable color if it's different
                        stable_color = color_name
                        consecutive_color_count = 1

            except brickpi3.SensorError as error:
                # Handle sensor error, assign 'unknown' as default
                stable_color = 'unknown'
                print(f"Error during get_ground_cam_left(): {error}")

            # Return the stable color
            return stable_color
    
    # To be implemented in 2.1    
    def get_ground_cam_right(self):
        try:
            color = self.BP.get_sensor(self.right_sensor) # Read in sensor
        except brickpi3.SensorError as error:
            color = None 
            print(f"Error during get_ground_cam_right(): {error}")
    
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
        print("Line following started")

        # Record the starting time
        start_time = time.time()

        while True:
            try:
                # Get the elapsed time since the function started
                elapsed_time = time.time() - start_time

                # Get reflected light from the right sensor for line tracking
                ground_cam_right = self.BP.get_sensor(self.right_sensor)
                
                # Only check the ground color condition after 1 second has passed
                if elapsed_time > 0.7:

                    velocity = 200
                    ground_cam_left = self.get_ground_cam_left()

                    # Stop if a specific ground color is detected
                    if ground_cam_left in ["Blue", "Green", "Yellow", "Red"]:
                        self.stop()
                        print(f"Line following ended because color: {ground_cam_left} detected.")
                        break

                # Calculate steering using the Controller algorithm
                u = controller.get_u(ground_cam_right)

                # Limit u to 500
                if velocity + abs(u) > 500:
                    u = 500 - velocity if u >= 0 else velocity - 500

                # Run motors with correction
                if u >= 0:
                    self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
                    self.BP.set_motor_dps(self.left_motor, velocity + abs(u))
                else:
                    self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
                    self.BP.set_motor_dps(self.left_motor, velocity - abs(u))

                time.sleep(0.1)

            except brickpi3.SensorError as error:
                print(f"Error during sensor reading: {error}")
                continue

    def follower_line_short_distance(self, velocity, controller):
        print("Line following started")

        # Record the starting time

        while True:
            try:
                # Get the elapsed time since the function started

                # Get reflected light from the right sensor for line tracking
                ground_cam_right = self.BP.get_sensor(self.right_sensor)
                
                # Only check the ground color condition after 1 second has passed

                velocity = 200
                ground_cam_left = self.get_ground_cam_left()

                # Stop if a specific ground color is detected
                if ground_cam_left in ["Blue", "Green", "Yellow", "Red"]:
                    self.stop()
                    print(f"Line following ended because color: {ground_cam_left} detected.")
                    break

                # Calculate steering using the Controller algorithm
                u = controller.get_u(ground_cam_right)

                # Limit u to 500
                if velocity + abs(u) > 500:
                    u = 500 - velocity if u >= 0 else velocity - 500

                # Run motors with correction
                if u >= 0:
                    self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
                    self.BP.set_motor_dps(self.left_motor, velocity + abs(u))
                else:
                    self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
                    self.BP.set_motor_dps(self.left_motor, velocity - abs(u))

                time.sleep(0.1)

            except brickpi3.SensorError as error:
                print(f"Error during sensor reading: {error}")
                continue


        
    def bypass_obstacle(self, controller_line_following, controller_bypass_obstacle, velocity):
        # Step 1: Follow the line until an obstacle is detected 12cm in front
        # time.sleep(0.01)
        # ground_cam_left = self.get_ground_cam_left()
        # print(ground_cam_left)
        # if ground_cam_left == "Red" or ground_cam_left == "Yellow":
        #     break
        while True:
            print("Starting line tracking until obstacle is detected.")
            while True:
                try:
                    # Track the black line using the follower_line logic until an obstacle is detected
                    front_distance = self.get_distance_front()
                    ground_cam_right = self.BP.get_sensor(self.right_sensor)
                    ground_cam_left = self.get_ground_cam_left()

                    if front_distance != -1 and front_distance <= 12:  # Stop if an obstacle is detected 12cm ahead
                        print("Obstacle detected 12cm ahead. Waiting for 10 seconds")
                        self.stop()
                        time.sleep(10)

                    if front_distance != -1 and front_distance <= 12:  # Stop if an obstacle is detected 12cm ahead
                        print("Obstacle detected 12cm ahead. Preparing to bypass.")
                        self.stop()
                        break

                    u = controller_line_following.get_u(ground_cam_right)
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

            # Step 2: Turn -60 degrees and go straight until the side distance is exactly 15cm
            print("Turning -60 degrees.")
            self.turn(-60)
            print("Going straight until side distance is 15cm.")
            while True:
                try:
                    # Move forward until the side distance is exactly 15cm
                    self.BP.set_motor_dps(self.left_motor, velocity)
                    self.BP.set_motor_dps(self.right_motor, velocity)

                    side_distance = self.get_distance_side()
                    if side_distance != -1 and abs(side_distance - 15) <= 1:  # Allow for slight error in measurement
                        print(f"Side distance is now 15cm. Stopping.")
                        self.stop()
                        break

                    time.sleep(0.01)

                except brickpi3.SensorError as error:
                    print(f"Error during sensor reading: {error}")
                    continue

            # Step 3: Circumvent the obstacle using the current behavior until the black line is detected
            print("Starting obstacle avoidance by maintaining a constant side distance.")
            while True:
                try:
                    side_distance = self.get_distance_side()

                    ground_cam_right = self.BP.get_sensor(self.right_sensor)
                    ground_cam_left = self.get_ground_cam_left()


                    # print('right: {}, left: {}'.format(ground_cam_right, ground_cam_left))
                    

                    # Check if the ground color is black to transition back to line following
                    if ground_cam_left == "Black":
                        print("Black line detected. Resuming line following.")
                        self.stop()
                        break


                    # Use side distance to control movement around the obstacle
                    u = controller_bypass_obstacle.get_u(side_distance)
                    # Limit u to 500
                    if velocity + abs(u) > 500:
                        if u >= 0:
                            u = 500 - velocity
                        else:
                            u = velocity - 500

                    # Run motors with correction
                    if u >= 0:
                        self.BP.set_motor_dps(self.right_motor, velocity + abs(u))
                        self.BP.set_motor_dps(self.left_motor, velocity - abs(u))
                    else:
                        self.BP.set_motor_dps(self.right_motor, velocity - abs(u))
                        self.BP.set_motor_dps(self.left_motor, velocity + abs(u))

                    time.sleep(0.01)


                except brickpi3.SensorError as error:
                    print(f"Error during sensor reading: {error}")
                    continue
            break

    def is_integer(self, x):
        try:
            int(x)
            return True
        except:
            return False

    # read and display the current voltages
    def print_battery_status(self):
        print("Battery voltage: %6.3f  9v voltage: %6.3f  5v voltage: %6.3f  3.3v voltage: %6.3f" % (self.BP.get_voltage_battery(), self.BP.get_voltage_9v(), self.BP.get_voltage_5v(), self.BP.get_voltage_3v3())) 


