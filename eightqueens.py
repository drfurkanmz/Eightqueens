import time

import numpy as np        
import random


class quen:
    
    def __init__(self, xkonum, ykonum, taslar,id):
        self.xkonum = xkonum 
        self.ykonum = ykonum   # konumu    
        self.taslar=taslar  # gidebileceği yerler   
        self.id=id          # hangi vezir olduğu

def tahtaolustur():
    # Aynı sütunda başka bir vezir var mı kontrol et
    secilen_sutunlar = []
    tahta = np.full((8, 8), "*", dtype=str)
 
    for satir in range(8):
        while True:
            sutun = random.randint(0, 7)
            if sutun not in secilen_sutunlar:  # Aynı sütunda daha önce vezir yoksa
                konumu=[satir,sutun]

                
                secilen_sutunlar.append(sutun)
                globals()[satir] = quen(konumu[0],konumu[1],gidebilcekyer(konumu[0],konumu[1]),satir)  # Farklı isimli nesneleri oluştur
                
                tahta[satir][sutun] = globals()[satir].id
                break

    return tahta   

def gidebilcekyer(xkonum,ykonum):
    x = xkonum
    y = ykonum
    hareketler = []

    # Dikey hareketler
    for i in range(8):
        if i != x:
            hareketler.append((i, y))

    # Yatay hareketler
    for j in range(8):
        if j != y:
            hareketler.append((x, j))

     #ÜST Çapraz hareketler
    for k in range(x):
        z=k+1
        if y==0 and ((y+z)<8) and ((x-z)>=0):
            hareketler.append((x-z,y+z))
        elif y==7 and ((y-z)>=0) and ((x-z)>=0) :
            hareketler.append((x-z,y-z))
        else :
            if ((y-z)>=0) and ((x-z)>=0):
                hareketler.append((x-z,y-z))
            if ((y+z)<8) and ((x-z)>=0):

                hareketler.append((x-z,y+z))
    # ALT Çapraz hareketler
    for l in range(7-x):
        z=l+1
        if y==0 and ((y+z)<8) and ((x+z)<8): #sağ alt
            hareketler.append((x+z,y+z))
        elif y==7 and ((y-z)>=0) and ((x+z)<8):
            hareketler.append((x+z,y-z))
        else  :
            if ((y-z)>=0) and ((x+z)<8):
                hareketler.append((x+z,y-z))
            if ((y+z)<8) and ((x+z)<8):
                hareketler.append((x+z,y+z))
           

    return hareketler

def tahtaguncelle (tahta,old,new):
    x,y=old[0],old[1]   
    f,d=new[0],new[1]
    for i in range (8):
        if (globals()[i].ykonum == y):
            surulenvezir = i #hangi vezir oldugu bulundu

    

    a=tahta[x][y]
    tahta[x][y]=tahta[f][d]
    tahta[f][d]=a

    #taşın yeri değişti
    
    
    
    
    globals()[surulenvezir].xkonum=f
    globals()[surulenvezir].ykonum=d
    
    globals()[surulenvezir].taslar= gidebilcekyer(globals()[surulenvezir].xkonum,globals()[surulenvezir].ykonum) #vezirin degerleri degisti
    
    return tahta

def yemesayisi():
    sayac=0
    for i in range (8):
        a=globals()[i].xkonum
        b=globals()[i].ykonum

        for j in range (8):
            for k in globals()[j].taslar:
                
                if k == (a,b) :
                    
                    sayac = sayac + 1  

        
    return sayac/2

def hillclimb (tahta):
    
    min=yemesayisi()

    degisecekeskikonum=[]
    degisecekyenikonum=[]

    for i in range (8):
        ilkkonum=[]

        ilksatir = globals()[i].xkonum #işleme almadan önce ilk konumu tuttum
        ilksutun = globals()[i].ykonum

        ilkkonum.append(ilksatir)
        ilkkonum.append(ilksutun)

        for j in range (8):
            if j != globals()[i].xkonum:
                yenikonum =[]
                yenikonum.append(j)
                yenikonum.append(ilksutun)

                tahtaguncelle(tahta, ilkkonum, yenikonum) # tabloyu güncelleştirdim
                guncelyeme = yemesayisi()

                if ( guncelyeme<min ):
                    degisecekeskikonum.clear()
                    degisecekyenikonum.clear()
                    
                    min=guncelyeme

                    degisecekeskikonum.append(i)
                    degisecekeskikonum.append(ilksutun)

                    degisecekyenikonum.append(j)
                    degisecekyenikonum.append(ilksutun)
                    
                
                tahtaguncelle(tahta, yenikonum, ilkkonum)
    if (len(degisecekeskikonum)>0 and len(degisecekyenikonum)>0):
        tahtaguncelle(tahta,degisecekeskikonum,degisecekyenikonum)




i=0
denemesayisi=[]
restartsayisi=[]
times=[]
while i < 15:
    start_time = time.time()

    tahta1=tahtaolustur()

    denemesayisi.insert(i,0)
    restartsayisi.insert(i,0)
    times.insert(i,0)

    while (True):
        guncelyeme=yemesayisi()
        hillclimb(tahta1)
        denemesayisi[i]+=1
        
        yenisayi=yemesayisi()
        
        if (yenisayi==guncelyeme):
            tahta1=tahtaolustur()
            
            restartsayisi[i]+=1

        if (yenisayi==0):
            end_time = time.time()
            times[i]= end_time - start_time


            break

    i=i+1
    
denemetoplam=0
restartoplam=0
timetoplam =0
for i in denemesayisi:
    denemetoplam+=i

for i in restartsayisi:
    restartoplam+=i

for i in times:
    timetoplam+=i
    
for i in range (15):
    print(i+1,". COZUM ICIN DENEME SAYISI: ",denemesayisi[i],",  RESTART SAYISI: ",restartsayisi[i],",  SURESI: ",times[i])

print("ORTALAMALAR: Deneme icin:", denemetoplam/15,", Restart icin", restartoplam/15, ", Time icin ", timetoplam/15 ) 