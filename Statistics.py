
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
       # print("Tempo Medio Servico: ......%.2f" % self.avgServiceTime())


class StatisticsRouter(object):
    numHttpRequests = 0
    numPackagesCreated = 0
    timePackagesCreated = 0
    timePackagesSend = 0
    busyTime = 0

    def creatingPackages(self, numPackages, time):
        self.numPackagesCreated = numPackages
        self.timePackagesCreated = time
        self.numHttpRequests += 1

    def sendPackages(self, time):
        self.timePackagesSend = time
        self.busyTime = self.timePackagesSend - self.timePackagesCreated

class StatisticsLinkSai(object):
    numPackagesRecived = 0
    timePackageRecived = 0
    timePackageSend = 0
    busyTime = 0

    def recivePackage(self, time):
        self.numPackagesRecived += 1
        self.timePackageRecived = time

    def sendPackage(self, time):
        self.timePackageSend = time
        self.busyTime = self.timePackageSend - self.timePackageRecived

class StatisticsLinkEn(object):
    numRequestRecived = 0
    timeRequestRecived = 0
    timeDocSend = 0
    budyTime = 0
    def reciveRequest(self, time):
        self.numRequestRecived += 1
        self.timeRequestRecived = time

    def sendDoc(self, time):
        self.timeDocSend = time
        self.budyTime += self.timeDocSend - self.timeRequestRecived
