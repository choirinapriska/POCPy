import cv2
import numpy as np
import matplotlib.pyplot as plt  
import matplotlib.patches as patches

from tabulate import tabulate
from POC import POC as POC
from getVektor import getVektor as Vect
from getQuadran import getQuadran as Qd

# inisiasi gambar 
 
  
imgAwal = cv2.cvtColor(cv2.imread('image/imgTitik/1-2.jpg'), cv2.COLOR_BGR2GRAY) 
imgAkhir = cv2.cvtColor(cv2.imread('image/imgTitik/1-3.jpg'), cv2.COLOR_BGR2GRAY) 

# imgAwal = cv2.cvtColor(cv2.imread('image/matakiri-img96.jpg'), cv2.COLOR_BGR2GRAY) 
# imgAkhir = cv2.cvtColor(cv2.imread('image/matakiri-img117.jpg'), cv2.COLOR_BGR2GRAY)

blockSize = 9 #setting ukuran blok (harus ganjil), karena membutuhkan nilai tengah untuk titik pusat

# Untuk menampilkan gambar + arah panah
plt.imshow(np.uint8((imgAwal*0.9) + (imgAkhir*0.1)), cmap="gray")

initPOC = POC(imgAwal, imgAkhir, blockSize) #inisiasi class getPOC

valPOC = initPOC.getPOC() #pemanggilan fungsi pocCalc() untuk menghitung nilai POC disetiap gambar
 
# pemanggilan class dan method untuk menampilkan quiver / gambar panah
initQuiv = Vect(valPOC, blockSize)
quivData = initQuiv.createVektor() 

plt.quiver(quivData[:, 0], quivData[:, 1], quivData[:, 2], quivData[:, 3], scale=1, scale_units='xy', angles='xy', color="r")    

num = 0
for  rect_def in valPOC[2]:
    x, y, width, height = rect_def
    
    rects = patches.Rectangle((x,y), width,height, edgecolor='r', facecolor='none') 
    plt.gca().add_patch(rects)
    
    plt.text(x,y,f'({num})', color="blue") 
    
    num += 1
    

# Pemanggilan class untuk mengeluarkan nilai karakteristik vektor
# blok ke, x,y,tetha, magnitude, dan quadran ke
initQuadran = Qd(quivData)
quadran = initQuadran.setQuadran()

print(tabulate(quadran, headers=['Blok Ke', 'X', 'Y', 'Tetha', 'Magnitude', 'Quadran Ke']))
plt.axis('on')  # Matikan sumbu
plt.show()
