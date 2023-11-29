# x0 = 0 => max(a0, a1,..., an)
# x0 > 0 => sort(a0, a1,..., an, reverse)
# x0 < 0 => sort negative in ordine cresc, pozitive in ordine descresc

A = input().split()
A = [float(x) for x in A]
x0 = float(input())

if x0 == 0:
    print(max(A))
elif x0 > 0:
    A.sort(reverse=True)
    print(A)
else:
    result = []
    neg = [x for x in A if x <= 0]
    pos = [x for x in A if x > 0]
    neg.sort()
    pos.sort(reverse=True)
    leftPos = 0
    leftNeg = 0
    rightPos = len(pos) - 1
    rightNeg = len(neg) - 1
    for i in range(len(A)-1, -1, -1):
        if i % 2 == 0:
            if leftPos <= rightPos:
                result.append(pos[leftPos])
                leftPos += 1
            else:
                result.append(neg[rightNeg])
                rightNeg -= 1
        else:
            if leftNeg <= rightNeg:
                result.append(neg[leftNeg])
                leftNeg += 1
            else:
                result.append(pos[rightPos])
                rightPos -= 1
    print(result)
