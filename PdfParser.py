# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <codecell>

from pyPdf import PdfFileReader
import re
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import numpy as np

# <markdowncell>

# Import Data
# =
# Import Timetable

# <codecell>

PDFHorario = PdfFileReader(file('Horarios.pdf','rb'))
Paginas = [page.extractText() for page in PDFHorario.pages]
for i in range(len(Paginas)):
    Paginas[i] = Paginas[i].replace(u'\u0160\n','').replace(u'\u0160','')

# <markdowncell>

# Import Map

# <codecell>

im = plt.imread('Mapa_300dpi.png')

# <markdowncell>

# Import Stations Coordinates

# <codecell>

coordestacoes = {}
with open('Localizacao_estacoes','r') as f:
    tuples = [i.split(',') for i in f.readlines()]
    for j,k in tuples:
        coordestacoes[j] = tuple(k.strip().split(' '))

# <markdowncell>

# Help Functions

# <codecell>

LinhaA = ['Estádio do Dragão,Campanhã,Heroísmo,Campo 24 de Agosto,Bolhão,Trindade,Lapa,Carolina Michaëlis,Casa da Música,Francos,Ramalde,Viso,Sete Bicas,Senhora da Hora']
LinhaA = LinhaA[0].split(',')
LinhaB = ['Estádio do Dragão,Campanhã,Heroísmo,Campo 24 de Agosto,Bolhão,Trindade,Lapa,Carolina Michaëlis,Casa da Música,Francos,Ramalde,Viso,Sete Bicas,Senhora da Hora,Fonte do Cuco,Custóias,Esposade,Crestins,Verdes,Pedras Rubras,Lidador,Vilar do Pinheiro,Modivas Sul,Modivas Centro,Mindelo,Espaço Natureza,Varziela,Árvore,Azurara,Santa Clara,Vila do Conde,Alto de Pega,Portas Fronhas,São Brás,Póvoa de Varzim']
LinhaB = LinhaB[0].split(',')
LinhaC = ['Campanhã,Heroísmo,Campo 24 de Agosto,Bolhão,Trindade,Lapa,Carolina Michaëlis,Casa da Música,Francos,Ramalde,Viso,Sete Bicas,Senhora da Hora,Fonte do Cuco,Cândido dos Reis,Pias,Araújo,Custió,Parque Maia,Fórum Maia,Zona Industrial,Mandim,Castêlo da Maia,ISMAI']
LinhaC = LinhaC[0].split(',')
LinhaD = ['Hospital de São João,IPO,Pólo Universitário,Salgueiros,Combatentes,Marquês,Faria Guimarães,TrindadeD,Aliados,São Bento,Jardim do Morro,General Torres,Câmara Gaia,João de Deus,D. João II,Santo Ovídio']
LinhaD = LinhaD[0].split(',')
LinhaE = ['Estádio do Dragão,Campanhã,Heroísmo,Campo 24 de Agosto,Bolhão,Trindade,Lapa,Carolina Michaëlis,Casa da Música,Francos,Ramalde,Viso,Sete Bicas,Senhora da Hora,Fonte do Cuco,Custóias,Esposade,Crestins,Verdes,Botica,Aeroporto']
LinhaE = LinhaE[0].split(',')
LinhaF = ['Fânzeres,Venda Nova,Carreira,Baguim,Campainha,Rio Tinto,Levada,Nau Vitória,Nasoni,Contumil,Estádio do Dragão,Campanhã,Heroísmo,Campo 24 de Agosto,Bolhão,Trindade,Lapa,Carolina Michaëlis,Casa da Música,Francos,Ramalde,Viso,Sete Bicas,Senhora da Hora']
LinhaF = LinhaF[0].split(',')

Cores = { 'A' : 'b', 'B' : 'r', 'C' : 'g', 'D' : 'y', 'E' : 'purple', 'F' : 'orange'}
Estacoes = { 'A' : LinhaA, 'B' : LinhaB, 'C' : LinhaC, 'D' : LinhaD, 'E' : LinhaE, 'F' : LinhaF}
Periodo = ['Dias Utéis','Sábados','Domingos e Feriados']
Hdr_splitter = {'B' : 'Trindade', 'C' : '2011/12', 'E' : 'Aeroporto', 'F' : 'Fânzeres'}
Sentidos = ['Póvoa de Varzim','Estádio do DragãoParagem','ISMAI','CAMPANHÂ','Aeroporto','Estádio do Dragão','Fânzeres','Senhora da Hora']
pgs = {'B' : 2 , 'C' : 8 , 'E' : 14, 'F' : 20}
estacaoNAS = {'B' : 'Fonte do Cuco,Custóias,Esposade,Crestins,Verdes,Lidador,Vilar do Pinheiro,Modivas Sul,Modivas Centro,Espaço Natureza,Árvore,Azurara,Santa Clara,Alto de Pega,São Brás' , 'C' : 'Zona Industrial,Mandim,Castêlo da Maia,ISMAI'}
NAS = {'B' : (range(3,6,2)+range(8,59,2),range(3,34,3),range(15,28,3)) , 'C' : (range(3,44,2)+range(47,72,2),range(6,43,2),range(16,33,2))}
NAS_inv = {'B' : (range(3,6,2)+range(8,59,2),range(3,34,3),range(15,28,3)) , 'C' : (range(3,72,2),range(4,43,2),range(14,33,2))}
pgs_hdr = ['','','Trindade','Trindade','Trindade','Trindade','Trindade','Trindade','2011/12','2011/12','2011/12','2011/12','2011/12','2011/12','Aeroporto','Estádio do Dragão','2011/12','Estádio do Dragão','2011/12','Estádio do Dragão','2011/12','Fânzeres','2011/12','Fânzeres','2011/12','Fânzeres']

# <codecell>

def fill_values_in_NA(linha,columns):
    for i in range(35,39):
        k = 0
        for n in NAS[linha][0]:
            columns[i%30].insert(n,columns[i][k])
            k += 1
    for i in range(39,43):
        k = 0
        for n in NAS[linha][0]:
            columns[i%29].insert(n,columns[i][k])
            k += 1
    k = 0
    for n in NAS[linha][0]:
        columns[19].insert(n,columns[43][k])
        k += 1
    k = 0
    for n in NAS[linha][0]:
        columns[24].insert(n,columns[44][k])
        k += 1
    k = 0
    for n in NAS[linha][0]:
        columns[26].insert(n,columns[45][k])
        k += 1
    k = 0
    for n in NAS[linha][0]:
        columns[30].insert(n,columns[46][k])
        k += 1
    k = 0
    for n in NAS[linha][0]:
        columns[32].insert(n,columns[47][k])
        k += 1
    k = 0
    for n in NAS[linha][0]:
        columns[34].insert(n,columns[48][k])
        k += 1
    k = 0
    for n in NAS[linha][0]:
        columns[9].insert(n,columns[49][k])
        k += 1
    for i in range(50,55):
        k = 0
        for n in NAS[linha][0]:
            columns[i%50].insert(n,columns[i][k])
            k += 1
    return columns

# <codecell>

def Horario_periodo_inv(estacao,periodo=-1):
    result = []
    linhas = []
    for lin,est in Estacoes.iteritems():
        if estacao in est:
            linhas.append(lin)
    for linha in linhas:
        if linha in ['A','D']:
            continue
        if periodo == -1:
            pags = [pgs[linha]+1,pgs[linha]+1+2, pgs[linha]+1+4]
        elif periodo == 'Dias Úteis':
            pags = [pgs[linha]+1]
        elif periodo == 'Sábados':
            pags = [pgs[linha]+1+2]
        else:
            pags = [pgs[linha]+1+4]
        for pg in pags:
            columns = []
            line_change = re.split(r'(\d\d:\d\d)\s*(\d:\d\d)',Paginas[pg].split(pgs_hdr[pg].decode('utf-8'))[1])
            line_change.reverse()
            if pg in [5,7]:
                line_change = line_change[line_change.index(u'5:53'):]
                line_change.append('')
            else:
                line_change.insert(0,'')
            for i in range(0,len(line_change)-2,3):
                columns.append(re.findall(r'(\d*\d:\d\d)',line_change[i]+line_change[i+1]+line_change[i+2]))
            if linha == 'B' and pg == 2:
                columns = fill_values_in_NA(linha,columns)
            else:
                pass
            columns = columns[:len(Estacoes[linha])]
            try:
                result.append(columns[Estacoes[linha].index(estacao)])   
            except:
                print 'Erro com: ',estacao,linha,Estacoes[linha].index(estacao),len(columns),len(Estacoes[linha])
    return result
            

    
def Horario_linha_inv(estacao,linha=-1):
    result = []
    linhas = []
    if linha == -1:
        for lin,est in Estacoes.iteritems():
            if estacao in est:
                linhas.append(lin)
    else:
        linhas = [linha]
        
    for linha in linhas:
        if linha in ['A','D']:
            continue
        pags = [pgs[linha]+1,pgs[linha]+1+2, pgs[linha]+1+4]
        for pg in pags:
            columns = []
            if pg == 25:
                line_change = re.split(r'(\d\d:\d\d)[\s\s\s]*(\d:\d\d)',Paginas[pg].split(pgs_hdr[pg].decode('utf-8'))[1])
            else:
                line_change = re.split(r'(\d\d:\d\d)(\d:\d\d)',Paginas[pg].split(pgs_hdr[pg].decode('utf-8'))[1])
            if pg in [7]:
                line_change = line_change[line_change.index(u'5:40'):]
                line_change.append('')
            elif pg == 3:
                line_change = line_change[line_change.index(u'5:42'):]
                line_change.append('')
            else:
                line_change.insert(0,'')
                line_change.append('')
            for i in range(0,len(line_change)-2,3):
                columns.append(re.findall(r'(\d*\d:\d\d)',line_change[i]+line_change[i+1]+line_change[i+2]))
            if linha == 'B' and pg == 3:
                tmp = []  
                for i in [0,14,1,15,2,16,17,18,3,19,4,20,21,22,23,34,24,25,26,27,28,5,6,7,8,9,10,11,12,13,29,30,31,32,33]:
                    tmp.append(columns[i])
                columns = tmp
            if linha == 'B' and pg == 2:
                columns = fill_values_in_NA(linha,columns)
                
            else:
                pass
            columns = columns[:len(Estacoes[linha])]
            try:
                result.append(columns[-Estacoes[linha].index(estacao)-1])   
            except:
                print 'Erro com: ',estacao,linha,Estacoes[linha].reverse().index(estacao),len(columns),len(Estacoes[linha])
    return result

# <codecell>

def Horario_periodo(estacao,periodo=-1):
    result = []
    linhas = []
    for lin,est in Estacoes.iteritems():
        if estacao in est:
            linhas.append(lin)
    for linha in linhas:
        if linha in ['A','D']:
            continue
        if periodo == -1:
            pags = [pgs[linha],pgs[linha]+2, pgs[linha]+4]
        elif periodo == 'Dias Úteis':
            pags = [pgs[linha]]
        elif periodo == 'Sábados':
            pags = [pgs[linha]+2]
        else:
            pags = [pgs[linha]+4]
        for pg in pags:
            columns = []
            line_change = re.split(r'(\d\d:\d\d)\s*(\d:\d\d)',Paginas[pg].split(pgs_hdr[pg])[1])
            if pg in [4,6]:
                line_change = line_change[line_change.index(u'5:53'):]
                line_change.append('')
            else:
                line_change.insert(0,'')
            for i in range(0,len(line_change)-2,3):
                columns.append(re.findall(r'(\d*\d:\d\d)',line_change[i]+line_change[i+1]+line_change[i+2]))
            if linha == 'B' and pg == 2:
                columns = fill_values_in_NA(linha,columns)
            else:
                pass
            columns = columns[:len(Estacoes[linha])]
            try:
                result.append(columns[Estacoes[linha].index(estacao)])   
            except:
                print 'Erro com: ',estacao,linha,Estacoes[linha].index(estacao),len(columns),len(Estacoes[linha])
    return result
            

    
def Horario_linha(estacao,linha=-1):
    result = []
    linhas = []
    if linha == -1:
        for lin,est in Estacoes.iteritems():
            if estacao in est:
                linhas.append(lin)
    else:
        linhas = [linha]
        
    for linha in linhas:
        if linha in ['A','D']:
            continue
        pags = [pgs[linha],pgs[linha]+2, pgs[linha]+4]
        for pg in pags:
            columns = []
            line_change = re.split(r'(\d\d:\d\d)\s*(\d:\d\d)',Paginas[pg].split(pgs_hdr[pg])[1])
            if pg in [7]:
                #line_change = line_change[line_change.index(u'5:53'):]
                line_change.append('')
            else:
                line_change.insert(0,'')
                line_change.append('')
            for i in range(0,len(line_change)-2,3):
                columns.append(re.findall(r'(\d*\d:\d\d)',line_change[i]+line_change[i+1]+line_change[i+2]))
            if linha == 'B' and pg == 2:
                columns = fill_values_in_NA(linha,columns)
            else:
                pass
                #columns = fill_values_in_NA_Sab(linha,columns)
            columns = columns[:len(Estacoes[linha])]
            try:
                result.append(columns[Estacoes[linha].index(estacao)])   
            except:
                print 'Erro com: ',estacao,linha,Estacoes[linha].index(estacao),len(columns),len(Estacoes[linha])
    return result
        
        
def Horario_estacao(estacao):
    pass

def Horario(estacao=-1, linha=-1,periodo=-1):
    if linha in ['A','D']:
        print 'Não há horario fixo'
        return []
    elif estacao == -1:
        return []
    elif linha == -1 and periodo == -1:
        return Horario_estacao(estacao)
    elif linha == -1:
        return Horario_periodo(estacao,periodo)
    elif periodo == -1:
        return Horario_linha(estacao,linha)

# <codecell>

def fill_values_in_NA_Sab(linha,columns):
    l = 0
    print columns[0]
    for n in NAS[linha][1]:
        k = 0
        for j in range(13)+[19,24,26,30,32,34]:
            columns[j+19].insert(n,columns[k][l])
            k +=1
        l+=1
    return columns[19:]

# <codecell>

def add_NA(times,estacao,linha,nperiodo):
    if linha in estacaoNAS.keys():
        if estacao in estacaoNAS[linha]:
            for i in NAS[linha][nperiodo]:
                if linha == 'B' and i == 8 and Estacoes[linha].index(estacao) > 21:
                    times.insert(7,'--')
                times.insert(i,'--')
        elif linha == 'B' and nperiodo == 0 and Estacoes[linha].index(estacao) > 21:
                times.insert(7,'--')
    return times

def add_NA_inv(times,estacao,linha,nperiodo):
    if linha in estacaoNAS.keys():
        if estacao in estacaoNAS[linha]:
            if linha == 'B' and nperiodo == 0 and Estacoes[linha].index(estacao) > 21:
                times.insert(4,'--')
                times.insert(13,'--')
            for i in NAS_inv[linha][nperiodo]:
                if linha == 'B':
                    continue
                    #and i == 8 and Estacoes[linha].index(estacao) > 21:
                    
#                    times.insert(7,'--')
                times.insert(i,'--')
        elif linha == 'B' and nperiodo == 0 and Estacoes[linha].index(estacao) > 21:
            times.insert(4,'--')
            times.insert(13,'--')
    return times
        
def Horario_row(linha,periodo):
    hor = []
    if periodo == 'Dias Úteis':
        ind = 0
        for estacao in Estacoes[linha]:
            tmp = Horario_linha(estacao,linha)[ind]
            hor.append(add_NA(tmp,estacao,linha,ind))
    elif periodo == 'Sábados':
        ind = 1
        for estacao in Estacoes[linha]:
            tmp = Horario_linha(estacao,linha)[ind]
            hor.append(add_NA(tmp,estacao,linha,ind))
    else:
        ind = 2
        for estacao in Estacoes[linha]:
            tmp = Horario_linha(estacao,linha)[ind]
            hor.append(add_NA(tmp,estacao,linha,ind))
    return np.array(hor).transpose()

def Horario_row_inv(linha,periodo):
    hor = []
    if periodo == 'Dias Úteis':
        ind = 0
        for estacao in Estacoes[linha]:
            tmp = Horario_linha_inv(estacao,linha)[ind]
            hor.append(add_NA_inv(tmp,estacao,linha,ind))
    elif periodo == 'Sábados':
        ind = 1
        for estacao in Estacoes[linha]:
            tmp = Horario_linha_inv(estacao,linha)[ind]
            hor.append(add_NA_inv(tmp,estacao,linha,ind))
    else:
        ind = 2
        for estacao in Estacoes[linha]:
            tmp = Horario_linha_inv(estacao,linha)[ind]
            hor.append(add_NA_inv(tmp,estacao,linha,ind))
    hor.reverse()
    return np.array(hor).transpose()

# <codecell>

def getcoord(estacao):
    return coordestacoes[estacao]

horrowd = {}
for linha in ['B','C','E','F']:
    horrowd[linha] = {}
    for period in ['Dias Úteis','Sábados','Domingos e Feriados']:
        horrowd[linha][period] = Horario_row(linha,period)

horrowdinv = {}
for linha in ['B','C','E','F']:
    horrowdinv[linha] = {}
    for period in ['Dias Úteis','Sábados','Domingos e Feriados']:
        horrowdinv[linha][period] = Horario_row_inv(linha,period)
        
def current_map(i,linhas=-1):
    t = datetime.datetime.today()
    period = 'Dias Úteis'
    #tstr = u'%d:%.2d'%(t.hour,t.minute)
    tstr = u'%d:%.2d'%(5+(i+40)/60,(40+i)%60)
    result,result2 = [],[]
    if linhas == -1:
        linhas = ['B','C','E','F']
    for linha in linhas:
        horrow = horrowd[linha][period]
        for row in horrow:
            if tstr in row:
                result.append((Estacoes[linha][list(row).index(tstr)],linha))
            else:
                try:
                    t2 = datetime.datetime(t.year,t.month,t.day,int(tstr.split(':')[0])%24,int(tstr.split(':')[1]))
                except:
                    print t.year,t.month,t.day,int(tstr.split(':')[0])%24,int(tstr.split(':')[1]) 
                hor = []
                if linha == 'B':
                    for sched in row:
                        if sched != '--':
                            hor.append(datetime.datetime(t.year,t.month,t.day,int(sched.split(':')[0])%24,int(sched.split(':')[1])) > t2)
                        else:
                            hor.append(False)
                else:
                    hor = [datetime.datetime(t.year,t.month,t.day,int(sched.split(':')[0])%24,int(sched.split(':')[1])) > t2 for sched in row if sched != '--']
                try:
                    k = 1
                    while hor[hor.index(True)-k] == '--' and hor.index(True)-k > 0:
                        k +=1
                    if hor[hor.index(True)-k] == False and hor.index(True)-k > -1:
                        result2.append((Estacoes[linha][hor.index(True)-k],Estacoes[linha][hor.index(True)],linha))
                except:
                    pass
        horrow = horrowdinv[linha][period]
        for row in horrow:
            if tstr in row:
                result.append((Estacoes[linha][-list(row).index(tstr)-1],linha))
            else:
                t2 = datetime.datetime(t.year,t.month,t.day,int(tstr.split(':')[0])%24,int(tstr.split(':')[1]))
                hor = []
                if linha == 'B':
                    for sched in row:
                        if sched != '--':
                            hor.append(datetime.datetime(t.year,t.month,t.day,int(sched.split(':')[0])%24,int(sched.split(':')[1])) > t2)
                        else:
                            hor.append(False)
                else:
                    hor = [datetime.datetime(t.year,t.month,t.day,int(sched.split(':')[0])%24,int(sched.split(':')[1])) > t2 for sched in row if sched != '--']
                try:
                    k = 1
                    while hor[hor.index(True)-k] == '--' and hor.index(True)-k > 0:
                        k +=1
                    if hor[hor.index(True)-k] == False and hor.index(True)-k > -1 and row[0]!='--':
                        result2.append((Estacoes[linha][-hor.index(True)],Estacoes[linha][-hor.index(True)-k],linha))
                except:
                    pass
    return result,result2

# <markdowncell>

# Plot
# =

# <codecell>

fig = plt.figure()

def init():
    plt.scatter([],[])
    return implot,

def update_plot(i):
    x, y = [],[]
    exact,intransit =current_map(i)
    plt.cla()
    implot = plt.imshow(im)
    for key,linha in exact:
        try:
            x = int(coordestacoes[key.decode('utf-8').encode('latin-1')][0])
            y = int(coordestacoes[key.decode('utf-8').encode('latin-1')][1])
            plt.scatter(x,y, c=Cores[linha], s=40)
        except:
            print 'Erro nas coordenadas exactas',key
    for est1,est2,linha in intransit:
        try:
            x = np.mean([int(coordestacoes[est1.decode('utf-8').encode('latin-1')][0]),int(coordestacoes[est2.decode('utf-8').encode('latin-1')][0])])
            y = np.mean([int(coordestacoes[est1.decode('utf-8').encode('latin-1')][1]),int(coordestacoes[est2.decode('utf-8').encode('latin-1')][1])])
            plt.scatter(x,y, c=Cores[linha], s=40)
        except:
            print 'Erro nas coordenadas em transito',est1,est2
    plt.title('%2d:%.2d'%(5+(i+40)/60,(i+40)%60))
    return implot,

ani = animation.FuncAnimation(fig, update_plot, frames=xrange(60))
#ani.save('metrodiasuteis.mp4', fps=4, clear_temp=True)
plt.show()

# <codecell>


