
class Statistics(object):
    observation_time = 0
    arrivals_num = 0
    completions_num = 0
    busy_time = 0

    def __init__(self, observation_time):
        self.observation_time = observation_time
        self.arrivals_num = 0
        self.completions_num = 0
        self.busy_time = 0

    def __setObservationTime(self, t):
        self.observation_time = t

    def addArrivals(self):
        self.arrivals_num += 1

    def addCompletions(self):
        self.completions_num += 1

    def addBusyTime(self, t):
        self.busy_time += t

    def printStats(self):
        print("Tempo de Observacao %d" % (self.observation_time))
        print("Numero de Chegadas %d" % self.arrivals_num)
        print("Numero de Saidas %d " % self.completions_num)
        print("Tempo ocupado %d" % self.busy_time)
