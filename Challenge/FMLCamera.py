from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import cv2
import zbar
import time

class FMLCamera:

    def __init__(self):
        self.resolution = (800,400) # rows x columns
        self._pi_camera = PiCamera()
        self._pi_camera.framerate = 10
        self._pi_camera.resolution=self.resolution
        # make shure camera is up and awake
        time.sleep(2)

    
    # Destructor (gets called once the object is destroyed)
    def __del__(self):
        # Frees ressources connected to the camera
        self._pi_camera.close() 
    
    # Return a array as a image just a in 06-perception
    def get_image_array(self):
        raw_capture = PiRGBArray(self._pi_camera, size=self.resolution)
        self._pi_camera.capture(raw_capture, format="bgr")
        return raw_capture.array

    # saves a image to disk - probably usefull for the shape recognition.
    def save_to_disk(self, path_to_image):
        self._pi_camera.capture(path_to_image)



    # the following function only provide hints on what could be done using the FMLCamera class. 
    # Feel free to implement things differently. 

    # return the parsed barcode thats directly in front of the roboter (takes image -> processes it -> return the result)
    def get_barcode(self):
        # Capture the current frame from the camera
        frame = self.get_image_array()

        # Create a QRCodeDetector object
        qr_detector = cv2.QRCodeDetector()

        # Detect and decode the QR code in the frame
        value, points, _ = qr_detector.detectAndDecode(frame)

        # Check if a QR code was detected
        if points is not None:
            # If a QR code is detected, print its value
            # print(f"QR Code detected: {value}")
            return value
        else:
            print("No QR Code detected")
            return None
               
    # return the perceentage of greenish pixels in the current camera picture (takes images -> processes it -> returns the result)
    def get_green_percentage(self):
        # Capture the current frame from the camera
        frame = self.get_image_array()

        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the range for green color in HSV
        lower_green = np.array([35, 100, 100])
        upper_green = np.array([85, 255, 255])

        # Create a binary mask where green colors are detected
        green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)

        # Calculate the percentage of green pixels in the image
        green_pixels = np.count_nonzero(green_mask)
        total_pixels = green_mask.size
        green_percentage = (green_pixels / total_pixels) * 100

        return green_percentage

    # returns a list of shapes recognized in the picture. The image is provided via a path saved to harddisk (mainly because image resultion is higher this way)
    # (load picture -> process it -> generate list of shapes -> return them)
    def get_shapes_on_image(self,path_to_image):
        pass

    # Return the offset of the centerpoint of the barcode relative to the center of the camera view. 
    # But here its really open to you what you want to control with the P-PI Controller. 
    # Remind yourself that you can get the position of a barcode also from the Scanner() lib.
    def get_qr_position(self):
        # Capture the current frame from the camera
        frame = self.get_image_array()

        # Print the shape of the frame to understand its dimensions
        frame_height, frame_width, _ = frame.shape
        # print(f"Frame dimensions: width = {frame_width}, height = {frame_height}")

        # Calculate the frame center based on the dimensions
        frame_center_x = frame_width / 2
        frame_center_y = frame_height / 2
        # print(f"Frame center: x = {frame_center_x}, y = {frame_center_y}")

        # Create a QRCodeDetector object
        qr_detector = cv2.QRCodeDetector()

        # Detect and decode the QR code in the frame
        value, points, _ = qr_detector.detectAndDecode(frame)

        # Check if a QR code was detected
        if points is not None:
            # Calculate the center of the QR code bounding box
            x_coords = [p[0] for p in points[0]]
            y_coords = [p[1] for p in points[0]]
            qr_center_x = sum(x_coords) / len(x_coords)
            qr_center_y = sum(y_coords) / len(y_coords)

            # Calculate the offset of the QR code's center from the frame's center
            x_offset = qr_center_x - frame_center_x
            y_offset = qr_center_y - frame_center_y

            print(f"QR Code center: ({qr_center_x}, {qr_center_y})")
            print(f"QR Code offset from center: x = {x_offset}, y = {y_offset}")

            return x_offset, y_offset
        else:
            print("No QR Code detected in the frame.")
            return None
