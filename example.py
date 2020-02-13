

from encoder import Encoder
import numpy as np
np.set_printoptions(linewidth=380)

kitty =[82,97,112,116,111,114,81,1,2,3,4,54,43,44]
Encode=Encoder(kitty,0.5,2)
Encode.Encode()
print(Encode.Decode())
