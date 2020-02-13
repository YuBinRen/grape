
from phase5 import phase5
def phase4(matrixA, D, d, c, L, i, MO):
  for row in range(0, i +1): #
     for col in range(i+1, L):
           b = matrixA[row][col]
           if b == 0:
               continue
           else:
               D = MO.addRowsInPlace(D, b, d[col], d[row])
 
 
 
  C = phase5(matrixA, D, d, c, L, i, MO)
  return C
