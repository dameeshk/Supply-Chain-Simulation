#By Dameesh Kumar
import random
import math
import numpy as np

# Test data - a 14-day forecast
forecast = [5, 3, 7, 2, 6, 4, 8, 1, 9, 3, 5, 2, 7, 4]

print("Original forecast:", forecast)
print("Number of days:", len(forecast))

# Poisson simulation with NumPy Library
def simulate_poisson_demand(forecast):
    return np.random.poisson(forecast).tolist()


poisson_result = simulate_poisson_demand(forecast)
print("\nPoisson simulation results:")
print("Forecast: ", forecast)
print("Poisson:  ", poisson_result)

# Binomial simulation with NumPy Library
def simulate_binomial_demand(forecast, trials=10):
    probabilities = np.minimum(np.array(forecast) / trials, 1.0)
    return np.random.binomial(trials, probabilities).tolist()


binomial_result = simulate_binomial_demand(forecast, trials=10)
print("\nBinomial simulation results:")
print("Forecast: ", forecast)
print("Binomial: ", binomial_result)

def compare_simulations(forecast, trials=10, num_runs=5):
    print(f"\nComparing Poisson vs Binomial simulations ({num_runs} runs):")
    print("Forecast:", forecast)
    print("-" * 80)
    
    for run in range(num_runs):
        poisson_result = simulate_poisson_demand(forecast)
        binomial_result = simulate_binomial_demand(forecast, trials)
        
        print(f"Run {run + 1}:")
        print(f"  Poisson:  {poisson_result}")
        print(f"  Binomial: {binomial_result}")
        print()


compare_simulations(forecast, trials=10, num_runs=5)