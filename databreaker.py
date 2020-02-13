
import numpy as np
np.set_printoptions(linewidth=380)
def databreaker(rawdata, paylen):
    data=np.zeros((27,paylen),dtype=np.int)
    count=0
    for i in range(0,len(rawdata)):
        data[17][i]=rawdata[i]
        count+=1
    pading=paylen-count
    return data,pading

    
# import numpy as np
# import math
# np.set_printoptions(linewidth=380)
# def databreaker(rawdata, paylen):
#     matdata = []
#     length = len(rawdata)
#     numOfPackets = math.floor(length / paylen)
#     reminding = length % paylen
#     numOfzeros = 0
#     data=np.zeros((1,paylen),dtype=np.int)
    
#     statpt=1
#     endpt=paylen
#     for i in range(0,numOfPackets):
#         if i==0:
#             statpt=1
#             endpt=paylen
#         else:
#             startpt = (i - 1) * paylen + 1
#             endpt = i * paylen
#         matdata.extend(rawdata[startpt:endpt])

#     if(reminding > 0):
#         numOfzeros = paylen - reminding
#         paddeddata = rawdata[length - reminding + 1 : length]
#         for n in range(numOfzeros):
#             paddeddata.append(0)
        
#         matdata.extend(paddeddata)
#     return (matdata,numOfzeros)