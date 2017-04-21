import copy
import multiprocessing
import random

from deap import creator, base, tools, algorithms

from train import Train

creator.create("FitnessMin", base.Fitness, weights=(-1.0, 1.0, -0.1, -0.1))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 1, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=81)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

t = Train(distance=3200)
print(t.control(t.ascii2list('')))


def eval_gem(individual):
    tc = copy.deepcopy(t)

    return tc.control(individual), tc.is_success(), tc.speed, abs(tc.distance - tc.position)


toolbox.register("evaluate", eval_gem)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=-2, up=2, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=30)

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=8)
    toolbox.register("map", pool.map)

    population = toolbox.population(n=2400)
    print("  Evaluated %i individuals" % len(population))

    gen = 0

    while True:
        gen += 1

        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = toolbox.select(offspring, k=len(population))

        if gen % 10 == 0:
            best_ind = tools.selBest(population, 1)[0]
            print('%d\t[%s]\t[%s]' % (gen, Train.list2ascii(best_ind), best_ind.fitness.values))

        if gen > 1000:
            break

    pool.close()

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(population, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
