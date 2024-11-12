import numpy as np
import matplotlib.pyplot as plt

num_chords = 10000


def draw_circle_and_triangle(ax):
    circle = plt.Circle((0, 0), 1, color='w', linewidth=2, fill=False)
    ax.add_patch(circle) 

    ax.plot([np.cos(np.pi / 2), np.cos(7 * np.pi / 6)], 
            [np.sin(np.pi / 2), np.sin(7 * np.pi / 6)], linewidth=2, color='g')
    ax.plot([np.cos(np.pi / 2), np.cos(- np.pi / 6)],  
            [np.sin(np.pi / 2), np.sin(- np.pi / 6)], linewidth=2, color='g')
    ax.plot([np.cos(- np.pi / 6), np.cos(7 * np.pi / 6)],  
            [np.sin(- np.pi / 6), np.sin(7 * np.pi / 6)], linewidth=2, color='g')


def bertrand_simulation(method_number):
    count_long_chords = 0

    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    ax.set_aspect('equal', 'box')
    ax.set_xlim((-1, 1)) 
    ax.set_ylim((-1, 1))  

    draw_circle_and_triangle(ax)

    for i in range(num_chords):
        x, y = bertrand_methods[method_number]()
        x1, y1 = x[0], y[0]
        x2, y2 = x[1], y[1]

        chord_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        if chord_length > np.sqrt(3):
            count_long_chords += 1
            color = 'r'  
        else:
            color = 'b'  

        if i < 1000:
            ax.plot([x1, x2], [y1, y2], color=color, alpha=0.1)

    probability_long_chords = count_long_chords / num_chords
    print(f'Probability of chords longer than triangle side: {probability_long_chords:.4f}')

    plt.show()


def bertrand1():
    """Method 1: Random points on the circle"""
    theta1 = np.random.rand() * 2 * np.pi
    theta2 = np.random.rand() * 2 * np.pi

    x = [np.cos(theta1), np.cos(theta2)]
    y = [np.sin(theta1), np.sin(theta2)]

    return x, y

def bertrand2():
    """Method 2: Random points inside the circle, then calculate the chord."""
    
    u1 = np.random.rand()
    u2 = np.random.rand()

    x = np.sqrt(u1) * np.cos(2 * np.pi * u2)
    y = np.sqrt(u1) * np.sin(2 * np.pi * u2)

    d = np.sqrt(x**2 + y**2)
    
    half_chord_length = np.sqrt(1 - d**2)  

    theta = np.arctan2(y, x) + np.pi / 2 

    x1 = x + half_chord_length * np.cos(theta)
    y1 = y + half_chord_length * np.sin(theta)

    x2 = x - half_chord_length * np.cos(theta)
    y2 = y - half_chord_length * np.sin(theta)
    
    return (x1, x2), (y1, y2)


bertrand_methods = {1: bertrand1, 2: bertrand2}

bertrand_simulation(2)
