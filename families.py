import alv_sections as a_s

#Família 39x14
#Cada Bloco
P0515 = a_s.Bloco(4,14,19,'I',[],1.7,0,[0],0)
P1015 = a_s.Bloco(9,14,20,'I',[],1.7,0,[0],0)
P2015 = a_s.Bloco(19,14,21,'I',[],1.7,1,[],2.5)
P2015G = a_s.Bloco(19,14,22,'I',[1],1.7,1,[],2.5)
P3515 = a_s.Bloco(34,14,23,'C',[],1.7,2,[],2.5)
P3515G1 = a_s.Bloco(34,14,24,'C',[2],1.7,2,[],2.5)
P3515G2 = a_s.Bloco(34,14,25,'C',[1],1.7,2,[],2.5)
P3515F = a_s.Bloco(34,14,26,'C',[1,2],1.7,2,[],2.5)
P4015 = a_s.Bloco(39,14,27,'I',[],1.7,2,[],2.5)
P4015G = a_s.Bloco(39,14,28,'I',[1],1.7,2,[],2.5)
P4015F = a_s.Bloco(39,14,29,'I',[1,2],1.7,2,[],2.5)
P5515 = a_s.Bloco(54,14,30,'T',[],1.7,3,[],2.5)
P5515G1 = a_s.Bloco(54,14,31,'T',[2],1.7,3,[],2.5)
P5515G2 = a_s.Bloco(54,14,32,'T',[2,3],1.7,3,[],2.5)
P5515G3 = a_s.Bloco(54,14,33,'T',[3],1.7,3,[],2.5)
P5515F = a_s.Bloco(54,14,34,'T',[1,2,3],1.7,3,[],2.5)

familia_39x14_dict = {
'P0515':P0515,
'P1015':P1015,
'P2015':P2015,
'P2015G':P2015G,
'P3515':P3515,
'P3515G1':P3515G1,
'P3515G2':P3515G2,
'P3515F':P3515F,
'P4015':P4015,
'P4015G':P4015G,
'P4015F':P4015F,
'P5515':P5515,
'P5515G1':P5515G1,
'P5515G2':P5515G2,
'P5515G3':P5515G3,
'P5515F':P5515F,
}

A = familia_39x14_dict['P4015']
#print(A.area)