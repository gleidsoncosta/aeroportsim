
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
    startObserv = 0
    endObser = 0

    def start(self, time):
        if self.startObserv == 0:
            self.startObserv = time

    def end(self, time):
        self.endObser = time

    def creatingPackages(self, numPackages, time):
        self.numPackagesCreated += numPackages
        self.timePackagesCreated = time
        self.numHttpRequests += 1

    def sendPackages(self, time):
        self.timePackagesSend = time
        self.busyTime = self.timePackagesSend - self.timePackagesCreated

    def printData(self):
        print("***************** Estatisticas *****************")
        print("********* Roteador *********")
        print("Número de Pacotes Criados: %s" % self.numPackagesCreated)
        print("Tempo ocupado: %s" % self.busyTime)
        print("Taxa de entrada: %s" % (self.numHttpRequests / self.busyTime))
        print("Taxa de saida: %s" % (self.numPackagesCreated / self.busyTime))
        print("Throughput: %s" % (self.numPackagesCreated / self.busyTime))
        print(
            "StartObserver: %s ------ EndObserver: %s" % (self.startObserv, self.endObser))
        print("Utilização: %.2f%%" % ((self.busyTime / (self.endObser - self.startObserv)) * 100))

class StatisticsLinkSai(object):
    numPackagesRecived = 0
    timePackageRecived = 0
    numRequestFile = 0
    timePackageSend = 0
    busyTime = 0
    startObserv = 0
    endObser = 0

    def start(self, time):
        if self.startObserv == 0:
            self.startObserv = time

    def end(self, time):
        self.endObser = time

    def recivePackage(self, time):
        self.numPackagesRecived += 1
        self.timePackageRecived = time

    def sendPackage(self, time):
        self.timePackageSend = time
        self.busyTime = self.timePackageSend - self.timePackageRecived
        self.numRequestFile += 1

    def printData(self):
        print("********* Link Saída *********")
        print("Número de pacotes Recebidos: %s" % self.numPackagesRecived)
        print("Tempo ocupado: %s" % self.busyTime)
        print("Taxa de entrada: %s" % (self.numPackagesRecived / self.busyTime))
        print("Taxa de saída: %s" % (self.numPackagesRecived / self.busyTime))
        print("Throughput: %s" % (self.numRequestFile / self.busyTime))
        print("StartObserver: %s ------ EndObserver: %s" % (self.startObserv, self.endObser))
        print("Utilização: %.2f%%" % ((self.busyTime / (self.endObser - self.startObserv)) * 100))

class StatisticsLinkEn(object):
    numRequestRecived = 0
    timeRequestRecived = 0
    timeDocSend = 0
    busyTime = 0
    startObserv = 0
    endObser = 0
    numDocSend = 0

    def start(self, time):
        if self.startObserv == 0:
            self.startObserv = time

    def end(self, time):
        self.endObser = time

    def reciveRequest(self, time):
        self.numRequestRecived += 1
        self.timeRequestRecived = time

    def sendDoc(self, time):
        self.timeDocSend = time
        self.busyTime += self.timeDocSend - self.timeRequestRecived
        self.numDocSend += 1

    def printData(self):
        print("********* Link Entrada *********")
        print("Número de pacotes Recebidos: %s" % self.numRequestRecived)
        print("Tempo ocupado: %s" % self.busyTime)
        print("Taxa de entrada: %s" % (self.numRequestRecived / self.busyTime))
        print("Taxa de saída: %s" % (self.numDocSend / self.busyTime))
        print("Throughput: %s" % (self.numRequestRecived / self.busyTime))
        print("StartObserver: %s ------ EndObserver: %s" % (self.startObserv, self.endObser))
        print("Utilização: %.2f%%" % ((self.busyTime / (self.endObser - self.startObserv)) * 100))