import matplotlib.pyplot as plt
import numpy as np

def plot(chain_len_per_round_file):
    chain_len_per_round = np.load(chain_len_per_round_file)
    plt.figure()

    plt.xlabel("Round")
    plt.ylabel("Chain length")
    plt.plot(chain_len_per_round, label="Chain length", color='tab:blue')
    plt.tick_params(axis='y', labelcolor='tab:blue')
    plt.show()

def pow(n,q):
    plt.figure()
    x = [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2]
    y = [0.0008, 0.0102, 0.08333333333333333, 0.6402266288951841, 1, 1, 1]
    plt.xlabel("Probability of solving puzzle in one hash query")
    plt.ylabel("Chain growth rate")
    a = np.linspace(0, 9, 1000)
    a = 10**(-a)
    plt.loglog(a, 1-(1-a)**(n*q), label="Theoretical results", color='tab:blue')
    plt.plot(x, y, 'o', label="Simulation result", color='tab:orange')
    plt.legend()
    plt.show()

def selfish():
    plt.figure()
    x = [0.1, 0.2, 0.3, 0.4, 0.5]
    y = [0.07802041040272138, 0.19262585677144883, 0.3332482450542438, 0.5168571025532516, 0.9805106217111674]
    plt.xlabel("Malicious rate")
    plt.ylabel("Revenue rate")
    a = np.linspace(0, 0.5, 1000)
    plt.plot(a, (a*(1-a)**2*(4*a+(1-2*a)/2)-a**3) / (1-a*(1+(2-a)*a)), label="Theoretical results", color='tab:blue')
    plt.plot(x, y, 'o', label="Simulation result", color='tab:orange')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # plot("./data/chain_gen_1e-07.npy")
    # selfish()
    pow(n=1000,q=100)