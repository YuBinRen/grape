

from encoder import Encoder
import numpy as np
np.set_printoptions(linewidth=380)

kitty =[82,97,112,116,111,114,81]
Encode=Encoder(kitty,0.5,2)

internate=Encode.makeRepairSymbols()
row,col= internate.shape
for i in range(0,row):
    
    print(internate[i,0:10])