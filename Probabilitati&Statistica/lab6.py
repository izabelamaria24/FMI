# bernoulli

import matplotlib.pyplot as plt
import numpy as np

p = 0.6
cnt = 1000
x = []

for i in range(cnt):
    x.append(int(np.random.random() < p))
    
bins = [-1/2, 1/2, 3/2]
counts = np.histogram(x, bins=bins)

plt.hist(x, bins=bins, ec='black', density=True)
plt.xticks([0, 1], ['Failure (0)', 'Success (1)'])
plt.xlabel('Outcome')
plt.ylabel('Probability Density')
plt.title('Histogram of Bernoulli')
plt.show()

#Binomial 
#nevectorizat
def bin_nevec(n, p, num_experiments):
    outcomes = []
    for _ in range(num_experiments):
        successes = sum(np.random.random(n) < p) 
        outcomes.append(successes)

    outcomes = np.array(outcomes)

    bins = np.arange(-0.5, n + 1.5, 1)  

    plt.hist(outcomes, bins=bins, edgecolor='black', density=True)
    plt.xticks(range(n + 1))  
    plt.xlabel('Number of Successes')
    plt.ylabel('Probability Density')
    plt.title(f'Binomial Distribution (n={n}, p={p})')
    plt.show()

# vectorizat

def binomial(n, p, num_experiments):
    outcomes = np.random.random((num_experiments, n)) < p
    success_counts = outcomes.sum(axis=1)

    bins = np.arange(-0.5, n + 1.5, 1) 

    plt.hist(success_counts, bins=bins, edgecolor='black', density=True)
    plt.xticks(range(n + 1)) 
    plt.xlabel('Number of Successes')
    plt.ylabel('Probability Density')
    plt.title(f'Binomial Distribution (n={n}, p={p})')
    plt.show()


def geometrica(n, p, cnt_sim):
    x = []
    for i in range(cnt_sim):
        cnt = 0
        while np.random.random() < p:
            cnt += 1
        x.append(cnt)
    
    bins = np.arange(-0.5, n + 1.5, 1)
    
    plt.hist(x, bins=bins, edgecolor='black', density=True)
    plt.xticks(range(n + 1))
    plt.xlabel('Number of Trials')
    plt.ylabel('Probability Density')
    plt.title(f'Geometric Distribution (n={n}, p={p})')
    plt.show()
    

#geometrica(20, 0.6, 1000)

