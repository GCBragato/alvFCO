import os

pathConvUnid = os.getcwd() + "\\utilitarios"
import sys
sys.path.append(pathConvUnid)

def discretizar_septos(septos,N):
    """Discretiza cada septo em N² segmentos. Cada lado será dividido
    por N. Retorna lista de septos com seu cg, área e status de graute.

    Args:
        septos (list): lista de septos em que
        [0] = lista de 4 vértices
        [1] = CG
        [2] = área
        [3] = status de graute
        N (integer): número de divisões por lado
    """

    septos_discretizados = []
    for septo in septos:
        polyline = septo[0]
        septo_discretizado = BRGTgeo.discretize(polyline,N)
        for sect in septo_discretizado:
            sect.append(septo[3])
            septos_discretizados.append(sect)

    return septos_discretizados

def ponderadores(trav_a,trav_b,graute_a,graute_b,R):
    """Calcula os ponderadores"""
    if trav_a:
        if graute_a:
            k_a = 2
        else:
            k_a = 1.5
    else:
        if graute_a:
            k_a = 2*R
        else:
            k_a = 1.5*R

    if trav_b:
        if graute_b:
            k_b = 2
        else:
            k_b = 1.5
    else:
        if graute_b:
            k_b = 2*R
        else:
            k_b = 1.5*R

    return k_a,k_b

import conv_areadeaco as cv_as
import conv_unidades as cv_un
import alv_fbk as a_fbk
import families as fam
import BRGTgeo
import alv_subs as a_sub

# 1 - Início dos dados para dimensionamento:

# Propriedades físicas
fbk = 4
resistencias = a_fbk.Bloco_Concreto(fbk)
aco = a_fbk.Aco_Passivo('CA50')

# Geometria da subestrutura
sub_blo = a_sub.Subestrutura_Blocos([('P4015F',(0,0),90),('P4015F',(0,40),90)],fbk)
sub_aco = [[8,(0,-9.125)],[8,(0,9.125)],[8,(0,30.875)],[8,(0,49.1265)]]

# Dados necessários para AlvEst:
hef = 280 # Altura efetiva (cm)
tef = 14 # Largura efetiva (cm)
R = 1-(hef/(40*tef))**3 # Redutor de resistência à compressão devido à flambagem
trav_a = True # Status de travamento por flange lado A
trav_b = True # Status de travamento por flange lado B
graute_a = True # Status de graute lado A
graute_b = True # Status de graute lado B
k_a,k_b = ponderadores(trav_a,trav_b,graute_a,graute_b,R)
sub_dir = 'Y' # Direção da subestrutura
# metodo = 2 # Ver mais abaixo

# 2 - Tensões de dimensionamento
fd = resistencias.fd # MPa
fdG = resistencias.fdG # MPa
fyd = aco.fyd/2 # MPa

# 3 - Separação de septos da subestrutura
# 0 - coordenadas dos vértices
# 1 - [X,Y] do CG
# 2 - área do septo
# 3 - status de graute
septos = sub_blo.sept_list
N = 10

discret = discretizar_septos(septos,N)
# Áreas discretizadas:
# [n][0] - Coordenadas do CG
#   [n][0][0] - X
#   [n][0][1] - Y
# [n][1] - Área do septo
# [n][2] - Status de graute

# 4 - Normal Máxima
dA_a = []
dA_b = []
# Dependendo da direção da subestrutura, separa as áreas discretizadas em
# Regiões A e B
for dA in discret:
    if sub_dir == 'Y':
        if dA[0][1] >= sub_blo.coord_CGY:
            dA_a.append(dA)
        else:
            dA_b.append(dA)
    else:
        if dA[0][0] >= sub_blo.coord_CGX:
            dA_a.append(dA)
        else:
            dA_b.append(dA)

# # Correção de áreas para o método de cálculo
# # Método 1 - Aumento de fd para fdG em áreas grauteadas
# # Método 2 - Aumento de fd para fdG e área por egraute
# eGraute = a_fbk.alv_fbk[fbk]['fpk*/fpk']
# if metodo == 2:
#     for dA in dA_a:
#         dA[1] = dA[1]*eGraute
#     for dA in dA_b:
#         dA[1] = dA[1]*eGraute

# Soma das áreas nas regiões A e B
area_a = 0.0 # Total de áreas não grauteadas
area_aG = 0.0 # Total de áreas grauteadas
for dA in dA_a:
    if dA[2]: # Se área grauteada
        area_aG += dA[1]
    else:
        area_a += dA[1]

area_b = 0.0
area_bG = 0.0
for dA in dA_b:
    if dA[2]: # Se área grauteada
        area_bG += dA[1]
    else:
        area_b += dA[1]

# NRd máxima
R = 0.85
NRd_max = (fd*cv_un.convPressao('MPa','tf/cm2')*R*(area_a+area_b)+
fdG*cv_un.convPressao('MPa','tf/cm2')*R*(area_aG+area_bG))
#print(fdG*cv_un.convPressao('MPa','tf/m2'))
print(R)
print(NRd_max)
teste2 = resistencias.fk*1000/resistencias.Eb
#print(teste2)

# AGORA FINALMENTE POSSO IR PARA FCO
# sub_aco = lista com diâmetro em mm e coordenadas
# discret = lista com coordenada dos CGs, áreas e status de graute
# Tenho também as resistências e o módulo de elasticidade de cada material
# Assim, falta escrever funções para FCO