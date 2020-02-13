

def   Encode1( IS, d, a, b, d1, a1, b1, W, P, P1, MO,i):
    
    result = IS[b]
    
    for j in range(0,d):
        b = (b + a) % W
        
        
        result = MO.vectorVectorAddition(result, IS[b])

    while (b1 >= P):
        b1 = (b1 + a1 ) % P1
    
    result = MO.vectorVectorAddition(result, IS[W + b1])
    
    
    for j in range(0, d1-1):
        b1 = (b1 + a1)% P1
        while (b1 >= P):
            b1 = (b1 + a1 ) % P1
        result = MO.vectorVectorAddition(result, IS[W + b1])
    return result

