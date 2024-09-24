import time
import numpy as np

class PController:
    def __init__(self, kp, target_value):
        self.kp = kp
        self.target_value = target_value
    
    def get_u(self,current_value):
        error = None # Compute error
        u = None # compute u
        return u


class PIController:
    def __init__(self, kp,ki, target_value):
        self.kp = kp
        self.ki = ki
        self.target_value = target_value
        self.last_call= time.time()
        self.dt =0
        self.integral =0
    
    def get_u(self,current_value):
        now = time.time()
        self.dt = self.last_call - now
        error = None # compute error 
        self.integral += None # Update integral value
        u = None # Compute U from P and I portion
        # Update time for next call
        self.last_call = now
        return u