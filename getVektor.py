import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class getVektor:
    def __init__(self, pocOutput, blockSize):
        self.blockSize = blockSize
        self.poc = pocOutput[0]
        self.coorAwal = pocOutput[1]
        self.rect = pocOutput[2]

    def createVektor(self):
        mb_x = self.blockSize  # panjang macroblock
        mb_y = self.blockSize  # lebar macroblock

        cur_x = np.arange(0, mb_x)
        cur_y = np.arange(0, mb_y)

        nilTeng = np.int16(np.median(cur_x))
        medX = nilTeng
        medY = nilTeng

        rep_x = np.arange(-(nilTeng), nilTeng+1)   
        rep_y = np.arange(nilTeng, -(nilTeng+1), -1) 

        output = np.empty((len(self.rect), 6))

        valPOC = self.poc

        for i in range(valPOC.shape[2]):
            r = valPOC[:, :, i]
            rects = patches.Rectangle((self.rect[i,0], self.rect[i,1]), self.rect[i,2], self.rect[i,3], edgecolor='r',
                                      facecolor='none')

            temp_y, temp_x = np.where(r == np.max(r))

            if np.all(r == r[0,0]) or len(temp_x) >= mb_x : 
                output[i, :] = 0
            else:
                temp_y = temp_y[0]  # Assuming nilTeng is defined elsewhere
                temp_x = temp_x[0]

                if temp_x == nilTeng and temp_y == nilTeng : 
                    output[i,:] = 0
                else : 
                    corX = self.coorAwal[i][0]  # koordinat X mulai
                    corY = self.coorAwal[i][1]  # koordinat Y mulai

                    tX = corX - medX
                    tY = corY - medY

                    oX = rep_x[cur_x[temp_x]]
                    oY = rep_y[cur_y[temp_y]]

                    mX = corX - (mb_x - temp_x)
                    mY = corY - (mb_y - temp_y)

                    p1 = [tX, tY]
                    p2 = [mX, mY]
                    V = np.int8(np.array(p2) - np.array(p1))

                    output[i, 0] = p1[0]
                    output[i, 1] = p1[1]
                    output[i, 2] = V[0]
                    output[i, 3] = V[1]
                    output[i, 4] = oX
                    output[i, 5] = oY 

                    print(p1)
                    print(p2)
                    print(V)
                    print('----------------------------------------') 
            
                
            plt.gca().add_patch(rects)
        
        return output
