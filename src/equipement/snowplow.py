"""
! This file contatins the class of snowplows, it has the price information and the snowplow type
"""

class Snowplow:
    """
    ! This class will hold the price info and the type of snowplow
    """
    def __init__(self, type : int):
        """
        ! This function will initialize the class
        @param type: int: the type of snowplow, can be 1 or 2
        """
        self.type = type
        self.node_id = 0
        if type == 1:
            self.fixed_cost = 500
            self.cost_km = 1.1
            self.cost_first_8_hours = 1.1
            self.cost_after_8_hours = 1.3
            self.speed = 10
        elif type == 2:
            self.fixed_cost = 800
            self.cost_km = 1.3
            self.cost_first_8_hours = 1.3
            self.cost_after_8_hours = 1.5
            self.speed = 20
        else:
            raise ValueError("Usage error: snowplow type must be 1 or 2")