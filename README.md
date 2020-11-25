EMBS-Design-Contest

# Important things from the handout
- XY Routing
- Tasks inside same router don't need to use NOC to connect
- There is no comptime (From what I can see)
- Simulation needs to be able to handle NxP mesh network
- No limits on buffer size and memory
- Communication flows are the things between task (Like sdf graph)
- Tiles clocked at Fc, can run lower using factorFC to run slower [0.001, 0.999]
- Task util with linearly change with factorFC which is divide by factorFC
- Task can't be exec if util becomes over 1.0 (That means lowest frequecy can be found at start)
- Router frequency Fi, and changed with factorFI
- Interconnect frequency util scaled with factorFI again
- Can't excede 1.0

## Achievements
- Sum of utils per tile be under 1.0
- Sum of utils per router be under 1.0
- Cost = (X*Y)+facFC+facFI if no cores are overutilised, infinte otherwise

# Doc
Mapping is done as follows (taskId, X, Y), .... for all tasks where X and Y are the coords on a mesh

# Proposed solotion
For n in range(1, inf)
    For p in range(1, inf)

        gen alg using frequencies factors and mapping
        (Can skip some failed processes by calulating lowest freq that we can possibly go to)

plot to see the global optimum to see best score depending on mesh size


# DEV
Search # TODO: