"""
Carwash example.

Covers:

- Waiting for other processes
- Resources: Resource

Scenario:
  A carwash has a limited number of washing machines and defines
  a washing processes that takes some (random) time.

  Car processes arrive at the carwash at a random time. If one washing
  machine is available, they start the washing process and wait for it
  to finish. If not, they wait until they can use one.

"""
import random

import simpy


RANDOM_SEED = 42
NUM_GATES = 2  # Number of machines in the carwash
WAIT_TIME = 5      # Minutes it takes to clean a car
T_INTER = 7       # Create a car every ~7 minutes
SIM_TIME = 20     # Simulation time in minutes


class Airport(object):
    """A carwash has a limited number of machines (``NUM_MACHINES``) to
    clean cars in parallel.

    Cars have to request one of the machines. When they got one, they
    can start the washing processes and wait for it to finish (which
    takes ``washtime`` minutes).

    """
    def __init__(self, env, num_gates, wait_time):
        self.env = env
        self.num_gates = simpy.Resource(env, num_gates)
        self.wait_time = wait_time

    def land(self, plane):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
        yield self.env.timeout(WAIT_TIME)
        print("Airport authorizes %s to land" % plane)


def plane(env, name, ap):
    """The car process (each car has a ``name``) arrives at the carwash
    (``cw``) and requests a cleaning machine.

    It then starts the washing process, waits for it to finish and
    leaves to never come back ...

    """
    print('%s arrives at the airport at %.2f.' % (name, env.now))
    with ap.num_gates.request() as request:
        yield request

        print('%s enters the airport at %.2f.' % (name, env.now))
        yield env.process(ap.land(name))

        print('%s leaves the airport at %.2f.' % (name, env.now))


def setup(env, num_gates, wait_time, t_inter):
    """Create a carwash, a number of initial cars and keep creating cars
    approx. every ``t_inter`` minutes."""
    # Create the airport
    airport = Airport(env, num_gates, wait_time)

    # Create 4 initial planes
    for i in range(4):
        env.process(plane(env, 'Plane %d' % i, airport))

    # Create more cars while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter-2, t_inter+2))
        i += 1
        env.process(plane(env, 'Plane %d' % i, airport))


# Setup and start the simulation
print('Airport')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_GATES, WAIT_TIME, T_INTER))

# Execute!
env.run(until=SIM_TIME)
