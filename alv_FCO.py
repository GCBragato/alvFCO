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
from scipy.optimize import brentq

import matplotlib.pyplot as plt
import numpy as np

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

def get_k(trav,graute,R):
    """Calcula o ponderador K que varia com status de graute"""
    if trav:
        if graute:
            k = 2
        else:
            k = 1.5
    else:
        if graute:
            k = 2*R
        else:
            k = 1.5*R

    return k

# Pra obtenção de tensão do bloco, depende do status de graute
# Porém, o método escolhido para calculado FCO é ponderar a área com egraute
# Logo, a área é majorada, a tensão é igual, mas a resultante é maior
# O que significa que precisaremos encontrar o equilíbio pela RESULTANTE
def tensao_bloco(Eps):
    return a_fbk.o_b_de_Eps_b(Eps)

def tensao_aco(Eps):
    return a_fbk.o_s_de_Eps_s(Eps)

def esforcos(x=0.0,normal=0.0,secoes=[],sub_aco=[],d_fc = 0.0,egraute=1.0,fyd=0.0,fd=0.0):
    # Equação f(xln) = N - sum(ob*Ab)-sum(os*As)
    # Encontrar quais áreas entram no cálculo, com base em X
    # Preciso computar a distância da face mais comprimida até a seção
    sum_secoes_c = 0.0
    for dA in secoes[0]:
        # Se a área estiver dentro do retângulo 0.8*x, entra na soma
        if dA[0][1] >= (d_fc - x*0.8):
            #print('dA[0][1] = ',dA[0][1])
            sum_secoes_c += dA[1]
    # Preciso corrigir essa área se ela tem uma barra de aço dentro
    for aco in sub_aco:
        if aco[1][1] >= d_fc - x*0.8:
            # Não preciso reduzir a área de aço da área de compressão
            # ABNT NBR 16868-1 11.5.3.2
            # Aumentar a área de tensão à compressão, encontrando uma
            # área equivalente se a tensão fosse fd
            #sum_secoes_c += (egraute*math.pi*aco[0]**2/(4*100))*fyd/fdG
            pass
    forcas_c = sum_secoes_c*fd*cv_un.convPressao('MPa','tf/cm2') # tf

    # Para encontrar os esforços de tração, preciso calcular a
    # deformação em cada barra
    # Primeiro: encontrar o ângulo da deformação
    if x == 0.0:
        x = 1/1000000
    ang_def = math.atan(3/x)
    defs = []
    for aco in sub_aco:
        d_this = d_fc-aco[1][1]
        defs.append([(d_this-x)*math.tan(ang_def),aco[0]])
    forcas_t = 0.0
    aco = a_fbk.Aco_Passivo()
    for def_ in defs:
        forcas_t -= aco.o_s_de_Eps_s(def_[0])*cv_un.convPressao('MPa','tf/cm2')*cv_as.barras_As(1,def_[1])

    #print('normal',normal)
    #print('forcas_c',forcas_c)
    #print('forcas_t',forcas_t)
    soma = normal - forcas_c - forcas_t
    #print('soma',soma)
    return soma

#main(fbk,aco,sub_blo,sub_aco,hef,tef,trav_a,trav_b,sub_dir,egraute,fd,fdG,fyd,N,normal)
def main(fbk,aco,sub_blo,sub_aco,hef,tef,trav_a,trav_b,sub_dir,N,normal):
    # 1 - Início dos dados para dimensionamento:

    # Propriedades físicas
    #fbk = 4
    resistencias = a_fbk.Bloco_Concreto(fbk)
    #aco = a_fbk.Aco_Passivo('CA50')

    # Geometria da subestrutura
    # sub_blo = a_sub.Subestrutura_Blocos(
    #     [
    #         ('P4015F',(0,0),90)
    #         ,('P4015F',(0,40),90)
    #     ]
    #     ,fbk)
    # sub_aco = [
    #         [8,[0,-9.125]],
    #         [8,[0,9.125]],
    #         [8,[0,30.875]],
    #         [8,[0,49.1265]]
    #     ]

    # Dados necessários para AlvEst:
    # hef = 280 # Altura efetiva (cm)
    # tef = 14 # Largura efetiva (cm)
    R = 1-(hef/(40*tef))**3 # Redutor de resist. à comp. devido à flambagem
    # trav_a = False # Status de travamento por flange lado A
    # trav_b = False # Status de travamento por flange lado B
    # graute_a = True # Status de graute lado A
    # graute_b = True # Status de graute lado B
    # k_a,k_b = ponderadores(trav_a,trav_b,graute_a,graute_b,R) # errado
    # k_a e k_b deve ser calculado para cada seção discretizada
    # sub_dir = 'Y' # Direção da subestrutura
    # metodo = 2 # Ver mais abaixo - abortado para FCO, aqui para lembrar
    egraute = a_fbk.alv_fbk[fbk]['fpk*/fpk']

    # 2 - Tensões de dimensionamento
    fd = resistencias.fd # MPa
    fdG = resistencias.fdG # MPa
    fyd = aco.fyd # MPa

    # 3 - Separação de septos da subestrutura
    # 0 - coordenadas dos vértices
    # 1 - [X,Y] do CG
    # 2 - área do septo
    # 3 - status de graute
    septos = sub_blo.sept_list
    # N = 99

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

    # Soma da área de aço, entra na compressão para cálculo de FCO
    sum_As = 0.0
    for aco in sub_aco:
        sum_As += math.pi*aco[0]**2/400 # cm²

    # NRd máxima
    R = 0.85
    NRd_max = (fd*cv_un.convPressao('MPa','tf/cm2')*R*(area_a+area_b)+
    fdG*cv_un.convPressao('MPa','tf/cm2')*R*(area_aG+area_bG)
    +fyd*cv_un.convPressao('MPa','tf/cm2')*sum_As)

    # 5 - Normal Mínima
    NRd_min = -fyd*cv_un.convPressao('MPa','tf/cm2')*sum_As # tf

    # 6 - Coordenadas mais distantes do CG para cada quadrante
    # Para calcular a altura útil (d) de cada ângulo de linha neutra (alfa)
    # 6.1 - Lista de coordenadas extremas de cada bloco
    coords_blocos = sub_blo.coordXYCG_list
    coords_extremas = []

    for i in range(len(sub_blo)):
        # Coordenada do bloco depende da rotação dele
        teta = sub_blo.dir_list[i]
        # Ponto 1
        x = sub_blo.familia[sub_blo.bList[i][0]].bcoords[0][0]
        y = sub_blo.familia[sub_blo.bList[i][0]].bcoords[0][1]
        x,y = BRGTgeo.axis_rotation(x,y,teta)
        x1 = coords_blocos[i][0] + x
        y1 = coords_blocos[i][1] + y
        # Ponto 2
        x = sub_blo.familia[sub_blo.bList[i][0]].bcoords[1][0]
        y = sub_blo.familia[sub_blo.bList[i][0]].bcoords[1][1]
        x,y = BRGTgeo.axis_rotation(x,y,teta)
        x2 = coords_blocos[i][0] + x
        y2 = coords_blocos[i][1] + y
        # Ponto 3
        x = sub_blo.familia[sub_blo.bList[i][0]].bcoords[2][0]
        y = sub_blo.familia[sub_blo.bList[i][0]].bcoords[2][1]
        x,y = BRGTgeo.axis_rotation(x,y,teta)
        x3 = coords_blocos[i][0] + x
        y3 = coords_blocos[i][1] + y
        # Ponto 4
        x = sub_blo.familia[sub_blo.bList[i][0]].bcoords[3][0]
        y = sub_blo.familia[sub_blo.bList[i][0]].bcoords[3][1]
        x,y = BRGTgeo.axis_rotation(x,y,teta)
        x4 = coords_blocos[i][0] + x
        y4 = coords_blocos[i][1] + y

        coords_extremas.append([[x1,y1],[x2,y2],[x3,y3],[x4,y4]])

    # 6.2 Ponto mais distante para cada quadrante - ver_dist[quadrante][x,y]
    ver_dist = [[0,0],[0,0],[0,0],[0,0]]
    dist_q1 = 0.0
    dist_q2 = 0.0
    dist_q3 = 0.0
    dist_q4 = 0.0
    for i in range(len(sub_blo)):
        # i = número do bloco dentro da subestrutura
        for j in range(4):
            # j = número do vértice extremo do bloco
            x = coords_extremas[i][j][0]
            y = coords_extremas[i][j][1]
            if x >= 0 and y >= 0:
                if BRGTgeo.dist_2p(0,0,x,y) > dist_q1:
                    dist_q1 = BRGTgeo.dist_2p(0,0,x,y)
                    ver_dist[0] = [x,y]
            elif x < 0 and y >= 0:
                if BRGTgeo.dist_2p(0,0,x,y) > dist_q2:
                    dist_q2 = BRGTgeo.dist_2p(0,0,x,y)
                    ver_dist[1] = [x,y]
            elif x < 0 and y < 0:
                if BRGTgeo.dist_2p(0,0,x,y) > dist_q3:
                    dist_q3 = BRGTgeo.dist_2p(0,0,x,y)
                    ver_dist[2] = [x,y]
            elif x >= 0 and y < 0:
                if BRGTgeo.dist_2p(0,0,x,y) > dist_q4:
                    dist_q4 = BRGTgeo.dist_2p(0,0,x,y)
                    ver_dist[3] = [x,y]

    # 7 - Função para encontrar a profundidade da linha neutra

    # 7.1 - Para alvaneria estrutural, a tensão é reduzida por R ou K
    # A Normal é sempre reduzida por R, mas a tensão causada pelo momento
    # pode ser reduzida por K ou K*R, dependendo do status de travamento
    # da subestrutura naquela região
    # Em FCO, a tensão obtida para uma seção discretizada é a partir da
    # deformação, o que depende da área e módulo de elasticidade
    # Simplificadamente: Deformação = Tensão / Módulo de elasticidade
    # e Tensão = Força / Área
    # Sendo assim, para simplificar, ponderaremos a área de cada seção
    # discretizada de acordo com seu status de graute e travamento
    # Todas as seções dA_a e dA_b serão salvas em duas lista simplificadas
    # que possui CG e área somente, uma para Normal e outra para Momento
    # As novas listas serão dA_n e dA_m
    dA_n = []
    dA_m = []

    # Seções discretizadas da região 'a' = dA_a
    # Seções discretizadas da região 'b' = dA_b
    # Status de travamento da região 'a' = trav_a
    # Status de travamento da região 'b' = trav_b
    # Para isso também, precisamos majorar a área de cada um pelo coeficiente
    # de eficiência de graute.

    for dA in dA_a:
        if dA[2]:
            coef_graute = egraute
        else:
            coef_graute = 1.0
        dA_n.append([dA[0],dA[1]*R*coef_graute])
        k = get_k(trav_a,dA[2],R)
        dA_m.append([dA[0],dA[1]*k*coef_graute])
    for dA in dA_b:
        if dA[2]:
            coef_graute = egraute
        else:
            coef_graute = 1.0
        dA_n.append([dA[0],dA[1]*R*coef_graute])
        k = get_k(trav_b,dA[2],R)
        dA_m.append([dA[0],dA[1]*k*coef_graute])

    # Equação da linha neutra que depende só da normal que será iterada
    # pelo método de brentq. Para encontrar a soma das tensões pelas
    # deformações, criarei a função 'esforcos'
    # Porém, para iterar por brentq, preciso de uma função com só uma
    # entrada. Para isto, usarei o módulo 'partial' de functools.
    # A inclinação da linha neutra usada depende da discretização requerida
    # Por enquanto, usarei 0 radianos.

    inc_x = 0 # deg
    # As áreas discretizadas foram para coordendas globais.
    # Preciso atualizar a coordenada de cada barra para em relação ao
    # centro de gravidade da subestrutura
    for i in range(len(dA_n)):
        dA_n[i][0][0] -= sub_blo.coord_CGX
        dA_n[i][0][1] -= sub_blo.coord_CGX
        dA_m[i][0][0] -= sub_blo.coord_CGY
        dA_m[i][0][1] -= sub_blo.coord_CGY
    # A sub_aco de entrada foi para coordendas globais.
    # Preciso atualizar a coordenada de cada barra para em relação ao
    # centro de gravidade da subestrutura
    for aco in sub_aco:
        aco[1][0] -= sub_blo.coord_CGX
        aco[1][1] -= sub_blo.coord_CGY

    # Para entrar na equação de FCO, precisamos rotacionar as coordenadas
    # de dA n e m para que a linha neutra seja a horizontal
    for dA in dA_n:
        dA[0][0],dA[0][1] = BRGTgeo.axis_rotation(dA[0][0],dA[0][1],inc_x)
    for dA in dA_m:
        dA[0][0],dA[0][1] = BRGTgeo.axis_rotation(dA[0][0],dA[0][1],inc_x)
    secoes = [dA_n,dA_m]

    # Idem, precisamos rotacionar as coordenadas de sub_aco
    for aco in sub_aco:
        aco[1][0],aco[1][1] = BRGTgeo.axis_rotation(aco[1][0],aco[1][1],inc_x)

    # Encontrar altura últil para inc_x
    d_fc = 0.0 # Distância do CG à fibra mais comprimida
    for i in range(4):
        x,y = BRGTgeo.axis_rotation(ver_dist[i][0],ver_dist[i][1],inc_x)
        if y >= 0:
            d_fc = max(d_fc,BRGTgeo.dist_point_line_inc(x,y,inc_x))
    d_ft = 0.0 # Distância do CG à fibra mais tracionada
    for aco in sub_aco:
        x,y = BRGTgeo.axis_rotation(aco[1][0],aco[1][1],inc_x)
        if y <= 0:
            d_ft = max(d_ft,BRGTgeo.dist_point_line_inc(x,y,inc_x))
    d = abs(d_fc)+abs(d_ft) # Soma das distâncias = altura útil


    # normal = NRd_max/4
    esforcos_parcial = partial(esforcos,normal=normal,secoes=secoes,sub_aco=sub_aco,d_fc=d_fc,egraute=egraute,fyd=fyd,fd=fd)
    #teste = esforcos_parcial(x=39.5)
    #print('teste',teste)

    # Cálculo de X para que a barra mais afastada esteja deformada a 10o/oo
    xmin = 3*d/(10+3)

    # Testa se f(val1) > 0, se sim, diminui val1
    # Testa se f(fal2) < 0, se sim, aumenta val2
    # Se não encontrar dentro de 10 tentativas, retorna erro
    val1 = 10*d
    val2 = xmin
    #print('esforcos_parcial(x=',val1,') = ',esforcos_parcial(x=val1))
    #print('esforcos_parcial(x=',val2,') = ',esforcos_parcial(x=val2))
    #input()

    errorLevel = False
    for i in range(999):
        if esforcos_parcial(x=val1) >= 0:
            val1 = 10*val1
        if esforcos_parcial(x=val2) <= 0:
            val2= 10*val2
        if esforcos_parcial(x=val1) < 0 and esforcos_parcial(x=val2) > 0:
            break
        if i == 998:
            errorLevel = True
            break

    if errorLevel:
        print('Erro: x não encontrado')
        return 0
    else:
        raiz = brentq(esforcos_parcial,val1,val2,xtol=1.0*10e-6,rtol=1.0*10e-6,maxiter=100)

    """
    # ---- PLOT TEST ----

    # 100 linearly spaced numbers
    x = np.linspace(-35,35,20000)

    # the function, which is y = x^3 here
    y=[]
    for x_ in x:
        y.append(esforcos_parcial(x_))

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x,y, color='b', lw = 2.0)

    # show the plot
    plt.show()
    """
    return raiz

if __name__ == '__main__':
    # Entrada de Dados
    fbk = 4 # MPa
    aco = a_fbk.Aco_Passivo('CA50')
    sub_blo = a_sub.Subestrutura_Blocos(
        [
            ('P4015F',(0,0),90)
            ,('P4015F',(0,40),90)
        ]
        ,fbk)
    sub_aco = [
            [8,[0,-9.125]],
            [8,[0,9.125]],
            [8,[0,30.875]],
            [8,[0,49.1265]]
        ]
    hef = 280 # Altura efetiva (cm)
    tef = 14 # Largura efetiva (cm)
    trav_a = False # Status de travamento por flange lado A
    trav_b = False # Status de travamento por flange lado B
    sub_dir = 'Y' # Direção da subestrutura
    N = 99 # Discretizações por lado
    div = 4
    normal = 29.533503036071373 * ( 1 / div ) # Normal (tf)

    # Cálculo de x
    resultado = main(fbk,aco,sub_blo,sub_aco,hef,tef,trav_a,trav_b,sub_dir,N,normal)
    print(f'x = {resultado:.3f} cm')
