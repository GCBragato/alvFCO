from functools import partial
import os
pathConvUnid = os.getcwd() + "\\utilitarios"
import sys
sys.path.append(pathConvUnid)

import conv_areadeaco as cv_as
import conv_unidades as cv_un
import alv_fbk as a_fbk
import families as fam
import BRGTgeo
import alv_subs as a_sub
import math

# Entrada de Dados
hc = 12 # cm
hb = 39 # cm
bw = 14 # cm
d = 12+39-3 # cm
lamba = 0.8
alfa_c = 0.85
alfa_b = 1.0
Mk = 3.384 #tf.m
Vk = 4.705 #tf
gama_f = 1.0
fcd = 20/1.4 # MPa
fbd = 6.4/2 # MPa
fyd = (500/1.15)*cv_un.convPressao('MPa','tf/cm2')

print('\n'+'---- RESULTADOS ----'+'\n')
cv_aux = cv_un.convPressao('MPa','tf/cm2')
Md = Mk*gama_f*cv_un.convMomento('tf.m','tf.cm')
# Cálculo de fd equivalente por média ponderada
fdeq = (fcd*(alfa_b/alfa_c)*hc+fbd*(alfa_b/alfa_c)*hb)/(hc+hb)
print('fdeq = ',round(fdeq,2),'MPa')

# Teste se encaixa na Poss1
FRc = alfa_c*fcd*cv_aux*bw*hc # tf
dRc = d-hc/2 # cm
MRdc = FRc*dRc
poss1 = True
if MRdc < Md:
    poss1 = False
print('MRdC =',round(MRdc*cv_un.convMomento('tf.cm','tf.m'),2),'tf.m')
print('Poss1 =',poss1)

# Se Poss1 = True, dimensionar como uma viga normal
# Se Poss1 = False, dimensionar como uma viga mista

if poss1:
    print(f'd={d}cm')
    x = (d-(d**2-2*(Md/(bw*alfa_c*fcd*cv_aux)))**(1/2))/0.8
    print('x =',round(x,3),'cm')
    As = Md/((d-0.5*0.8*x)*fyd)
    print('As = ',round(As,3),'cm²')
    barra = 10
    print(math.ceil(cv_as.As_barras(As,barra)),f'Barras de {barra} mm')

if not poss1:
    Mc = alfa_c*fcd*cv_aux*bw*hc*(d-hc/2)
    # Poderia ser Mc = MRdc
    beta = alfa_b*fbd*cv_aux*bw
    a = 0.32*beta
    b = -beta*0.8*d
    c = beta*d*hc-beta*0.5*hc**2-Mc+Md
    x1 = (-b+math.sqrt(b*b-4*a*c))/(2*a)
    x2 = (-b-math.sqrt(b*b-4*a*c))/(2*a)
    print(f'd={d}cm')
    print('x1 =',round(x1,3),'cm')
    print('x2 =',round(x2,3),'cm')
    As1 = (alfa_c*fcd*cv_aux*bw*hc+alfa_b*fbd*cv_aux*bw*
    (0.8*x1-hc))/fyd
    print('As1 = ',round(As1,3),'cm²')
    barra = 10
    print(math.ceil(cv_as.As_barras(As1,barra)),f'Barras de {barra} mm')
    As2 = (alfa_c*fcd*cv_aux*bw*hc+alfa_b*fbd*cv_aux*bw*
    (0.8*x2-hc))/fyd
    print('As2 = ',round(As2,3),'cm²')
    print(math.ceil(cv_as.As_barras(As2,barra)),f'Barras de {barra} mm')