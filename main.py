from lib import Simulation
import numpy as np
import matplotlib.pyplot as plt


def main():
    factorfi = 1
    factorfc = 1
    fc_passing = True
    fi_passing = True
    while fc_passing:
        try:
            sim = Simulation.Simulation(4, 3, factorfc, 1,
                                        [(1, 2, 2), (2, 3, 0), (3, 3, 1), (4, 0, 1), (5, 3, 1), (6, 0, 2), (7, 1, 2),
                                         (8, 3, 0), (9, 3, 1), (10, 3, 2), (11, 3, 2), (12, 2, 2), (13, 1, 2),
                                         (14, 2, 2), (15, 2, 0), (16, 2, 2), (17, 0, 1), (18, 3, 2), (19, 0, 0),
                                         (20, 0, 2), (21, 3, 2), (22, 1, 0), (23, 3, 2), (24, 2, 1), (25, 1, 0),
                                         (26, 2, 2), (27, 0, 0), (28, 2, 0), (29, 2, 2), (30, 1, 2), (31, 0, 2),
                                         (32, 3, 0), (33, 0, 2), (34, 3, 0), (35, 0, 1), (36, 1, 0), (37, 1, 2),
                                         (38, 2, 1), (39, 0, 0), (40, 1, 2), (41, 1, 1), (42, 1, 0), (43, 1, 1),
                                         (44, 1, 2)])
            factorfc -= 0.01
        except Exception:
            factorfc += 0.01
            fc_passing = False

    while fi_passing:
        try:
            sim = Simulation.Simulation(4, 3, 1, factorfi,
                                        [(1, 2, 2), (2, 3, 0), (3, 3, 1), (4, 0, 1), (5, 3, 1), (6, 0, 2), (7, 1, 2),
                                         (8, 3, 0), (9, 3, 1), (10, 3, 2), (11, 3, 2), (12, 2, 2), (13, 1, 2),
                                         (14, 2, 2), (15, 2, 0), (16, 2, 2), (17, 0, 1), (18, 3, 2), (19, 0, 0),
                                         (20, 0, 2), (21, 3, 2), (22, 1, 0), (23, 3, 2), (24, 2, 1), (25, 1, 0),
                                         (26, 2, 2), (27, 0, 0), (28, 2, 0), (29, 2, 2), (30, 1, 2), (31, 0, 2),
                                         (32, 3, 0), (33, 0, 2), (34, 3, 0), (35, 0, 1), (36, 1, 0), (37, 1, 2),
                                         (38, 2, 1), (39, 0, 0), (40, 1, 2), (41, 1, 1), (42, 1, 0), (43, 1, 1),
                                         (44, 1, 2)])
            factorfi -= 0.01
        except Exception:
            factorfi += 0.01
            fi_passing = False

    print(factorfc, factorfi)


def gen_main():
    graphx = []
    graphy = []
    bestmapping = []
    bestmapping_fit = 0

    try:
        # Consts
        pop_size = 500
        mutation_rate = 0.01
        meshX = 20
        meshY = 20
        runs = 100

        # Generate population
        def create_random_mapping():

            # # Uncomment for non-selective start
            # mapping = []
            # taskIDs = [i.id for i in Simulation.btasks]

            # for id in taskIDs:

            #     randX = np.random.randint(0, meshX)
            #     randY = np.random.randint(0, meshY)
            #     mapping.append((id, randX, randY))

            # Uncomment to have selective start
            yn = True

            while yn:

                taskIDs = [i.id for i in Simulation.btasks]

                mapping = []

                for id in taskIDs:
                    randX = np.random.randint(0, meshX)
                    randY = np.random.randint(0, meshY)
                    mapping.append((id, randX, randY))

                try:
                    sim = Simulation.Simulation(meshX, meshY, 1, 1, mapping)
                    yn = False
                except Exception:
                    print(mapping)
                    yn = True

            print("Found sol")
            return mapping

        population_mappings = [create_random_mapping() for i in range(pop_size)]

        for k in range(runs):
            print('\nIteration {}'.format(k))
            # Sim population collect costs and inf if fail
            costs = []

            for mapping in population_mappings:
                try:
                    sim = Simulation.Simulation(meshX, meshY, 1, 1, mapping)
                    costs.append(sim.get_fitness())
                except Exception:
                    costs.append(1000)

                # costs.append(np.random.randint(0, 1000))

            # Invert costs need to find range
            inv_costs = np.asarray(costs)
            inv_costs = np.abs(inv_costs - 1000)
            print('Fitness = Max: {}  Min: {}  Ave: {}  Fails: {}'.format(inv_costs.max(), inv_costs.min(),
                                                                            inv_costs.mean(),
                                                                            np.count_nonzero(inv_costs == 0)))
            print('Best mapping is:\n{}'.format(population_mappings[np.argmax(inv_costs)]))

            # Drawing pretty lines and collecting results
            graphx.append(k)
            graphy.append((inv_costs.max(), inv_costs.min(), inv_costs.mean()))

            if inv_costs.max() > bestmapping_fit:
                bestmapping_fit = inv_costs.max()
                bestmapping = population_mappings[np.argmax(inv_costs)]
            # ~~~~

            # Breed population
            if sum(inv_costs) != 0:
                distribution = inv_costs / sum(inv_costs)
            else:
                distribution = np.asarray([1 / pop_size] * pop_size)

            choices1 = np.random.choice(np.arange(pop_size), pop_size, p=distribution)
            choices2 = np.random.choice(np.arange(pop_size), pop_size, p=distribution)

            newpop = []

            for i in range(pop_size):
                mapping1 = population_mappings[choices1[i]]
                mapping2 = population_mappings[choices2[i]]

                newmapping = []

                for (tsk1, x1, y1,), (tsk2, x2, y2) in zip(mapping1, mapping2):

                    if np.random.random() > mutation_rate:

                        # No mutation
                        if np.random.randint(1, 11, 1) > 5:
                            newmapping.append((tsk1, x1, y1))
                        else:
                            newmapping.append((tsk2, x2, y2))

                    else:

                        # Mutation
                        newmapping.append((tsk1, np.random.randint(0, meshX), np.random.randint(0, meshY)))

                newpop.append(newmapping)

            population_mappings = newpop

    except:
        pass
    print('\n\n\n\n----------------------')
    print(bestmapping_fit)
    print(bestmapping)
    plt.plot(graphx, graphy)
    plt.show()


if __name__ == '__main__':
    gen_main()
