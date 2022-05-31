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

def data_of_polyline(polyline):
    # Particiona os pontos X e Y da polilinha em duas listas
    coorsX = []
    coorsY = []
    for XY in polyline:
        coorsX.append(XY[0])
        coorsY.append(XY[1])

    #Calcula a área e o centroide de um polígono
    sArea = 0.0
    cgX = 0
    cgY = 0
    for i in range(len(coorsX)):
        sArea += (coorsX[i-1]+coorsX[i])*(coorsY[i-1]-coorsY[i])
        cgX += (coorsX[i-1]+coorsX[i])*(coorsX[i-1]*coorsY[i]-coorsX[i]*coorsY[i-1])
        cgY += (coorsY[i-1]+coorsY[i])*(coorsX[i-1]*coorsY[i]-coorsX[i]*coorsY[i-1])
    sArea = abs(sArea/2)
    cgX = cgX/(6*sArea)
    cgY = cgY/(6*sArea)
    return sArea, cgX, cgY

def discretize(polyline,N):
    """Dividir uma polilinha em n*n segmentos. Cada lado será dividido
    por n. Retorna lista de polilinhas com 4 vértices e sua área.
    Os vértices devem ser listados em ordem anti-horária.

    Args:
        polyline (list): lista de 4 vértices
        N (integer): número de divisões por lado
    """

    # 1 - Encontrar ângulo da reta A->B com o eixo x
    theta = math.atan((polyline[1][1]-polyline[0][1])/(polyline[1][0]-polyline[0][0]))
    # 2 - Encontrar o comprimento dos vetores X0,Y0->X1,Y1 e X0,Y0->X3,Y3
    r = dist_2p(polyline[0][0],polyline[0][1],polyline[1][0],polyline[1][1])
    t = dist_2p(polyline[0][0],polyline[0][1],polyline[3][0],polyline[3][1])
    # 3 - Encontrar os lados/2 de cada seção discretizada
    m = r/(2*N)
    n = t/(2*N)
    # 4 - Área da seção discretizada
    area = (m*2)*(n*2)
    # 5 - Início da lista de seções
    sect = []
    # 6 - Loops
    for i in range(N): # Loop externo
        v = i*(2*n)+n
        for j in range(N): # Loop interno
            u = j*(2*m)+m
            alfa = math.atan(v/u)
            hip = math.sqrt(u**2+v**2)
            x = math.cos(alfa+theta)*hip
            y = math.sin(alfa+theta)*hip
            xcg = polyline[0][0]+x
            ycg = polyline[0][1]+y
            sect.append([[xcg,ycg],area])
    return sect #lista de cg e área de cada segmento

def axis_rotation(x,y,theta):
    """Return a point to a new rotated axis"""
    theta = math.radians(theta)
    xr = x*math.cos(theta)-y*math.sin(theta)
    yr = x*math.sin(theta)+y*math.cos(theta)
    return xr, yr