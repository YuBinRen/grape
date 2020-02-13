

import numpy as np
from phase4 import phase4

def phase3(matrixA, matrixX, D, d, c, L, i, octmath):
     Arows = i
     Acols = L
     Xrows = Arows
     Xcols = Arows
    
     temp1=np.zeros((Xrows,Xcols),dtype=np.int)
     temp2=np.zeros((Arows,Acols),dtype=np.int)
     for i in range(0,Xrows):
         for ii in range(0,Xcols):
             temp1[i][ii]=matrixX[i][ii]
     for i in range(0,Arows):
         for ii in range(0,Acols):
             temp2[i][ii]=matrixA[i][ii]


     matrixA = octmath.multiplyMatrix(temp1, temp2)
    
     ignore, lenD = D.shape
     DM = np.zeros((Xrows, lenD), dtype=np.int)
     
     for row in range(0, Xrows):
         DM[row] = D[d[row]]

     for t in range(0, Xrows):
         temp3=[]
         for i in range(0,Xrows):
             temp3.append(matrixX[t][i])
         D[d[t]] = octmath.multiplyRow(temp3, DM)
  
     C = phase4(matrixA, D, d, c, L, i, octmath)
     
     return C
