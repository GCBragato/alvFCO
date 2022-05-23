# Dicionário de proprieades físicas dos blocos de acordo com a norma

alv_fbk_1 = {'fbk':3,'fa':4,'fgk':15,'fpk/fbk':0.8,'fpk*/fpk':2,
'fpk':2.4,'fpk*':4.8,'ftk':-0.2,'E':1920,'E*':3840}
alv_fbk_2 = {'fbk':4,'fa':4,'fgk':15,'fpk/fbk':0.8,'fpk*/fpk':2,
'fpk':3.2,'fpk*':6.4,'ftk':-0.2,'E':2560,'E*':5120}
alv_fbk_3 = {'fbk':6,'fa':6,'fgk':15,'fpk/fbk':0.75,'fpk*/fpk':1.75,
'fpk':4.5,'fpk*':7.9,'ftk':-0.2,'E':3600,'E*':6320}
alv_fbk_4 = {'fbk':8,'fa':6,'fgk':20,'fpk/fbk':0.75,'fpk*/fpk':1.75,
'fpk':6,'fpk*':10.5,'ftk':-0.2,'E':4800,'E*':8400}
alv_fbk_5 = {'fbk':10,'fa':8,'fgk':20,'fpk/fbk':0.7,'fpk*/fpk':1.75,
'fpk':7,'fpk*':12.3,'ftk':-0.25,'E':5600,'E*':9840}
alv_fbk_6 = {'fbk':12,'fa':8,'fgk':25,'fpk/fbk':0.7,'fpk*/fpk':1.6,
'fpk':8.4,'fpk*':13.4,'ftk':-0.25,'E':6720,'E*':10720}
alv_fbk_7 = {'fbk':14,'fa':12,'fgk':25,'fpk/fbk':0.7,'fpk*/fpk':1.6,
'fpk':9.8,'fpk*':15.7,'ftk':-0.25,'E':7840,'E*':12560}
alv_fbk_8 = {'fbk':16,'fa':12,'fgk':30,'fpk/fbk':0.65,'fpk*/fpk':1.6,
'fpk':10.4,'fpk*':16.6,'ftk':-0.25,'E':8320,'E*':13280}
alv_fbk_9 = {'fbk':18,'fa':14,'fgk':30,'fpk/fbk':0.65,'fpk*/fpk':1.6,
'fpk':11.7,'fpk*':18.7,'ftk':-0.25,'E':9360,'E*':14960}
alv_fbk_10 = {'fbk':20,'fa':14,'fgk':35,'fpk/fbk':0.6,'fpk*/fpk':1.6,
'fpk':12,'fpk*':19.2,'ftk':-0.25,'E':9600,'E*':15360}
alv_fbk_11 = {'fbk':22,'fa':18,'fgk':35,'fpk/fbk':0.55,'fpk*/fpk':1.6,
'fpk':12.1,'fpk*':19.4,'ftk':-0.25,'E':9075,'E*':14550}
alv_fbk_12 = {'fbk':24,'fa':18,'fgk':40,'fpk/fbk':0.7,'fpk*/fpk':1.6,
'fpk':13.2,'fpk*':21.1,'ftk':-0.25,'E':9900,'E*':15825}

alv_fbk = {3:alv_fbk_1,4:alv_fbk_2,6:alv_fbk_3,8:alv_fbk_4,10:alv_fbk_5,
12:alv_fbk_6,14:alv_fbk_7,16:alv_fbk_8,18:alv_fbk_9,20:alv_fbk_10,
22:alv_fbk_11,24:alv_fbk_12}

class Bloco_Concreto:
    """Propriedades do Bloco de Concreto. Insira fbk em MPa.

    Propriedades:
    Coeficiente de Dilatação Térmica = .cDilTermica [/°C],
    .fbk [MPa], .fa [MPa], .fgk [MPa], .fpk_gpk, .fpkG_fpk, .fpk [MPa],
    .fpkG [MPa], .ftk [MPa], .Eb [MPa], .EbG [MPa], .y_a, .y_g,
    .fd [MPa], .fdG [MPa], .Eps_bu [o/oo]
    """
    def __init__(self, fbk, y_a = 2.0, y_g = 2.0):

        self.cDilTermica = 9*10e-6
        self.fbk = fbk
        self.fa = alv_fbk[fbk]['fa']
        self.fgk = alv_fbk[fbk]['fgk']
        self.fpk_fbk = alv_fbk[fbk]['fpk/fbk']
        self.fpkG_fpk = alv_fbk[fbk]['fpk*/fpk']
        self.fpk = alv_fbk[fbk]['fpk']
        self.fpkG = alv_fbk[fbk]['fpk*']
        self.ftk = alv_fbk[fbk]['ftk']
        self.Eb = alv_fbk[fbk]['E']
        self.EbG = alv_fbk[fbk]['E*']
        self.y_a = y_a
        self.y_g = y_g
        self.fd = 0.7*self.fpk/self.y_a
        self.fdG = 0.7*self.fpkG/self.y_g
        self.Eps_bu = 3 #o/oo

    def o_b_de_Eps_b(self,Eps_b):
        if Eps_b < 0.6:
            o_b = 0
        elif Eps_b <= 3:
            o_b = self.fd
        else:
            o_b = self.fd
        return o_b

    def o_bG_de_Eps_b(self,Eps_b):
        if Eps_b < 0.6:
            o_b = 0
        elif Eps_b <= 3:
            o_b = self.fdG
        else:
            o_b = 0
        return o_b

class Aco_Passivo:
    """Propriedades do Aço Passivo. Insira categoria como CA25, CA50 ou
    CA60 e superficie como lisa, entalhada ou nervurada.

    Propriedades:
    Peso próprio = .pp [kN/m³],
    Coeficiente de Dilatação Térmica = .cDilTermica [/°C],
    .Es [MPa], .n_1, .fyk [MPa], .fyd [MPa], .Eps_su [o/oo]
    .Eps_fyk [o/oo], .Eps_fyd [o/oo]
    """
    def __init__(self, catAco = 'CA50', superficie = 'nervurada', y_s = 1.15):
        self.catAco = catAco
        self.superficie = superficie
        self.y_s = y_s
        self.pp = 78.5
        self.cDilTermica = 10e-5
        self.Es = 210000
        self.n_1 = self.n_1_F()
        self.fyk = self.fyk_F()
        self.fyd = self.fyk/self.y_s
        self.Eps_su = 10
        self.Eps_fyk = self.fyk*1000/self.Es
        self.Eps_fyd = self.fyd*1000/self.Es

    def n_1_F(self):
        """Retorna aderencia da superfície da barra"""
        aderencia_dic = {'lisa': 1, 'entalhada': 1.4, 'nervurada': 2.25}
        return aderencia_dic.get(self.superficie)

    def fyk_F(self):
        """Retorna tensão de escoamento característica em MPa"""
        fyk_dic = {'CA25': 250, 'CA50': 500, 'CA60': 600}
        return fyk_dic.get(self.catAco)

    def o_s_de_Eps_s(self,Eps_s,tipo='b'):
        """Retorna tensão [MPa] para deformação inserida [o/oo]
        
        Tipo 'a' = retorna o_s para fyk\n
        Tipo 'b' = retorna o_s para fyd
        """
        if tipo == 'a':
            if Eps_s < self.Eps_fyk:
                o_s = Eps_s*self.Es*0.001
            elif Eps_s <= self.Eps_su:
                o_s = self.fyk
            else:
                o_s = 0
        if tipo =='b':
            if Eps_s < self.Eps_fyd:
                o_s = Eps_s*self.Es*0.001
            elif Eps_s <= self.Eps_su:
                o_s = self.fyd
            else:
                o_s = 0
        return o_s
