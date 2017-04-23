class elevator:
    
    def __init__(self, name, direction, current_floor, capaticy, num_customer):
        
        self.name = name
        self.direction = direction
        self.current_floor = current_floor
        self.capaticy = capaticy
        self.num_customer = num_customer
    
    def move(self):
        
        if self.direction == "up":
            self.current_floor += 1
        elif self.direction == "down":
            self.current_floor -= 1
        else:
            pass