from lib import Simulation
import numpy as np


def main():
    sim = Simulation.Simulation(2, 2, 1, 1, [(36, 0, 1), (37, 0, 0)])


def gen_main():
    # Consts
    pop_size = 10
    mutation_rate = 0.01
    meshX = 3
    meshY = 3
    runs = 100

    # Generate population
    def create_random_mapping():
        taskIDs = [i.id for i in Simulation.tasks]

        mapping = []

        for id in taskIDs:
            randX = np.random.randint(0, meshX)
            randY = np.random.randint(0, meshY)
            mapping.append((id, randX, randY))

        return mapping

    population_mappings = [create_random_mapping() for i in range(pop_size)]

    for k in range(runs):
        # Sim population collect costs and inf if fail
        # costs = []

        # for mapping in population_mappings:
        #     try:
        #         sim = Simulation.Simulation(meshX, meshY, 1, 1, mapping)
        #         costs.append(sim.get_cost_mark())
        #     except Exception:
        #         costs.append(1000)


        # Invert costs need to find range
        # TODO: Can't do yet until sim can run and get a good guage on the range
        inv_costs = [1]*10

        inv_costs = np.asarray(inv_costs)


        # Breed population
        distribution = inv_costs/sum(inv_costs)

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

    # Repeat
    return None


if __name__ == '__main__':
    gen_main()
