

def mode(lists):
 count={}
 for i in lists:
     if i in count:
         count[i]+=1
     else:
         count[i]=1
 more=0
 num=0
 for i in lists:
     if count[i]>more:
        more=count[i]
        num=i
 return num