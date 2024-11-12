# import matplotlib.pyplot as plt
# import numpy as np

# def simulare_aruncari_bitwise(nr_aruncari, lungime_secv_cap):
#     bit_sequence = 0
#     pattern = (1 << lungime_secv_cap) - 1
    
#     for i in range(nr_aruncari):
#         flip = 1 if np.random.random() < 0.5 else 0
#         bit_sequence = ((bit_sequence << 1) | flip) & pattern
#         if bit_sequence == pattern:
#             return True
#     return False  


# nr_simulari = 1000 
# max_nr_aruncari = 20
# lungime_secventa_cap = 4
# probabilities = []

# for nr_aruncari in range(1, max_nr_aruncari + 1):
#     count_success = 0
#     for _ in range(nr_simulari):
#         if simulare_aruncari_bitwise(nr_aruncari, lungime_secventa_cap):
#             count_success += 1
#     probability = count_success / nr_simulari
#     probabilities.append(probability)
    
#     if nr_aruncari == 20:
#         print(f"{probability} ")


# plt.figure(figsize=(10, 6))
# plt.plot(range(1, max_nr_aruncari + 1), probabilities, marker='o', linestyle='-')
# plt.xlabel("Number of coin flips")
# plt.ylabel(f"Probability of {lungime_secventa_cap} heads in a row")
# plt.title(f"Probability of {lungime_secventa_cap} in a row in a sequence")
# plt.grid()
# plt.show()
