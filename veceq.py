class VectorEquation:
    def __init__(self, start, direction):
        self.x_m = direction[1]
        self.x_b = start[0]
        
        self.y_m = direction[0]
        self.y_b = start[1]
        
    def calcPosition(self, t):
        x = self.x_m * t + self.x_b
        y = self.y_m * t + self.y_b
        
        return (x, y)
    
    def checkPoint(self, x, y):
        t1 = x - self.x_b
        t2 = y - self.y_b
        if self.x_m != 0:
            t1 = int(t1 / self.x_m)
        if self.y_m != 0:
            t2 = int(t2 / self.y_m)
        
        return t1 == t2