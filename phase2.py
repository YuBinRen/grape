
from swapVector import swapVector
from mode import mode

def  phase2(matrixA, D, d, fromRow, toRow, fromCol, toCol, MO ):

   fromCol=fromCol-1
   lead = fromCol

   for row in range(fromRow,toRow):
    beta=0
    if lead > toCol:
        return
    
    cr = row

    while matrixA[cr][lead] == 0:
        cr = cr + 1
        if cr == toRow:
            cr = row
            lead = lead + 1
               
    if  cr != row:
        matrixA[[cr, row],:] = matrixA[[row,cr],:]
        d = swapVector(d, cr, row)
        beta = matrixA[row][lead]
    else:
        beta = matrixA[cr][lead]
     
    if beta != 0:
        matrixA = MO.divideRowsInPlace(matrixA, row, beta)
        D = MO.divideRowsInPlace(D, d[row], beta)

    for r in range(fromRow,toRow):
        if row != r:
            beta = matrixA[r][lead]
            matrixA = MO.addRowsInPlace(matrixA, beta, row, r)
            D = MO.addRowsInPlace(D, beta, d[row], d[r])
    lead = lead + 1
  
   return [ matrixA, d, D ]
