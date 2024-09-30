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
        pass
               
    # return the perceentage of greenish pixels in the current camera picture (takes images -> processes it -> returns the result)
    def get_green_percentage(self):
        pass

    # returns a list of shapes recognized in the picture. The image is provided via a path saved to harddisk (mainly because image resultion is higher this way)
    # (load picture -> process it -> generate list of shapes -> return them)
    def get_shapes_on_image(self,path_to_image):
        pass

    # Return the offset of the centerpoint of the barcode relative to the center of the camera view. 
    # But here its really open to you what you want to control with the P-PI Controller. 
    # Remind yourself that you can get the position of a barcode also from the Scanner() lib.
    def get_qr_position(self):
        pass