import matplotlib.pyplot as plt
import numpy as np

no_simulations = 10000

def simulate_door(no_doors, no_revealed, no_simulations):
    stay_win = 0
    change_win = 0
    
    for _ in range(no_simulations):
        car = np.random.choice([i for i in range(1, no_doors + 1)])
        first_guess = np.random.choice([i for i in range(1, no_doors + 1)])
        stay_win += car == first_guess
        
        revealed = np.random.choice([i for i in range(1, no_doors + 1) if i != car and i != first_guess])
        second_guess = np.random.choice([door for door in range(1, no_doors + 1) if door != revealed and door != first_guess])
        
        change_win += car == second_guess
    
    return stay_win, change_win

    
no_doors = 3
no_revealed = 1

stay_win, change_win = simulate_door(no_doors, no_revealed, no_simulations)

stay_win_prob = stay_win / no_simulations
change_win_prob = change_win / no_simulations

labels = ['Stay with first guess', 'Change guess']
probabilities = [stay_win_prob, change_win_prob]

plt.bar(labels, probabilities, color=['blue', 'green'])
plt.ylabel('Winning Probability')
plt.title('Monty Hall Problem: Stay vs Change Strategy')
plt.ylim([0, 1])
plt.show()    
