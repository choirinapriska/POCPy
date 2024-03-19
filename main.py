import cv2
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

from POC import POC as POC
from getVektor import getVektor as Vect
from getQuadran import getQuadran as Qd

# inisiasi gambar
imgBlockCur = cv2.cvtColor(cv2.imread('image/imgTitik/5-1.jpg'), cv2.COLOR_BGR2GRAY) 
imgBlockRef = cv2.cvtColor(cv2.imread('image/imgTitik/5-2.jpg'), cv2.COLOR_BGR2GRAY)

# imgBlockCur = cv2.cvtColor(cv2.imread('image/matakiri-img96.jpg'), cv2.COLOR_BGR2GRAY) 
# imgBlockRef = cv2.cvtColor(cv2.imread('image/matakiri-img117.jpg'), cv2.COLOR_BGR2GRAY)

blockSize = 7 #setting ukuran blok (harus ganjil), karena membutuhkan nilai tengah untuk titik pusat

initPOC = POC(imgBlockCur, imgBlockRef, blockSize) #inisiasi class getPOC

valPOC = initPOC.getPOC() #pemanggilan fungsi pocCalc() untuk menghitung nilai POC disetiap gambar

# Untuk menampilkan gambar + arah panah
plt.imshow(np.uint8((imgBlockCur*0.9) + (imgBlockRef*0.1)), cmap="gray")

# pemanggilan class dan method untuk menampilkan quiver / gambar panah
initQuiv = Vect(valPOC, blockSize)
quivData = initQuiv.createVektor()

plt.quiver(quivData[:, 0], quivData[:, 1], quivData[:, 2], quivData[:, 3], scale=1, scale_units='xy', angles='xy', color="r", pivot='middle')    

# Pemanggilan class untuk mengeluarkan nilai karakteristik vektor
# blok ke, x,y,tetha, magnitude, dan quadran ke
initQuadran = Qd(quivData)
quadran = initQuadran.setQuadran()
print(tabulate(quadran, headers=['Blok Ke', 'X', 'Y', 'Tetha', 'Magnitude', 'Quadran Ke']))


plt.axis('on')  # Matikan sumbu
plt.show()
