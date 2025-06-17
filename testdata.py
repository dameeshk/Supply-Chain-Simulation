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

def analyze_simulations(forecast, trials=10, num_runs=1000):
    """
    Perform statistical analysis comparing Poisson vs Binomial simulations
    """
    print(f"\nStatistical Analysis ({num_runs} runs):")
    print("=" * 60)
    
    # Store all results for analysis
    poisson_errors = []
    binomial_errors = []
    poisson_totals = []
    binomial_totals = []
    
    # Run many simulations
    for _ in range(num_runs):
        poisson_result = simulate_poisson_demand(forecast)
        binomial_result = simulate_binomial_demand(forecast, trials)
        
        # Calculate errors (difference from forecast)
        poisson_error = sum(abs(p - f) for p, f in zip(poisson_result, forecast))
        binomial_error = sum(abs(b - f) for b, f in zip(binomial_result, forecast))
        
        poisson_errors.append(poisson_error)
        binomial_errors.append(binomial_error)
        poisson_totals.append(sum(poisson_result))
        binomial_totals.append(sum(binomial_result))
    
    # Calculate statistics
    forecast_total = sum(forecast)
    
    print(f"Original forecast total: {forecast_total}")
    print()
    
    # Poisson Statistics
    print("POISSON RESULTS:")
    print(f"  Average total demand: {np.mean(poisson_totals):.2f}")
    print(f"  Standard deviation: {np.std(poisson_totals):.2f}")
    print(f"  Average absolute error: {np.mean(poisson_errors):.2f}")
    print(f"  Error standard deviation: {np.std(poisson_errors):.2f}")
    
    print()
    
    # Binomial Statistics  
    print("BINOMIAL RESULTS:")
    print(f"  Average total demand: {np.mean(binomial_totals):.2f}")
    print(f"  Standard deviation: {np.std(binomial_totals):.2f}")
    print(f"  Average absolute error: {np.mean(binomial_errors):.2f}")
    print(f"  Error standard deviation: {np.std(binomial_errors):.2f}")
    
    print()
    
    # Comparison
    print("COMPARISON:")
    poisson_better = sum(1 for p, b in zip(poisson_errors, binomial_errors) if p < b)
    binomial_better = sum(1 for p, b in zip(poisson_errors, binomial_errors) if b < p)
    
    print(f"  Poisson more accurate: {poisson_better}/{num_runs} times ({poisson_better/num_runs*100:.1f}%)")
    print(f"  Binomial more accurate: {binomial_better}/{num_runs} times ({binomial_better/num_runs*100:.1f}%)")
    
    if np.mean(poisson_errors) < np.mean(binomial_errors):
        print(f"  Winner: Poisson (lower average error)")
    else:
        print(f"  Winner: Binomial (lower average error)")


analyze_simulations(forecast, trials=10, num_runs=1000)