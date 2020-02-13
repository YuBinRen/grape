
from databreaker import databreaker
from octextMath import octetmath
import math
import numpy as np
from util import Search
from scheme import V0, V1, V2, V3, OCT_EXP, OCT_LOG, f
from phase1 import phase1
from Encode import Encode1
# 矩阵布局如下,除了HDPC部分外其余的元素只有0和1两种
#             B          S        U        H
# S  |-----LDPC1----|---I_S---|-----LDPC2------|
# H  |----------HDPC----------------|---I_H----|
# K  |---------------GENC----------------------|


class Encoder():
   def __init__(self, kitty, erasureRate, overhead, PAY_LEN=368):
        self.SourceSymbols, self.numPadding = databreaker(kitty, PAY_LEN)
        self.datalen=len(kitty)
        r,c=self.SourceSymbols.shape
        self.SourceSymbols1=np.zeros((r,c),dtype=np.int)
        for i in range(0,r):
            for ii in range(0,c):
                self.SourceSymbols1[i][ii]=self.SourceSymbols[i][ii]
        self.numSouceSymbols, self.ignore = self.SourceSymbols.shape
        self.numOfRepairSymbols = math.ceil(1 * erasureRate) + overhead
        self.PAY_LEN=PAY_LEN
        self.RepairSymbols = np.zeros(
            (self.numOfRepairSymbols, PAY_LEN), dtype=np.int)
        k_prime, J, S, H, W = Search(self.numSouceSymbols)
        self.octetmath = octetmath()
        self.K = k_prime
        self.J = J
        self.S = S
        self.H = H
        self.W = W
        self.L = self.K+self.S+self.H  # 27
        self.P = self.L-self.W         # 10
        self.U = self.P-self.H         # 0
        self.P1 = self.P+1             # 1，P1是大于P的最小质数
        self.B = self.W-self.S         # 10
        self.matrix = np.zeros(
            (self.B+self.S+self.U+self.H, self.H+self.S+self.K), dtype=np.int)
        self.make_LDPC1()
        self.make_identity()
        self.make_LDPC2()
        self.make_HDPC()
        self.make_ENC()

   def makeIntermediateSymbol(self):
       return phase1(self.matrix, self.SourceSymbols, self.P, self.L, self.S, self.H, self.K)

   def makeRepairSymbols(self):
       IntermediateSymbols = self.makeIntermediateSymbol()
       for i in range(0, self.numOfRepairSymbols):
          ix = self.params_get_idxs(self.K + i)
          matA = np.zeros((1, self.L), dtype=np.int)
          for ii in range(0, len(ix)):
              matA[0][ix[ii]] = 1
          self.RepairSymbols[i] = self.octetmath.multiplyMatrix(
              matA, IntermediateSymbols)
       return self.RepairSymbols

   def Encode(self):
       self.makeRepairSymbols()
       SourceSymbols = self.SourceSymbols1[self.S +self.H: self.L - (self.K - self.numSouceSymbols), ]
       temp = np.zeros((1, self.PAY_LEN), dtype=np.int)
       temp[0] = SourceSymbols[0]
       self.SourceSymbols = temp




   def Decode(self):

      sb,s1=self.SourceSymbols.shape
      b2=np.zeros((sb,s1),dtype=np.int)
      for row1 in range(0,sb):
            for col1 in range(0,s1):
                b2[row1][col1]=self.SourceSymbols[row1][col1]  

      # 解码过程需要这么几个参数，这里不做模拟，写死了
      self.matrix = np.zeros(
          (self.B+self.S+self.U+self.H, self.H+self.S+self.K), dtype=np.int)
      self.make_LDPC1()
      self.make_identity()
      self.make_LDPC2()
      self.make_HDPC()
      self.make_ENC()
      numSouceSymbols = 1
      missIdx = [1]
      RepairSymbolsReal = np.zeros((2, self.PAY_LEN), dtype=np.int)
      RepairSymbolsReal[0] = self.RepairSymbols[0]
      RepairSymbolsReal[1] = self.RepairSymbols[2]
      repairIdx = [0, 2]
      padding = self.PAY_LEN-self.datalen
      SourceSymbols =np.zeros((1,self.PAY_LEN),dtype=np.int)
      temp=[]
      
      for i in range(0,self.PAY_LEN):
          temp.append(0)
    
      for ii in range(0,self.K - numSouceSymbols):
          SourceSymbols= np.row_stack((SourceSymbols, temp))
      for i1 in range(0,self.S+self.H):
         SourceSymbols= np.row_stack((SourceSymbols, temp))
      mA=self.matrix.copy()


      counter=0

      for i2 in range(0,len(missIdx)):
        idx = self.S + self.H + missIdx[i2]-1
        yy=[]
        for it in range(0,self.L):
            yy.append(0)
        mA[idx] =np.array(yy)
        ix =self.params_get_idxs(self.K +  repairIdx[i2])
        for i4 in range(0,len(ix)):

            mA[idx][ix[i4]] = 1
        counter = i2
        SourceSymbols[idx] =self.RepairSymbols[i2]

      b1=self.matrix

  
      self.matrix=mA
      self.SourceSymbols=SourceSymbols
      result=self.makeIntermediateSymbol()
      ff,gg=result.shape
      SourceSymbols = []
      for i in range(0,self.K-1):

        # 单纯的result矩阵的拷贝，作者使用了copy好像没有生效，先这样吧
        temp=np.zeros((ff,gg),dtype=np.int)
        for row in range(0,ff):
            for col in range(0,gg):
                temp[row][col]=result[row][col]       
        g = self.TupleGenerator(i)
        SourceSymbols.append(Encode1(temp,  g['d'], g['a'], g['b'], g['d1'], g['a1'], g['b1'], self.W, self.P, self.P1, self.octetmath,i))  
      SourceSymbols=np.array(SourceSymbols)
      wid, length = b2.shape
      for row in range(0, wid):
        for col in range(0,length):
          if b2[row][col] != SourceSymbols[row][col]:
             print("failed")
             break
  
      w, l= SourceSymbols.shape
      raptorq=[]
      counter = 0
      for n in range(0,w):
         for nn in range(0,l):
             counter=counter+1
             raptorq.append(SourceSymbols[n][nn])
             if(counter == self.datalen):
               return raptorq




















   def TupleGenerator(self, X):
        ret = {}
        A = 53591 + self.J * 997
        if (A % 2 == 0):
            A += 1
        B1 = 10267 * (self.J + 1)
        y = int((B1 + X * A))
        v = rnd_get(y, 0, int((1 << 20)))
        ret['d'] = deg(v, self.W)
        ret['a'] = 1 + int(rnd_get(y, 1, self.W - 1))
        ret['b'] = int(rnd_get(y, 2, self.W))
        if ret['d'] < 4:
           ret['d1'] = 2 + int(rnd_get(X, 3, 2))
        else:
           ret['d1'] = 2
        ret['a1'] = 1 + int(rnd_get(X, 4, self.P1 - 1))
        ret['b1'] = int(rnd_get(X, 5, self.P1))
        return ret

   def params_get_idxs(self, X):
      ret = []
      t = self.TupleGenerator(X)

      ret.append(t['b'])
      for j in range(0, t['d']):
          t['b'] = (t['b']+t['a']) % self.W
          ret.append(t['b'])

      ret.sort()

      while t['b1'] >= self.P:
        t['b1'] = (t['b1'] + t['a1']) % self.P1

      ret.append(self.W + t['b1'])
      for j in range(0, t['d1']-1):
          while True:
            t['b1'] = (t['b1']+t['a1']) % self.P1
            if t['b1'] < self.P:
                break
          ret.append(self.W+t['b1'])
      return ret

   def make_LDPC1(self):
       circulant_matrix = 0
       for col in range(0, self.B):
            submtx = int(col / self.S)
            b1 = col % self.S
            b2 = (col + submtx + 1) % self.S
            b3 = (col + 2 * (submtx + 1)) % self.S
            self.matrix[b1][col] = 1
            self.matrix[b2][col] = 1
            self.matrix[b3][col] = 1

   def make_identity(self):
        for col in range(0, self.S):
            self.matrix[col][self.B+col] = 1

   def make_LDPC2(self):
       for col in range(0, self.S):
            b1 = col % self.P
            b2 = (col + 1) % self.P
            self.matrix[col][self.W+b1] = 1
            self.matrix[col][self.W+b2] = 1

   def make_MT(self):
       rows, cols = self.H, self.K+self.S
       MT = np.zeros((rows, cols), dtype=np.int)
       for col in range(0, cols-1):
           b1 = rnd_get(col+1, 6, rows)
           b2 = (b1+rnd_get(col+1, 7, rows-1)+1) % rows
           MT[b1][col] = 1
           MT[b2][col] = 1
       for row in range(0, rows):
           MT[row][cols-1] = OCT_EXP[row]
       return MT

   def make_GAMMA(self):
       rows, cols = self.K+self.S, self.K+self.S
       GAMMA = np.zeros((rows, cols), dtype=np.int)
       for row in range(0, rows):
           for col in range(0, row+1):
              GAMMA[row][col] = OCT_EXP[(row-col) % 255]
           for index2 in range(col, cols):
               pass
            #  GAMMA[row][index2]=0
       return GAMMA

   def make_HDPC(self):
       MT = self.make_MT()
       GAMMA = self.make_GAMMA()
       HDPC = self.octetmath.GaloisMultiply(MT, GAMMA)

       for row in range(self.S, self.S+self.H):
           for col in range(0, self.K+self.S):
            self.matrix[row][col] = HDPC[row-self.S][col]
       for index in range(self.S, self.S+self.H):
           self.matrix[index][self.K+index] = 1

   def make_ENC(self):
       temp=np.zeros((self.L,self.H+self.S+self.K),dtype=np.int)
       for row in range(self.S+self.H, self.L):
           isi = (row-self.S)-self.H
           idxs = self.params_get_idxs(isi)
           for col in range(0, len(idxs)):
               self.matrix[row][idxs[col]] = 1
               temp[row-self.H-self.S][idxs[col]]=1
       return temp


def rnd_get(y, i, m):
  x0 = (y + i) & 0xff
  x1 = ((y >> 8) + i) & 0xff
  x2 = ((y >> 16) + i) & 0xff
  x3 = ((y >> 24) + i) & 0xff
  return (V0[x0] ^ V1[x1] ^ V2[x2] ^ V3[x3]) % m


def deg(v, w):
    j = 0
    while v > f[j]:
        j += 1
    if j < (w-2):
        return j
    else:
        return (w-2)
