
import numpy as np


def phase5(matrixA, D, d, c, L, i, MO):
    Lr, Lc = D.shape
    C = np.zeros((Lr, Lc), dtype=np.int)
    ss,dd=D.shape
    for j in range(0, i+1):
       beta = matrixA[j][j]
       if beta != 1:
            matrixA = MO.divideRowInPlace(matrixA, j, beta)
            D = MO.divideRowInPlace(D, d[j], beta)
       for eL in range(0, j):
            beta = matrixA[j][eL]
            if (beta == 0):
                continue
            else:
              D = MO.addRowsInPlace(D, beta, d[eL], d[j])
    for index in range(0, L):
        C[c[index]] = D[d[index]]

    return C
