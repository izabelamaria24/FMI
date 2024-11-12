
def aruncari_teoretice(n):
    if n < 3: 
        return 0
    if n == 3:
        return (1 / 8)
    
    return (5 / 8) * aruncari_teoretice(n - 3) + (1 / 8) * aruncari_teoretice(n - 1) + (1 / 4) * aruncari_teoretice(n - 2)


print(aruncari_teoretice(20))