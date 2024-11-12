import numpy as np
import matplotlib.pyplot as plt
import time

def arunca(prob, nr_aruncari):
    tic = time.perf_counter()
    
    res = np.random.random(nr_aruncari)
    x = []
    y = []
    
    counter = 0
    
    for i in range(nr_aruncari):
        if res[i] < prob:
            counter += 1
        x.append(i)
        y.append(counter/(i + 1))
    
    toc = time.perf_counter()
    print(f"Time 1:' {toc-tic}")
    print(counter)
    plt.plot(x, y, marker='o')
    plt.xlabel('Aruncari')
    plt.ylabel('Probabilitate cap')
    plt.show()
    
    
def arunca_vectorizat(prob, nr_aruncari):
    tic = time.perf_counter()
    
    res = np.random.random(nr_aruncari)
    x = np.arange(nr_aruncari)
    y = np.cumsum(res < prob) / (x + 1)
    
    toc = time.perf_counter()
    print(f"Time 2:' {toc-tic}")
    #print(y[-1])
    plt.plot(x, y, marker='o')
    plt.xlabel('Aruncari')
    plt.ylabel('Probabilitate cap')
    plt.show()    


# arunca(0.5, 10000)    
#arunca(0.7, 10000)
arunca(0.5, 10000)
arunca_vectorizat(0.5, 10000)