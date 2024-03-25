import numpy as np

class getQuadran:
    def __init__(self, coorData) :
        self.dataA = coorData[:, 4]
        self.dataB = coorData[:, 5]
    
    def setQuadran(self):
        Quadran = np.empty((len(self.dataA), 6), dtype=object)

        for i in range(len(self.dataA)):
             
            X = self.dataA[i]
            Y = self.dataB[i]

            tetha = np.degrees(np.arctan2(Y,X)) + 360*(Y<0)
            magnitude = np.sqrt(np.power(X,2) + np.power(Y,2))

            qdLabel = ''

            if X != 0 and Y != 0:
                if tetha >= 0 and tetha < 90:
                    qdLabel = 'Q1'
                elif tetha >= 90 and tetha < 180:
                    qdLabel = 'Q2'
                elif tetha >= 180 and tetha < 270 : 
                    qdLabel = 'Q3'
                elif tetha >= 270 and tetha < 360:
                    qdLabel = 'Q4'
                else :
                    qdLabel = 'No Quadran'
            else :
                qdLabel = 'No Quadran'

            Quadran[i, :] = [ np.str_(i) ,X, Y, tetha, magnitude, qdLabel]

        return Quadran
        
         
         
         