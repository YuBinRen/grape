import numpy as np
from RowObject import RowObject 
from util import nonZerosInRow,nonZeroRowIterator
from octextMath import octetmath
from phase2 import phase2
from phase3 import phase3
from swapVector import swapVector
from mode import mode

def phase1(matrixA, D, P, L, S, H, k):
  r, M = matrixA.shape
  i = 0
  u = P
  matrixX = matrixA.copy()
  d=np.linspace(0,len(matrixA)-1,len(matrixA-1),dtype=np.int)
  c = d.copy()
  keyss = []
  values = []
  for row  in range(0, r):
       ro = RowObject()
       ro.index = row
       ro.nonzeros = nonZerosInRow(matrixA, row, 1, L - u)
       
       if (row >= S) and (row < S + H ):
           ro.isHDPC = 1
       else:
           ro.isHDPC = 0

       nonZerosArr = nonZeroRowIterator(matrixA, row, 1, L - u)
       if (ro.nonzeros == 2) and (ro.isHDPC == 0):
           for n in range(0,len(nonZerosArr)):
               cellarr = nonZerosArr[n]
               ro.degree = ro.degree ^ cellarr[1]
               ro.nodes.append(cellarr[0])     
       else:
           od = 0
           for n in range(0,len(nonZerosArr)):
               od = od + nonZerosArr[n][1] 
           ro.degree = od
       
       keyss.append(row)
       values.append(ro)

  keyss=np.array(keyss).reshape(len(keyss),1)

  columnMap={} #keyss->values
  for i1 in range(0,len(values)):
      columnMap[i1]=values[i1]

  nonHDPCRows = S + k

  chosenRowsCounter = 0
  MO = octetmath()
  index=0
  while (i + u) < L:
    mindegree = 256 * L
    r = L + 1
    ro = RowObject()
    two1s = 0
    keyss = list(columnMap.keys())
    allzeros = 1

    for ct in range(0,len(keyss)):
        row = columnMap[keyss[ct]]
        if row.nonzeros != 0:
            allzeros = 0
        
        if (row.isHDPC == 1) and (chosenRowsCounter < nonHDPCRows):
            continue
        if len(row.nodes)!=0:
            two1s=1
        if (row.nonzeros < r) and (row.nonzeros > 0):
            ro = row
            r = ro.nonzeros
            mindegree = ro.degree
        elif (row.nonzeros == r) and (row.degree < mindegree):
            ro = row
            mindegree = ro.degree  
    if (r == 2) and (two1s == 1):
        ro = 0
        noderows = []
        nodes = []
        for ct  in range(0,len(keyss)):
            row = columnMap[keyss[ct]]
            if len(row.nodes) !=0:
                noderows.append(row)
                noderows.append(row)
                nodes.extend(row.nodes)
        target = mode(nodes)
        for ct in range(0, len(nodes)):           
            if target == nodes[ct]:
                ro = noderows[ct]
                break  

    chosenRowsCounter = chosenRowsCounter + 1
    
    if ro.index!= i:
      
        matrixA[[i, ro.index], :] = matrixA[[ro.index,i], :]
        matrixX[[i, ro.index], :] = matrixX[[ro.index,i], :]
        d = swapVector(d, i, ro.index)
        other = columnMap[i]
        other.index = ro.index
        columnMap[ro.index]= other
        del columnMap[i]
        ro.index = i
    nonZeroPos = nonZeroRowIterator(matrixA, i, i, L - u)

    firstNZpos = nonZeroPos[0][0]
    
    if firstNZpos!= i:
        matrixA[:,[i,firstNZpos]] = matrixA[:,[firstNZpos,i]]
        matrixX[:,[i,firstNZpos]] = matrixX[:,[firstNZpos,i]]
        c = swapVector(c, i, firstNZpos)
    currCol = L - u-1
    nzp, ignore= len(nonZeroPos)-1,2
    while nzp > 0:
        currNZpos = nonZeroPos[nzp][0]
        if currCol != currNZpos:
            matrixA[:,[currCol,currNZpos]] = matrixA[:,[currNZpos,currCol]]
            matrixX[:,[currCol,currNZpos]] = matrixX[:,[currNZpos,currCol]]
            c = swapVector(c, currCol, currNZpos)
        nzp = nzp - 1
        currCol = currCol - 1
    alpha = matrixA[i][i]
    
    for row in range(i+1, M):
        beta = matrixA[row][i]
        
        if beta == 0:
            continue
        else:
            bOA = MO.divide(beta, alpha)   
            matrixA = MO.addRowsInPlace(matrixA, bOA, i, row)
            D = MO.addRowsInPlace(D, bOA, d[i], d[row])
    i = i + 1
    u = u + r - 1
    keyss = list(columnMap.keys())
    for ct in range(0, len(keyss)):
        row = columnMap[keyss[ct]]
        row.nonzeros = nonZerosInRow(matrixA, row.index, i, L - u)
        row.nodes = []
        if(row.nonzeros != 2) or  (row.isHDPC == 1):
            continue
        else:
            it = nonZeroRowIterator(matrixA, row.index, i, L - u)
            for bb in range(0,len(it)):
                cellarr = it[bb]
                row.nodes.append(cellarr[0])
    index+=1
   
  matrixA, d, D = phase2(matrixA, D, d, i, M, L - u + 1, L, MO)
  C = phase3(matrixA, matrixX, D, d, c, L, i, MO)
  return C
 