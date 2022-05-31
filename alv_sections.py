from re import L
from alv_fbk import Bloco_Concreto

class Bloco():
    """Bloco de alvenaria estrutural em concreto armado.\n
    Insira: (comprimento, largura, altura, tipo, lista com índice de
    septos grauteados da esquerda para a direita, coeficiente de
    eficiência do grauteamento, número de septos, lista de septos e
    espessura da parede)

        Tipos:
            I = todos os septos iguais.\n
            T = bloco Tê com 3 septos onde o central é o menor\n
            C = bloco de Canto, 2 septos onde o esquerdo é o menor\n
            O = outro. Nesse caso a inserção de uma lista de
            comprimentos de septo é obrigatória\n

        Propriedades:\n
            Comprimento = .comp\n
            Largura = .larg\n
            Altura = .alt\n
            Tipo = .tipo\n
            Número de septos = .nsept\n
            Espessura da parede = .esp\n
            Lista de comprimentos de septos = .lsept\n
            Inércia líquida em torno do eixo X = .IxL\n
            Inércia líquida em torno do eixo Y = .IyL\n
            Área líquida = .areaL\n
            Inércia bruta em torno do eixo X = .IxB\n
            Inércia bruta em torno do eixo Y = .IyB\n
            Área bruta = .areaB\n

Eficiência de grauteamento é a relação fpk*/fpk\n
Para todos os cálculos o eixo X está na direção paralela ao comprimento
    """

    def __init__(self,comp:int,larg:int,alt:int,tipo:str,graute=[],
    egraute=2,nsept=2,lsept=[],esp=2.5):
        self.comp = comp
        self.larg = larg
        self.alt = alt
        if nsept == 0:
            nsept = 1
            lsept = [comp]
        self.nsept = nsept
        self.lsept = lsept
        self.esp = esp
        # 'graute' é uma lista indicando se o septo, enumerado da
        # esquerda para a direita, está grauteado
        # Se lista de pontos de graute != vazia, reduzir os valores
        # dentro dela em 1
        graute = [i-1 for i in graute if graute]
        # Se lista de pontos de graute = vazia, definir fator de
        # eficiência de graute como 0
        if not graute:
            egraute = 0
        self.graute = graute
        self.egraute = egraute
        # Se lista de comprimentos de septos vazia, executar função
        # que calcula o comprimento de cada septo automaticamente
        if not lsept:
            self.lsept = self.auto_sept(tipo)

        # Inércias e áreas
        self.IxL = self.inerciaX(comp,larg,graute,egraute,self.nsept,
        self.lsept,esp)
        self.IyL = self.inerciaY(comp,larg,graute,egraute,self.nsept,
        self.lsept,esp)
        self.areaL = self.areaL_F(comp,larg,graute,egraute,self.nsept,
        self.lsept,esp)
        self.IxB = (self.comp*self.larg**3)/12
        self.IyB = (self.larg*self.comp**3)/12
        self.areaB = self.comp*self.larg

        # Dados de área, resistência e coordenadas de cada septo
        # Obter usando lsept, egraute e
        self.csept = self.sept_comp(self.lsept,self.esp)
        self.asept = self.sept_area(self.csept,self.larg)
        self.xysept = self.sept_coords(self.comp,self.larg,self.csept)
        self.xyseptCG = self.sept_coordsCG(self.xysept)

    def auto_sept(self,tipo:str):
        """Retorna lista de septos para os tipos I (septos Iguais),
        T (Tê) e C (Canto)
        """

        lsept = []
        if tipo.upper() == 'I':
            #Se tipo Iguais, calcular todos os septos iguais
            for i in range(self.nsept):
                lsept.append((self.comp-(self.nsept+1)*self.esp)/
                self.nsept)
        elif tipo.upper() == 'T':
            #Aceita 3 septos
            #Se tipo T, teremos 3 septos, sendo o 1 e 3 iguais
            #Cálculo para septo do Meio
            sM = self.larg-2*self.esp
            #Cálculo para septos do Lado
            sL = (self.comp-sM-self.esp*4)/2
            lsept = [sL,sM,sL]
            self.nsept = 3
        elif tipo.upper() =='C':
            #Aceita 2 septos
            #Se tipo C, teremos 2 septos, sendo o à esquerda o menor
            #Cálculo para septo Menor
            sM = self.larg-2*self.esp
            #Cálculo para septo mAior
            sA = self.comp-sM-self.esp*3
            lsept = [sM,sA]
        return lsept

    def inerciaX(self,base,altura,graute,egraute,nsept,lsept,esp):
        #Calcula a inércia do bloco inteiro
        iI = base*altura**3/12
        
        #Calcula a dedução de inércia de cada septo
        iS = 0
        for i in range(nsept):
            if i in graute:
                mgraute = 2-egraute
            else:
                mgraute = 1
            iS += (lsept[i]*(altura-2*esp)**3/12)*mgraute

        return iI-iS
    
    def inerciaY(self,base,altura,graute,egraute,nsept,lsept,esp):
        #Calcula a inércia do bloco inteiro
        iI = altura*base**3/12

        #Calcula a dedução de inércia de cada septo
        iS = 0
        dAc = -base/2
        for i in range(nsept):
            if i in graute:
                mgraute = 2-egraute
            else:
                mgraute = 1
            dAc += esp + lsept[i]/2
            iS += (((altura-2*esp)*lsept[i]**3/12)+(altura-2*esp)*
            lsept[i]*(dAc**2))*mgraute
            dAc += lsept[i]/2

        return iI-iS

    def areaL_F(self,base,altura,graute,egraute,nsept,lsept,esp):
        #Calcula a área líquida do bloco inteiro
        aI = altura*base
        #Calcula a dedução de área de cada septo
        aS = 0
        if nsept == 0:
            return aI
        for i in range(nsept):
            if i in graute:
                mgraute = 2-egraute
            else:
                mgraute = 1
            aS += ((altura-2*esp)*lsept[i])*mgraute

        return aI-aS

    def sept_comp(self,lsept,esp):
        """Comprimento de cada septo bruto"""
        #Se septo for último ou primeiro, comprimento dele é lsept + esp + 1/2 esp
        #Se não, lsept + 1/2 esp + 1/2 esp
        csept = []
        if len(lsept) == 0:
            return [self.comp]
        for i in range(len(lsept)):
            if i == 0 or i == len(lsept)-1:
                csept.append(lsept[i]+1.0*esp+0.5*esp)
            else:
                csept.append(lsept[i]+0.5*esp+0.5*esp)
        return csept

    def sept_area(self,csept,larg):
        """Área de cada septo bruto"""
        asept = []
        if len(csept) == 0:
            return self.areaL
        for i in range(len(csept)):
            asept.append(csept[i]*larg)
        return asept

    def sept_coords_liquid(self,comp,larg,esp,lsept):
        """Coordenadas dos vértices de cada septo líquido"""
        dAc = -comp/2
        coords = []
        for i in range(len(lsept)):
            dAc += esp+lsept[i]/2
            c1 = [dAc+(lsept[i]/2),-(larg/2)+esp]
            c2 = [dAc+(lsept[i]/2),(larg/2)-esp]
            c3 = [dAc-(lsept[i]/2),(larg/2)-esp]
            c4 = [dAc-(lsept[i]/2),-(larg/2)+esp]
            coords.append([c1,c2,c3,c4])
            dAc += lsept[i]/2
        return coords

    def sept_coords(self,comp,larg,csept):
        """Coordenadas dos vértices de cada septo bruto"""
        dAc = -comp/2
        coords = []
        for i in range(len(csept)):
            c1 = [dAc,+larg/2]
            c2 = [dAc,-larg/2]
            c3 = [dAc+csept[i],-larg/2]
            c4 = [dAc+csept[i],+larg/2]
            coords.append([c1,c2,c3,c4])
            dAc += csept[i]
        return coords

    def sept_coordsCG(self,xysept):
        """Coordenas do CG de cada septo"""
        # xysept é uma lista de listas
        # A lista [0] tem o comprimento igual ao número de septos do bloco
        # A lista [1] tem o comprimento de 4, sendo cada um uma lista
        # A lista [2] tem o comprimento de 2, são coordenadas cartesianas

        # Precisamos retornar 1 lista d2
        # Lista [0] é uma lista de septos
        # Lista [1] é uma lista com CG de cada septo
        septo = []
        for m in range(len(xysept)): # Loop externo, percorre septos
            cgX = 0.0
            cgY = 0.0
            coorsX = []
            coorsY = []
            # PODE SER OTIMIZAADO PARA 1 SÓ LOOP
            for i in range(4): # Loop interno a, extrai as coordenadas
                coorsX.append(xysept[m][i][0])
                coorsY.append(xysept[m][i][1])
            for i in range(4): #Loop interno b, calcula o CG
                cgX += (coorsX[i-1]+coorsX[i])*(coorsX[i-1]*coorsY[i]-coorsX[i]*coorsY[i-1])
                cgY += (coorsY[i-1]+coorsY[i])*(coorsX[i-1]*coorsY[i]-coorsX[i]*coorsY[i-1])
            septo.append([cgX/(6*self.asept[m]),cgY/(6*self.asept[m])])
        return septo
