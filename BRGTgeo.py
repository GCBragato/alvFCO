import math

def dist_2p(x1,y1,x2,y2):
    """Distance between two points"""
    return ((x2-x1)**2+(y2-y1)**2)**(1/2)

def dist_point_line(x,y,A,B,C):
    """Distance from point x,y to line Ax+By+C"""
    return abs(A*x+B*y+C)/((A**2+B**2)**(1/2))

def dist_point_line_inc(x,y,inc):
    """Dist from point x,y to line with inclination in degrees from 0,0"""
    A = math.sin(math.radians(inc))
    B = -math.cos(math.radians(inc))
    C = 0
    return abs(A*x+B*y+C)/((A**2+B**2)**(1/2))

def line_ABC_2p(x1,y1,x2,y2):
    """A B and C of line equation: Ax+By+C=0 from two points"""
    A = y2-y1
    B = x1-x2
    C = A*x1+B*y1
    return A,B,C

def line_ABC_inclination(inc):
    """ABC of general form line equation for line from 0,0 with
    inclination in degrees"""
#    angle = math.radians(angle)
#    x = math.cos(angle)
#    y = math.sin(angle)
#    A = y
#    B = -x
#    C = 0
    return math.sin(math.radians(inc)),-math.cos(math.radians(inc)),0

def line_slope_2p(x1,y1,x2,y2):
    """Slope of a line (tan of its inclination)"""
    return (y2-y1)/(x2-x1)

def line_inclination_slope(slope):
    """Inclination in radians from line slope"""
    return math.atan(slope)
