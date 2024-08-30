#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


CONST_PEPTIDE_MIN_LENGTH = 3
CONST_PEPTIDE_MAX_LENGTH = 50
CONST_GENES = "ACDEFGHIKLMNPQRSTVWY"


class Solution:
    def __init__(self, peptide):
        self.peptide = peptide
        self.fitness = 0


class GeneticAlgorithm:

    def __init__(
        self,
        fitness_function,
        population_size,
        offspring_count,
        max_num_generations
    ):
        self.fitness_function = fitness_function
        self.population_size = population_size
        self.offspring_count = offspring_count
        self.max_num_generations = max_num_generations

    def search(self):
        self.results = []

        population = self.generate_random_population()
        self.evaluate_population(population)
        self.results.append(
            [[solution.peptide, solution.fitness] for solution in population]
        )
        generation = 1

        while True:
            if generation > self.max_num_generations:
                break

            print('Iteration/Generation: {}/{}'.format(generation, self.max_num_generations))

            self.evaluate_population(population)
            offspring = self.generate_offspring(population)

            population += offspring
            self.evaluate_population(population)

            population = self.next_generation(population)
            generation += 1

            self.results.append(
                [[solution.peptide, solution.fitness] for solution in population]
            )

        return self.results

    def generate_random_population(self):
        population = []

        for _ in range(self.population_size):
            peptide = ''
            for _ in range(np.random.randint(CONST_PEPTIDE_MIN_LENGTH, CONST_PEPTIDE_MAX_LENGTH + 1)):
                peptide += CONST_GENES[np.random.randint(len(CONST_GENES))]

            population.append(Solution(peptide))

        return population

    def evaluate_population(self, population):
        for solution in population:
            solution.fitness = self.fitness_function(solution.peptide)

    def generate_offspring(self, population):
        offspring = []

        for i in range(self.offspring_count):
            parent1 = self.selection(population)
            parent2 = self.selection(population)

            child = self.recombination(parent1, parent2)
            child = self.mutation(child)

            offspring.append(child)

        return offspring

    def selection(self, population):
        random_parent = population[np.random.randint(len(population))]

        for _ in range(2):
            i = np.random.randint(len(population))
            if population[i].fitness > random_parent.fitness:
                random_parent = population[i]

        return random_parent

    def recombination(self, parent1, parent2):
        p = np.random.rand()
        peptide = parent1.peptide[:int(len(parent1.peptide) * p)] + parent2.peptide[int(len(parent2.peptide) * p):]

        while len(peptide) < CONST_PEPTIDE_MIN_LENGTH:
            peptide += CONST_GENES[np.random.randint(len(CONST_GENES))]

        if len(peptide) > CONST_PEPTIDE_MAX_LENGTH:
            peptide = peptide[:CONST_PEPTIDE_MAX_LENGTH]

        return Solution(peptide)

    def mutation(self, child):
        r = np.random.rand()

        peptide = child.peptide[:]

        if r < 0.3:
            peptide = list(peptide)
            peptide[np.random.randint(len(peptide))] = CONST_GENES[np.random.randint(len(CONST_GENES))]
            peptide = ''.join(peptide)

        elif r < 0.6 and len(peptide) < CONST_PEPTIDE_MAX_LENGTH:
            peptide += CONST_GENES[np.random.randint(len(CONST_GENES))]

        elif r < 1 and len(peptide) > CONST_PEPTIDE_MIN_LENGTH:
            peptide = peptide[:-1]

        return Solution(peptide)

    def next_generation(self, population):
        sorted_population = sorted(population, key=lambda solution: solution.fitness)
        return sorted_population[-self.population_size:]
