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
    
    def get_fixed_cost(self):
        """
        This function will return the fixed cost of the drone
        @return float: the fixed cost of the drone
        """
        return self.fixed_cost
    
    def get_cost_km(self):
        """
        This function will return the cost per km of the drone
        @return float: the cost per km of the drone
        """
        return self.cost_km
    
    def get_speed(self):
        """
        This function will return the speed of the drone
        @return float: the speed of the drone
        """
        return self.speed