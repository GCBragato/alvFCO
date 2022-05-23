import os
pathConvUnid = os.getcwd() + "\\utilitarios"
import sys
sys.path.append(pathConvUnid)

import conv_areadeaco as cv_as
import conv_unidades as cv_un
import alv_fbk as a_fbk
import families as fam
import BRGTgeo as an_geo
import alv_subs as a_sub

# 1 - Início dos dados para dimensionamento:

# Propriedades físicas
fbk = 4
resistencias = a_fbk.Bloco_Concreto(fbk)
aco = a_fbk.Aco_Passivo('CA50')

# Geometria da subestrutura
sub_blo = a_sub.Subestrutura_Blocos([('P4015',(0,0),90),('P4015',(0,40),90)],fbk)
sub_aco = [[8,(0,-9.125)],[8,(0,9.125)],[8,(0,30.875)],[8,(0,49.1265)]]

# 2 - Tensões de dimensionamento
fd = resistencias.fd
fdG = resistencias.fdG
fyd = aco.fyd/2

# 3 - Separação de septos da subestrutura
# 0 - coordenada
# 1 - área
# 2 - status de graute
septo = []
for b in range(len(sub_blo.bList)):
    bloco = sub_blo.bList[b][0]
    print(bloco)
    # ABORTADO, MELHOR FAZER ISTO DENTRO DA CLASSE DA SUBESTRUTURA. PRÓXIMO PASSO