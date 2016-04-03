import datetime
import random

import simpy
from Statistics import Statistics

RANDOM_SEED = datetime.datetime.time(datetime.datetime.now())
NUM_GATES = 10
WAIT_TIME = 0
T_INTER = 7
SIM_TIME = 1440

usage = False


class Airport(object):
    def __init__(self, env, num_gates, wait_time):
        self.env = env
        self.num_gates = simpy.Resource(env, num_gates)
        self.wait_time = wait_time
        self.open = False

    def leave(self, plane):
        yield self.env.timeout(random.randrange(20,30))
        print("Airport authorizes %s to leave at %d" % (plane, env.now))


def plane(env, name, ap):
    #print("tempo sem locacao: u%d   nu%d    t%d" % (usage_res, non_usage_res, env.now))

    print('%s arrives at the airport at %.2f.' % (name, env.now))
    with ap.num_gates.request() as request:
        yield request

        #arrival_time = env.now
        print('%s enters the gate at %.2f.' % (name, env.now))
        yield env.process(ap.leave(name))
        stats.addCompletions()

        if(ap.num_gates.request == 0):
            ap.open = True
        else:
            ap.open = False

        #depart_time = env.now
        print('%s leaves the gate at %.2f.' % (name, env.now))


def setup(env, num_gates, wait_time, t_inter):
    airport = Airport(env, num_gates, wait_time)
    for i in range(1):
        env.process(plane(env, 'Plane %d' % i, airport))
        stats.addArrivals()

    usage_res = env.now
    while True:
        yield env.timeout(random.randint(t_inter-2, t_inter+2))
        i += 1
        env.process(plane(env, 'Plane %d' % i, airport))
        stats.addArrivals()

        #print(airport.num_gates.count)
        if not airport.open:
            stats.addBusyTime(env.now - usage_res)
            usage_res = env.now

stats = Statistics(SIM_TIME)

stats.setNumRecursos(NUM_GATES)

random.seed(RANDOM_SEED)

env = simpy.Environment()
env.process(setup(env, NUM_GATES, WAIT_TIME, T_INTER))

env.run(until=SIM_TIME)

stats.printStats("Airport")
