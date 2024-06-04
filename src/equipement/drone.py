"""
! This class will hold the class for drones, it will have the price information and the drone type
"""

class Drone:
    """
    ! This class will hold the class for drones, it will have the price information
    """
    def __init__(self):
        self.fixed_cost = 100
        self.cost_km = 0.01
        self.node_id = 0
        self.speed = 4 #m/s
