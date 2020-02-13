
from scheme import f
class DegreeGenerator():
    def __init__(self, w):
       self.fd = f
       self.W = w
    def getDegree(self,v):
       deg=0
       for i in range(0,len(self.fd)):
           if self.fd[i]>v:
           deg=i-1
       if deg>self.W-2:
           return self.W-2
       else:
           return deg 