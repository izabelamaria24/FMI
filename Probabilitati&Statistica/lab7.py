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


n = 5  
num_valori = 4  
min_val = 10  
max_val = 50  

variabile_generate = genereaza_variabile_discrete_random(n, num_valori, min_val, max_val)

for nume, date in variabile_generate.items():
    print(f"{nume}:")
    print(f"  Valori posibile: {date['valori']}")
    print(f"  Probabilități: {date['probabilitati']}")


nr_simulari = 10000
suma_initiala = 10000

W = np.array([])
X = np.array([])
for i in range(nr_simulari):
    # simulam 300 de variabile aleatoare
    variabile_generate = genereaza_variabile_discrete_random(300, 3, 0.001, 0.99)
    
    # pentru fiecare variabila aleatoare din variabile_generate, adaugam in X media ponderata
    X = np.concatenate((X, np.array([variabile_generate[f"X_{i+1}"]["probabilitati"].dot(variabile_generate[f"X_{i+1}"]["valori"]) for i in range(300)])))
    
    # pentru fiecare variabila aleatoare, adaugam in W suma_initiala * probability
    W = np.concatenate((W, np.array([suma_initiala * variabile_generate[f"X_{i+1}"]["probabilitati"][i] for i in range(300)])))
    

media_ponderata = np.mean(W)
mediana_ponderata = np.median(W)
dispersion_ponderata = np.var(W)