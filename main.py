from lib import Simulation
import numpy as np


def main():
    sim = Simulation.Simulation(2, 2, 1, 1, [(36, 0, 1), (37, 0, 0)])


def gen_main():
    # Consts
    pop_size = 1000
    mutation_rate = 0.01
    meshX = 3
    meshY = 3

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

    # Sim population collect costs and inf if fail

    # Invert costs need to find range

    # Breed population

    # Apply mutations

    # Repeat
    return None


if __name__ == '__main__':
    gen_main()
