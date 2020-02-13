

def swapVector(vector, target, source):
    temp = vector[source]
    vector[source] = vector[target]
    vector[target] = temp
    return vector
