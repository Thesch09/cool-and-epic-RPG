import math
'''
x = 0
for i in range(64):
    print(math.modf(i/32))
    x+=1

for i in range(64):
    tempVar = math.modf(x/32)
    print(tempVar[1])
    x+=1
'''
x = 0
for i in range(96):
    tempVar = math.fmod(i, 32)
    print(tempVar)

dictTest = {"value":0, "val2":"egg"}
for i in dictTest:
    print(i)
    print(dictTest[i])