from lib.sim import Simulation

def main():
    sim = Simulation(2,2,1,1)
    sim.run_map([(36, 0, 1), (37, 0, 0)])



if __name__ == '__main__':
    main()