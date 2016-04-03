
class Statistics(object):
    observation_time = 0
    arrivals_num = 0
    completions_num = 0
    busy_time = 0

    num_recursos = 0


    def __init__(self, observation_time):
        self.observation_time = observation_time
        self.arrivals_num = 0
        self.completions_num = 0
        self.busy_time = 0
        self.num_recursos = 0

    def setObservationTime(self, t):
        self.observation_time = t

    def addArrivals(self):
        self.arrivals_num += 1

    def addCompletions(self):
        self.completions_num += 1

    def addBusyTime(self, t):
        self.busy_time += t

    def setNumRecursos(self, t):
        self.num_recursos = t

    def arrivalRate(self):
        return self.arrivals_num/self.observation_time

    def throughput(self):
        return self.completions_num/self.observation_time

    def usage(self):
        return self.busy_time/self.observation_time

    def avgServiceTime(self):
        return self.busy_time/self.completions_num


    def printStats(self, titulo):
        print("---------------%s Statistics -----------------------" % titulo)
        print(" Numero de Recursos: %d" % self.num_recursos)

        print("Tempo de Observacao: ......%d" % self.observation_time)
        print("Numero de Chegadas:  ......%d" % self.arrivals_num)
        print("Numero de Saidas:    ......%d " % self.completions_num)
        print("Tempo Recursos Ocupados: ..%.2f" % self.busy_time)

        print("Taxa de chegada: ..........%.2f" % self.arrivalRate())
        print("Taxa de saida:   ..........%.2f" % self.throughput())
        print("Utilizacao:  ..............%.2f%%" % (self.usage()*100))
        #print("Tempo Medio Servico: ......%.2f" % self.avgServiceTime())

