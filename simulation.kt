// By Dameesh Kumar
import kotlin.math.*
import kotlin.random.Random

fun main() {
    // Test data - a 14-day forecast
    val forecast = listOf(5, 3, 7, 2, 6, 4, 8, 1, 9, 3, 5, 2, 7, 4)
    
    println("Original forecast: $forecast")
    println("Number of days: ${forecast.size}")
    
    // Poisson simulation
    val poissonResult = simulatePoissonDemand(forecast)
    println("\nPoisson simulation results:")
    println("Forecast: $forecast")
    println("Poisson:  $poissonResult")
    
    // Binomial simulation
    val binomialResult = simulateBinomialDemand(forecast, trials = 10)
    println("\nBinomial simulation results:")
    println("Forecast: $forecast")
    println("Binomial: $binomialResult")
    
    // Compare simulations
    compareSimulations(forecast, trials = 10, numRuns = 5)
    
    // Analyze simulations
    analyzeSimulations(forecast, trials = 10, numRuns = 1000)
}

// Poisson simulation function
fun simulatePoissonDemand(forecast: List<Int>): List<Int> {
    return forecast.map { lambda ->
        generatePoisson(lambda.toDouble())
    }
}

// Binomial simulation function
fun simulateBinomialDemand(forecast: List<Int>, trials: Int = 10): List<Int> {
    return forecast.map { f ->
        val probability = minOf(f.toDouble() / trials, 1.0)
        generateBinomial(trials, probability)
    }
}

// Compare simulations function
fun compareSimulations(forecast: List<Int>, trials: Int = 10, numRuns: Int = 5) {
    println("\nComparing Poisson vs Binomial simulations ($numRuns runs):")
    println("Forecast: $forecast")
    println("-".repeat(80))
    
    repeat(numRuns) { run ->
        val poissonResult = simulatePoissonDemand(forecast)
        val binomialResult = simulateBinomialDemand(forecast, trials)
        
        println("Run ${run + 1}:")
        println("  Poisson:  $poissonResult")
        println("  Binomial: $binomialResult")
        println()
    }
}

// Statistical analysis function
fun analyzeSimulations(forecast: List<Int>, trials: Int = 10, numRuns: Int = 1000) {
    println("\nStatistical Analysis ($numRuns runs):")
    println("=".repeat(60))
    
    // Store all results for analysis
    val poissonErrors = mutableListOf<Int>()
    val binomialErrors = mutableListOf<Int>()
    val poissonTotals = mutableListOf<Int>()
    val binomialTotals = mutableListOf<Int>()
    
    // Run many simulations
    repeat(numRuns) {
        val poissonResult = simulatePoissonDemand(forecast)
        val binomialResult = simulateBinomialDemand(forecast, trials)
        
        // Calculate errors (difference from forecast)
        val poissonError = poissonResult.zip(forecast) { p, f -> abs(p - f) }.sum()
        val binomialError = binomialResult.zip(forecast) { b, f -> abs(b - f) }.sum()
        
        poissonErrors.add(poissonError)
        binomialErrors.add(binomialError)
        poissonTotals.add(poissonResult.sum())
        binomialTotals.add(binomialResult.sum())
    }
    
    // Calculate statistics
    val forecastTotal = forecast.sum()
    
    println("Original forecast total: $forecastTotal")
    println()
    
    // Poisson Statistics
    println("POISSON RESULTS:")
    println("  Average total demand: ${"%.2f".format(poissonTotals.average())}")
    println("  Standard deviation: ${"%.2f".format(poissonTotals.standardDeviation())}")
    println("  Average absolute error: ${"%.2f".format(poissonErrors.average())}")
    println("  Error standard deviation: ${"%.2f".format(poissonErrors.standardDeviation())}")
    
    println()
    
    // Binomial Statistics
    println("BINOMIAL RESULTS:")
    println("  Average total demand: ${"%.2f".format(binomialTotals.average())}")
    println("  Standard deviation: ${"%.2f".format(binomialTotals.standardDeviation())}")
    println("  Average absolute error: ${"%.2f".format(binomialErrors.average())}")
    println("  Error standard deviation: ${"%.2f".format(binomialErrors.standardDeviation())}")
    
    println()
    
    // Comparison
    println("COMPARISON:")
    val poissonBetter = poissonErrors.zip(binomialErrors) { p, b -> p < b }.count { it }
    val binomialBetter = poissonErrors.zip(binomialErrors) { p, b -> b < p }.count { it }
    
    println("  Poisson more accurate: $poissonBetter/$numRuns times (${"%.1f".format(poissonBetter.toDouble() / numRuns * 100)}%)")
    println("  Binomial more accurate: $binomialBetter/$numRuns times (${"%.1f".format(binomialBetter.toDouble() / numRuns * 100)}%)")
    
    if (poissonErrors.average() < binomialErrors.average()) {
        println("  Winner: Poisson (lower average error)")
    } else {
        println("  Winner: Binomial (lower average error)")
    }
}

// Utility function to generate Poisson random numbers
fun generatePoisson(lambda: Double): Int {
    val L = exp(-lambda)
    var k = 0
    var p = 1.0
    
    do {
        k++
        p *= Random.nextDouble()
    } while (p > L)
    
    return k - 1
}

// Utility function to generate Binomial random numbers
fun generateBinomial(n: Int, p: Double): Int {
    var count = 0
    repeat(n) {
        if (Random.nextDouble() < p) {
            count++
        }
    }
    return count
}

// Extension function to calculate standard deviation
fun List<Int>.standardDeviation(): Double {
    val mean = this.average()
    val variance = this.map { (it - mean).pow(2) }.average()
    return sqrt(variance)
}