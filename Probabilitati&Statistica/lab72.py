import numpy as np

def genereaza_variabile_discrete_random(n, num_valori, min_val, max_val):
    variabile = {}
    
    for i in range(n):
        valori = np.random.uniform(min_val, max_val, num_valori)
        probabilitati = np.random.rand(num_valori)
        probabilitati /= probabilitati.sum()
        
        variabile[f"X_{i+1}"] = {
            "valori": valori,
            "probabilitati": probabilitati
        }
    
    return variabile


def genereaza_variabile_discrete_fixe(n):
    variabile = {}
    
    for i in range(n):
        valori = [1/2, 21/20, 3/2]
        probabilitati = [1/6, 4/6, 1/6]
        
        variabile[f"X_{i+1}"] = {
            "valori": valori,
            "probabilitati": probabilitati
        }
    
    return variabile


n = 300
num_valori = 3
min_val = 0.1
max_val = 2 

nr_simulari = 10000
suma_initiala = 1

W_totale = [] 

for sim in range(nr_simulari):
    W = []
    X = []

    variabile_generate = genereaza_variabile_discrete_fixe(300)
    
    for i in range(300):
        prob = variabile_generate[f"X_{i+1}"]["probabilitati"]
        valori = variabile_generate[f"X_{i+1}"]["valori"]
        
        X_i = np.dot(prob, valori)
        X.append(X_i)
    
    W_i = np.prod(X)  
    W.append(W_i) 

    W_totale.append(np.sum(W)) 


W_totale = np.array(W_totale)

media_W = np.mean(W_totale)
mediana_W = np.median(W_totale)

print(f"Media W: {media_W}")
print(f"Mediana W: {mediana_W}")
