import simpy
import random
import datetime
import time
from Statistics import StatisticsRouter
from Statistics import StatisticsLinkSai
from Statistics import StatisticsLinkEn


Seed = time.time()

NumMicros = 15
Latencia = 0.00005  # 50 μs == 0.00005s
Conexao = 7  # 56Kbps == 7 Kbyte/s
TaxaTransferencia = 2.5  # 20Kbps == 2.5 Kbyte/s
RequisicaoHTTP = 0.1  # 100 bytes == 0.1 Kbytes
RTT = 0.1  # 100 ms == 0.1s
RequestPerSecond = 0.3
TamanhoRequisicoes = [0.8, 5.5, 80, 800]  # KByte

FrequenciaOcorrencias = [35, 50, 14, 1]  # %

SIM_TIME = 200


class Router (object):
    def __init__(self, env, numMicros, latencia, conexao, requisicaoHTTP, requestPerSecond):
        self.env = env
        self.numMicros = numMicros
        self.latencia = latencia
        self.conexao = simpy.Resource(env, conexao)
        self.requisicaoHTTP = requisicaoHTTP
        self.requestPerSecond = requestPerSecond

class WebService (object):
    def __init__(self, env, taxaTransferencia, RTT, tamanhoRequisicao):
        self.env = env
        self.taxaTransferencia = taxaTransferencia
        self.RTT = RTT
        self.tamanhoRequisicao = tamanhoRequisicao
    # A resposta deve ser um dos tamanhos de requisições pela taxa de transferencia + o RTT (Round Trip Time)
    def reply (self):
        yield self.env.timeout(random.choice(self.tamanhoRequisicao) * self.taxaTransferencia + self.RTT)

def requests (env, router, requestID, webService):
    size = router.requisicaoHTTP
    print('Requisição: %s chegou com tempo: %.2f' % (requestID, env.now))
    with router.conexao.request() as request:
        yield request

        #arrivalTime = env.now
        print('Requisição: %s foi atendida no tempo: %.2f' %(requestID, env.now))
        yield env.process(webService.reply())

def setup (env):
    #Criando o Roteador
    router = Router(env, NumMicros, Latencia, Conexao, RequisicaoHTTP, RequestPerSecond)

    #Criando o WebService
    webService = WebService(env, TaxaTransferencia,RTT, TamanhoRequisicoes)

    #totalResquest = RequestPerSecond * NumMicros
    for i in range(4):
        env.process(requests(env, router, i, webService))

    while True:
        yield env.timeout(RequestPerSecond)
        i += 1
        env.process(requests(env, router, i, webService))

        print(router.conexao.count)



env = simpy.Environment()
env.process(setup(env))

env.run(until=SIM_TIME)
