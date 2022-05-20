import BRGTgeo

x = 30
y = 96

x1 = 0
y1 = 0
x2 = -55
y2 = 55

A,B,C = BRGTgeo.line_ABC_inclination(135)

print(A,B,C)

print(BRGTgeo.dist_point_line(x,y,A,B,C))

print(BRGTgeo.dist_point_line_inc(30,96,135))
