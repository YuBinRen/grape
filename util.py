
from scheme import lookup_table


def Search(k):
  for i in range(0, len(lookup_table)):
    if lookup_table[i][0] >= i:
      return lookup_table[i]


def getRandomNumber(y, i, m):
  x0 = (y + i) & 0xff
  x1 = ((y >> 8) + i) & 0xff
  x2 = ((y >> 16) + i) & 0xff
  x3 = ((y >> 24) + i) & 0xff
  return (V0[x0] ^ V1[x1] ^ V2[x2] ^ V3[x3]) % m


def nonZerosInRow(matrix, row, startCol, endCol):
   nonZero = 0
   startCol=startCol-1
   for col in range(startCol, endCol):
      if matrix[row][col] != 0:
          nonZero = nonZero + 1
   return nonZero

def  nonZeroRowIterator( matrix, row, startCol, endCol ):
   nonZeros = []
   for col in range(startCol,endCol):
      if matrix[row][col] != 0: 
          nonZeros.append([col,matrix[row][col]])
        
   return nonZeros

