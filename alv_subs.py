import families as fam

class Subestrutura():
    def __init__(self,bList = []):
        """Subestrutura de Alvenaria Estrutural"""
        self.bList = bList
        self.name_list,self.coordXY_list,self.coordX_list,self.coordY_list,self.dir_list = self.get_lists()
        self.coord_CGX, self.coord_CGY = self.get_CG()
        self.Ix,self.Iy,self.area = self.get_inertia()

    def get_lists(self):
        """Quebra a lista de entrada em outras listas simples"""
        name_list = []
        coordXY_list = []
        coordX_list = []
        coordY_list = []
        dir_list = []
        for i in range(len(self.bList)):
            name_list.append(self.bList[i][0])
            coordXY_list.append(self.bList[i][1])
            coordX_list.append(self.bList[i][1][0])
            coordY_list.append(self.bList[i][1][1])
            dir_list.append(self.bList[i][2])
        return name_list,coordXY_list,coordX_list,coordY_list,dir_list

    def get_CG(self):
        """Encontra o centro de gravidade da subestrutura"""
        #Para CG X, somar coordenadas X*Área
        #Para CG Y, somar coordenadas Y*Área
        sumArea = 0.0
        sumX = 0.0
        sumY = 0.0
        for i in range(len(self.bList)):
            #Área do bloco
            area = fam.familia_39x14_dict[self.name_list[i]].areaB
            sumArea += area
            #Coordenadas X
            cX = self.coordX_list[i]
            sumX += area*cX
            #Coordenadas Y
            cY = self.coordY_list[i]
            sumY += area*cY
        return sumX/sumArea,sumY/sumArea

    def get_inertia(self):
        """Calcula a inércia da subestrutura pelo teorema de eixos paralelos"""
        #Cada bloco tem uma Inércia, uma Coordenada e uma Área
        #O teorema de eixos paralelos diz: Icg = I + A*Dcg²
        #A distância para o CG = coordenada do bloco - self.coord_CG
        #A inércia a ser somada depende da direção do bloco
        #Se bloco em X, usar inércia X e vice-versa
        Ix = 0.0
        Iy = 0.0
        sArea = 0.0
        for i in range(len(self.bList)):
            #Cálculo de inércia X da subestrutura
            # 1 - Inércia do bloco
            if self.dir_list[i] == 'X':
                inercia = fam.familia_39x14_dict[self.name_list[i]].IxB
            else:
                inercia = fam.familia_39x14_dict[self.name_list[i]].IyB
            # 2 - Área do bloco
            area = fam.familia_39x14_dict[self.name_list[i]].areaB
            sArea += area
            # 3 - Distância do bloco ao CG da subestrutura
            distancia = self.coordY_list[i] - self.coord_CGY
            Ix += inercia + area*distancia**2

            #Cálculo de inércia Y da subestrutura
            # 1 - Inércia do bloco
            if self.dir_list[i] == 'X':
                inercia = fam.familia_39x14_dict[self.name_list[i]].IyB
            else:
                inercia = fam.familia_39x14_dict[self.name_list[i]].IxB
            # 2 - Área do bloco já foi calculada, se declarar aqui dobra
            #area = fam.familia_39x14_dict[self.name_list[i]].area_bruta
            #sArea += area
            # 3 - Distância do bloco ao CG da subestrutura
            distancia = self.coordX_list[i] - self.coord_CGX
            Iy += inercia + area*distancia**2
        return Ix,Iy,sArea

#mySub = Subestrutura([('P4015',(7,209.5),'Y'),('P4015',(7,369.5),'Y'),('P4015',(7,129.5),'Y'),('P0515',(7,442),'Y'),('P4015',(7,249.5),'Y'),('P2015',(-70.5,62),'X'),('P4015',(-40.5,62),'X'),('P4015',(7,329.5),'Y'),('P4015',(7,289.5),'Y'),('P3515G2',(7,407),'Y'),('P3515F',(-3,62),'X'),('P2015G',(-10.5,477),'X'),('P4015F',(7,89.5),'Y'),('P3515F',(7,37),'Y'),('P2015G',(7,9.5),'Y'),('P4015',(7,169.5),'Y'),('P3515F',(17,432),'X'),('P4015F',(7,464.5),'Y')])
#print('area = ', mySub.area/(100**2))
#print(mySub.Ix/(100**4)) #Se minha sub tá em Y, uso Inércia X, que é esse caso estudado
#print(mySub.Iy/(100**4))
#Ix deve ser 2.634

mySub2 = Subestrutura([('P4015',(0,-20),'Y'),('P4015',(0,20),'Y')])
#print('area = ', mySub2.area/(100**2))
print(mySub2.Ix/(100**4))
#print(mySub2.Iy/(100**4))

mySub3 = Subestrutura([('P4015',(0,100),'Y'),('P4015',(0,140),'Y'),('P4015',(0,60),'Y'),('P4015',(0,20),'Y'),('P4015',(0,-20),'Y'),('P4015F',(0,-140),'Y'),('P4015F',(0,-180),'Y'),('P4015',(0,-100),'Y'),('P4015F',(0,180),'Y'),('P4015',(0,-60),'Y'),('P4015F',(0,220),'Y')])
#print('area = ', mySub3.area/(100**2))
print('mysub3 ',mySub3.Ix/(100**4))
#print(mySub3.Iy/(100**4))

#mySub4 = Subestrutura([('P2015G',(100,175),'Y'),('P3515F',(100,147.5),'Y'),('P5515G2',(100,267.5),'Y'),('P5515G1',(100,212.5),'Y'),('P2015',(100,30),'Y'),('P4015',(100,0),'Y'),('P3515',(100,112.5),'Y'),('P5515',(100,67.5),'Y'),('P1015',(100,505),'Y'),('P4015F',(100,480),'Y'),('P4015',(100,535),'Y'),('P0515',(100,512.5),'Y'),('P3515G1',(100,367.5),'Y'),('P5515F',(100,322.5),'Y'),('P4015G',(100,440),'Y'),('P3515G2',(100,402.5),'Y')])
#print(mySub4.Ix/(100**4)) #deveria ser 2.517292

#MINHA INERCIA TÁ DANDO SEMPRE MENOR