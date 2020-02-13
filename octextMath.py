from scheme import OCT_EXP, OCT_LOG
import numpy as np


class octetmath():
    def __init__(self):
     self.logArray = OCT_LOG
     self.expArray = OCT_EXP

    def log(self, number):
      return self.logArray[number]

    def exp(self, number):
      return self.expArray[number]

    def multiply(self, octet1, octet2):
        if octet1 == 0 or octet2 == 0:
            return 0
        else:
            return self.exp(self.log(octet1)+self.log(octet2))

        pass

    def divide(self, octet1, octet2):
        if octet1 == 0:
            return 0
        else:
            return self.exp(self.log(octet1) - self.log(octet2) + 255)

    def addRowsInPlace(self, matrix, bOA, sourceRow, destRow):

        r, c = matrix.shape
        for i in range(0, c):
            matrix[destRow][i] = (matrix[destRow][i]) ^ self.multiply(
                bOA, matrix[sourceRow][i])
        return matrix

    def divideRowInPlace(self, matrix, row, dividend):
        r, c = matrix.shape
        for i in range(0, c):
            matrix[row][i] = self.divide(matrix[row][i], dividend)
        return matrix
    def divideRowsInPlace(self, matrix, r, beta):
        ignore, c = matrix.shape
        for i in range(0, c):
            matrix[r][i] = self.divide(matrix[r][i], beta)
        return matrix
    def multiplyMatrix(self, matrixA, matrixB):
        mr, mc = matrixA.shape
        mrb, mcb = matrixB.shape
        matrix = np.zeros((mr, mcb), dtype=np.int)
        for row in range(0, mr):
           for col in range(0, mcb):
                for x in range(0, mc):
                    temp = self.multiply(matrixA[row][x], matrixB[x][col])
                    matrix[row][col] = matrix[row][col] ^ temp
        return matrix
    def multiplyRow(self, matRow, multiplicant):
        numRows, numCols = multiplicant.shape
        matlen = len(matRow)
        matrix = []
        for i in range(0,numCols):
            matrix.append(0)
        for rs in range(0, numCols):
            for c in range(0, matlen):
                temp = self.multiply(matRow[c], multiplicant[c][rs])
                matrix[rs] = matrix[rs] ^ temp
        return matrix
    def vectorVectorAddition(self, vec, target):
        for i in range(0, len(vec)):
            vec[i] = vec[i] ^ target[i]
        return vec
    def alphaToI(self, i):
       return self.exp[i]

    def GaloisMultiply(self, matA, matB):
         matArow, matAcol = matA.shape
         matBrow, matBcol = matB.shape
         matAns = np.zeros((matArow, matBcol))
         for row in range(0, matArow):
              for col in range(0, matBcol):
                 matAns[row][col] = self.time(matA[row], matB[:, col])
         return matAns

    def time(self, vec1, vec2):
       m = 0
       for i in range(0, len(vec1)):
            m = m ^ self.multiply(vec1[i], vec2[i])
       return m
