# 좌표 평면 두점 사이의 거리를 구하는 알고리즘 
import math 

def getDistance(p1, p2):
    xDistance = p1[0] - p2[0]
    print(xDistance)
    yDistance = p1[1] - p2[1]
    print(yDistance)

    #피타고라스정리에 의해 
    pDistance = math.pow(xDistance,2) + math.pow(yDistance,2)

    return math.sqrt(pDistance)

p1 = (0, 2)
p2 = (3, 4)
print(getDistance(p1, p2))