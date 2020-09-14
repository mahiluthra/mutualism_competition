import ga
import agent_species_mutcomp as mutcomp
import numpy as np
#import matplotlib.pyplot as plt

# Params
N = 5
reps = 5
duration = 2000.0
stepsize = 0.1
steps = int(duration/stepsize)

# Fitness function
def fitnessFunction(genotype):
    fit = 0.0
    a = mutcomp.CLV(N)
    a.setParams(genotype)
    for i in range(reps):
        a.resetState()
        for i in range(steps):
            a.step_mutualism(stepsize)
        fit += a.diversity()/N
    return fit/reps
# EA Params
popsize = 5
genesize = 2 * (N*N - N + N) + N*N
recombProb = 0.5
mutatProb = 0.02
generations = 2
tournaments = generations * popsize

# Evolve and visualize fitness over generations
ga = ga.GA(fitnessFunction, popsize, genesize, recombProb, mutatProb)
ga.run(tournaments)
#ga.showFitness()

#compga = ga
bestHist = ga.bestHistory
avgHist = ga.avgHistory

# Show behavior of the best evolved solution
af,bf,genotype = ga.fitStats()


print(avgHist)
print(bestHist)
print(af,bf, genotype)

import csv

with open('agent_mutualismtyperx-fullyconnected_N5.csv', mode='w') as agent_file:
    agent_writer = csv.writer(agent_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    agent_writer.writerow(bestHist)
    agent_writer.writerow(avgHist)
    agent_writer.writerow([af])
    agent_writer.writerow([bf])
    agent_writer.writerow(genotype)
    