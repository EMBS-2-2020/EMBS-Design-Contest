from lib import Simulation
import numpy as np
import matplotlib.pyplot as plt


def main():
    sim = Simulation.Simulation(2, 2, 1, 1, [(36, 0, 1), (37, 0, 0)])


def gen_main():
    graphx = []
    graphy = []
    bestmapping = []
    bestmapping_fit = 0

    try:
        # Consts
        pop_size = 500
        mutation_rate = 0.01
        meshX = 4
        meshY = 3
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
            print('Fitness = Max: {}  Min: {}  Ave: {}  Fails: {}'.format(inv_costs.max(), inv_costs.min(), inv_costs.mean(), np.count_nonzero(inv_costs==0)))
            print('Best mapping is:\n{}'.format(population_mappings[np.argmax(inv_costs)]))

            # Drawing pretty lines and collecting results
            graphx.append(k)
            graphy.append((inv_costs.max(), inv_costs.min(), inv_costs.mean()))

            if inv_costs.max() > bestmapping_fit:
                bestmapping_fit = inv_costs.max()
                bestmapping = population_mappings[np.argmax(inv_costs)]
            #~~~~

            # Breed population
            if sum(inv_costs) != 0:
                distribution = inv_costs/sum(inv_costs)
            else: 
                distribution = np.asarray([1/pop_size]*pop_size)

            choices1 = np.random.choice(np.arange(pop_size), pop_size, p=distribution)
            choices2 = np.random.choice(np.arange(pop_size), pop_size, p=distribution)

            newpop = []

            for i in range(pop_size):
                mapping1 = population_mappings[choices1[i]]
                mapping2 = population_mappings[choices2[i]]

                newmapping = []

                for (tsk1, x1, y1,),(tsk2, x2, y2) in zip(mapping1, mapping2):
                    
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
