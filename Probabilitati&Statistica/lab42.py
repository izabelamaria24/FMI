import matplotlib.pyplot as plt
import numpy as np

def simulate_doors(no_doors, no_revealed, no_simulations):
    stay_win = 0 
    change_win = 0
    
    stay_win_probs = []
    change_win_probs = []
    
    for sim in range(1, no_simulations + 1):
        car = np.random.choice([i for i in range(1, no_doors + 1)]) 
        first_guess = np.random.choice([i for i in range(1, no_doors + 1)])  
        
        stay_win += (car == first_guess)
        
        revealed = np.random.choice([i for i in range(1, no_doors + 1) if i != car and i != first_guess], no_revealed, replace=False)
        
        second_guess = np.random.choice([door for door in range(1, no_doors + 1) if door not in revealed and door != first_guess])

        change_win += (car == second_guess)
    
        stay_win_prob = stay_win / sim
        change_win_prob = change_win / sim
        
        stay_win_probs.append(stay_win_prob)
        change_win_probs.append(change_win_prob)
    
    return stay_win_probs, change_win_probs


no_doors = 100
no_revealed = 50
no_simulations = 10000

stay_win_probs, change_win_probs = simulate_doors(no_doors, no_revealed, no_simulations)

plt.plot(range(1, no_simulations + 1), stay_win_probs, label='Stay with first guess', color='blue')
plt.plot(range(1, no_simulations + 1), change_win_probs, label='Change guess', color='green')
plt.xlabel('Number of Simulations')
plt.ylabel('Winning Probability')
plt.title('Monty Hall Problem: Stay vs Change Strategy Over Time')
plt.legend()
plt.grid(True)
plt.show()
