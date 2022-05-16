class Bloco():
    #get área por septo
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
            Inércia em torno do eixo X = .iX\n
            Inércia em torno do eixo Y = .iY\n
            Área líquida = .area\n
            Área bruta = .area_bruta\n

Eficiência de grauteamento é a relação fpk*/fpk\n
Para todos os cálculos o eixo X está na direção paralela ao comprimento
    """

    def __init__(self,comp:int,larg:int,alt:int,tipo:str,graute=[],
    egraute=1.7,nsept=2,lsept=[],esp=2.5):
        self.comp = comp
        self.larg = larg
        self.alt = alt
        self.nsept = nsept
        self.lsept = lsept
        self.esp = esp
        graute = [i-1 for i in graute if graute]
        if not graute:
            egraute = 0
        self.egraute = egraute
        if not lsept:
            self.lsept = self.auto_sept(tipo)
        self.Ix = self.inerciaX(comp,larg,graute,egraute,self.nsept,
        self.lsept,esp)
        self.Iy = self.inerciaY(comp,larg,graute,egraute,self.nsept,
        self.lsept,esp)
        self.area = self.area_F(comp,larg,graute,egraute,self.nsept,
        self.lsept,esp)
        self.area_bruta = self.comp*self.larg

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

    def area_F(self,base,altura,graute,egraute,nsept,lsept,esp):
        #Calcula a área do bloco inteiro
        aI = altura*base
        #Calcula a dedução de área de cada septo
        aS = 0
        for i in range(nsept):
            if i in graute:
                mgraute = 2-egraute
            else:
                mgraute = 1
            aS += ((altura-2*esp)*lsept[i])*mgraute

        return aI-aS
