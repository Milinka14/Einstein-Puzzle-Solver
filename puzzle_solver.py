import re
import copy
import numpy as np

m = int(input())
n = int(input())


def provjeracvorovabolja(fmatrica,fodnosi,fn = n, fm = m):
    for k in range(len(fodnosi)):
        ime = fodnosi[k][0]
        for j in range(0,n):
            if ime == fmatrica[fodnosi[k][3]][j]:
                if  fmatrica[fodnosi[k][5]][j] == fodnosi[k][1]:
                    if fodnosi[k][2] == "-":
                        return False
                elif fmatrica[fodnosi[k][5]][j] != fodnosi[k][1] and fmatrica[fodnosi[k][5]][j] != "None":
                    if fodnosi[k][2] == "+":
                        return False
    return True


unosi = []
matrica1 = []
for i in range(0,m):
    unoss = input().split(",")
    if i == 0:
        matrica1.append(unoss)
    unosi.append(unoss)
for i in range(1,m):
    pomocna = []
    for j in range(0,n):
        pomocna.append("None")
    matrica1.append(pomocna)
odnosi = []
br = 0
while True:
    unos = input()
    if unos == "":
        break
    odnosi1 = re.findall(r"[\w']+", unos) + re.findall(r"[+\-]", unos)
    for i in range(0,m):
        for j in range(0,n):
            if unosi[i][j] == odnosi1[0]:
                odnosi1.append(i)
                odnosi1.append(j)
            if unosi[i][j] == odnosi1[1]:
                odnosi1.append(i)
    odnosi.append(odnosi1)

for k in range(m-1):
    for j in  range(len(odnosi)):
        ime1 = odnosi[j][0]
        odnos1 = odnosi[j][1]


class cvor:
    def __init__(self,data,codnosi):
        self.data = data
        self.granase = provjeracvorovabolja(data, codnosi)
        self.children = []
        self.parent = None

root = cvor(matrica1, odnosi)
stek = [root]
br =0
while stek:
    trenutni = stek.pop()
    if trenutni.granase == False:
        continue
    for i in range(1,m):
        for j in range(0,n):
            for k in range(len(unosi[i])):
                flag = True
                for j1 in range(n):
                    if trenutni.data[i][j1] == unosi[i][k]:
                        flag = False
                        break
                if flag == False:
                    continue
                if trenutni.data[i][j] == "None":
                    sindata = [row[:] for row in trenutni.data]
                    sindata[i][j] = unosi[i][k]
                    sin = cvor(sindata, odnosi)
                    sin.parent = trenutni
                    trenutni.children.append(sin)
                    br += 1
    stek.extend(trenutni.children)
print(br)

dubina = (m-1)*n + 1

def najdublji_elementi(froot):
    br = 0
    q = [froot]
    flag1 = False
    visina = 0
    while q:
        for i in range(len(q)):
            if visina == dubina - 1:
                flag1 = True
                break
            tekuci1 = q.pop(0)
            if visina<dubina-1:
                for kid in tekuci1.children:
                    q.append(kid)
        if flag1 == True:
            break
        visina += 1
    for i in range(len(q)):
        if q[i-br].granase == False:
            q.remove(q[i-br])
            br += 1
    return q

rje = najdublji_elementi(root)

rjesenja = []
for i in range(len(rje)):
    rjesenja.append(rje[i].data)
rjesenja1 = []
for matrica in rjesenja:
    if matrica not in rjesenja1:
        rjesenja1.append(matrica)


def postorder(korjen):
    q  = [korjen]
    while q:
        for i in range(len(q)):
            tekuci = q.pop(0)
            print(tekuci.data,tekuci.granase)
            if tekuci.granase == True:
                for i in range(0,len(tekuci.children)):
                    q.append(tekuci.children[i])
        print("\n")

def preorder(froot):
    q  = [froot]
    while q:
        for i in range(len(q)):
            tekuci = q.pop(0)
            print(tekuci.data,tekuci.granase)
            if tekuci.granase == False:
                print("\n")
            if tekuci.granase == True:
                for i in range(len(tekuci.children)-1,-1,-1):
                    q.insert(0, tekuci.children[i])


def printanjerijesenja(dno,rjesenja):
    patevi = []
    for rjesenje in rjesenja:
        for elem in dno:
            if rjesenje == elem.data:
                put = []
                trenutni = elem
                while trenutni != None:
                    put.append(trenutni.data)
                    trenutni = trenutni.parent
                put.reverse()
                patevi.append(put)
                break
    for i in range(len(patevi)):
        for j in range(len(patevi[i])):
            print(patevi[i][j])
            if j != len(patevi[i])-1:
                print("                                     ↓")
        print("\n")


print("\n")

def igranje_igre(fmatrica,frjesenja,fm,fn,froot):
    brojac = 0
    matricaIgra = copy.deepcopy(fmatrica)
    while True:
        print("Unesite 1 ako zelite da odustanete")
        print("Unesite 2 ako zelite da unesete pojam")
        print("Unesite 3 ako zelite da trazite pomoc")
        unos1 = input()
        if unos1 == "1":
            break
        if unos1 == "2":
            brojac += 1
            unos4 = input("Koji pojam zelite da uneste ")
            unos3 = input("U koju vrstu i kolonu zelite da unesete pojam ").split(",")
            matricaIgra[int(unos3[0])][int(unos3[1])] = unos4
            flag1 = True
            if len(frjesenja) != 0:
                for k in range(len(frjesenja)):
                    if matricaIgra[int(unos3[0])][int(unos3[1])] == frjesenja[k][int(unos3[0])][int(unos3[1])]:
                        flag1 = True
                        break
                    else:
                        pass
                else:
                    flag1 = False
                for row in matricaIgra:
                    print(*row)
                if flag1 == True and brojac == (fm-1)*fn:
                    print("Uspijesno ste uparili pojmove.")
                    break
                if flag1 == True:
                    print("Na dobrom ste putu")
                    continue
                if flag1 == False:
                    print("Unos vas ne vodi ka rijesenju. Probajte ponovo")
                    matricaIgra[int(unos3[0])][int(unos3[1])] = "None"
                    brojac -= 1
                    continue
            else:
                for row in matricaIgra:
                    print(*row)
                print("Unos vas ne vodi ka rijesenju. Probajte ponovo")
                matricaIgra[int(unos3[0])][int(unos3[1])] = "None"
                continue

        if unos1 == "3":
            if len(frjesenja) != 0:
                brojac += 1
                fq = [froot]
                flag = True
                flag1 = True
                flag2 = True
                flag3 = True
                flag4 = True
                while fq:
                    if flag4 == False:
                        break
                    for k in range(len(fq)):
                        if flag3 == False:
                            flag4 = False
                            break
                        trenutni = fq.pop(0)
                        jednake = np.array_equal(trenutni.data, matricaIgra)
                        if jednake == True:
                            for i in range(fm):
                                if flag2 == False:
                                    flag3 = False
                                    break
                                for j in range(fn):
                                    if flag1 == False:
                                        flag2 = False
                                        break
                                    if matricaIgra[i][j] == "None":
                                        lista = trenutni.children
                                        for elem in lista:
                                            listaindeksa = []
                                            br = 0
                                            dodajemo = True
                                            mflag = True
                                            if flag == False:
                                                flag1 = False
                                                break
                                            if elem.granase == True:
                                                matra = elem.data
                                                dodajemo = True
                                                for d in range(len(frjesenja)):
                                                    flagp = True
                                                    for p in range(fm):
                                                        if flagp == False:
                                                            flagd = False
                                                            break
                                                        for s in range(fn):
                                                            if matra[p][s] == frjesenja[d][p][s] or matra[p][s] == "None":
                                                                dodajemo = True
                                                            else:
                                                                dodajemo = False
                                                                flagp = False
                                                                break
                                                    if dodajemo == True:
                                                        matricaIgra[i][j] = frjesenja[d][i][j]
                                                        flag = False
                                                        break
                        for kid in trenutni.children:
                            fq.append(kid)
                if brojac == (fm-1)*fn:
                    for row in matricaIgra:
                        print(*row)
                    print("Uspijesno ste uparili pojmove.")
                    break
                for row in matricaIgra:
                    print(*row)
            else:
                print("Ne mozemo vam pomoci jer zagonetka nema rijesenja.")
print("IGRANJE IGRE")
while unos != "4":
    print("Za printanje stabla unesite 1")
    print("Za ispis rijesenja unesite 2")
    print("Za odigravanje igre unesite 3")
    print("Za zavrsetak program unesite 4")
    print("Zagonetka nema rijesenja 5")
    unos = input()
    if unos == "1":
        preorder(root)
    if unos == "2":
        print(len(rje))
        if len(rje) == 0:
            print("NEMA RJESENJA !!!!!")
        printanjerijesenja(rje, rjesenja1)
    if unos == "3":
        igranje_igre(matrica1,rjesenja1,m,n,root)
    if unos == "4":
        exit()
    if unos == "5":
        if len(rjesenja1) == 0:
            print("Pravilno ste rijesili zadatak")
            break
        else:
            print("Program ima ", len(rjesenja1) , ",pogresno ste rijesili")
            break
