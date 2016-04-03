import simpy
import random
import datetime

Seed = datetime.datetime.time(datetime.datetime.now())

LargBandaLan = 10                                       #largura da banda LAN em mgbits
OvhdFrame = 18                                          #numero de bytes no inicio de um pacote
MSS = 1460                                              #bytes tamanho maximo de um pacote
RouterLatencia = 0.00005                                #Tempo latencia entre pacotes 50 μs/pct == 0.00005s/pct

LargBandaLink = 7                                       # 56Kbps == 7 Kbyte/s
RttAtrasoNet = 0.1                                      # 100 ms = 0.1 s
TaxaDadosNet = 2.5                                      # 20Kbps == 2.5 Kbyte/s

TaxaBrowser = 0.3                                       #num pedidos por segundo

NumMicros = 150                                         #num micros na rede
PorcMicrosUsage = 10                                    #porcentagem de micros ativos
NumMicrosActive = (NumMicros/100) * PorcMicrosUsage     #num micros ativos na rede

PedidoHTTPMedio = 290                                   #bytes, tamanho medio da requisicao http para servidor

TamanhoMedioDocs = 22.23                                #kb

TamanhoDocs = [0.8, 5.5, 80, 800]                       # KByte
FrequenciaDocs = [35, 50, 14, 1]                        # %


RequestID = 0

Pct_list = []

SIM_TIME = 20

class Pct(object):
    def __init__(self, requisicaoID, partePCT, numPartsTotal, sizePct):
        self.requisicaoID = requisicaoID
        self.partePCT = partePCT
        self.numPartsTotal = numPartsTotal
        self.sizePct = sizePct

class LinkSai(object):
    def __init__(self, env, rttAtrasoNet, taxaDadosNet):
        self.env = env
        self.rttAtrasoNet = rttAtrasoNet
        self.taxaDadosNet = taxaDadosNet
        self.conexao = simpy.Resource(env, 1)

    def takePct(self, pacote):
        time_to_pass = int(pacote.sizePct/self.taxaDadosNet) + 1

        for i in range(0, time_to_pass):
            yield self.env.timeout(self.rttAtrasoNet)
            print('Requisição: %s Pacote: %s tamPct: %s saiu do roteador: %.2f' %
                  (pacote.requisicaoID, pacote.partePCT, pacote.sizePct, env.now))



class Router (object):
    def __init__(self, env, numMicros, taxa_browser, latencia_rout, mss, ovh_frame):
        self.env = env

        #aqui ele pega o numero de micros na minha rede, somente
        #os ativos. Latencia do rout que é o tempo de espera entre
        #um pacote e outro
        self.numMicros = numMicros
        self.taxa_browser = taxa_browser
        self.latencia_rout = latencia_rout

        #isso aqui é informação do tamanho maximo de pacote q o
        #roteador envia, e o segundo variavel é pq cada pacote
        #deve conter esse numero de byte estra
        self.mss = mss
        self.ovh_frame = ovh_frame

        #aqui poe o tanto de recursos q o roteador vai precisar
        #botei inicial somente 1
        self.conexao = simpy.Resource(env, 1)

    def makeAPctNavServer(self, requisicaoID, sizeDoc):
        #calcular quantos datagramas esta requisicao esta consumindo
        #inicialmente 1 requisicao = datagrama

        #converte de kb para byte
        #tamPac = sizeDoc*1024
        #e ver quantos pacotes essa requisição requer
        num_pacs = int(sizeDoc/(self.mss - self.ovh_frame)) + 1
        print("size documento: %s num packs: %s" % (sizeDoc, num_pacs))

        #para cada pacote, é esperado um tempo de latencia
        #e depois é enviado e passado para outro pacote
        #ate o envio de todos
        for i in range(0, num_pacs):
            yield self.env.timeout(self.latencia_rout)
            Pct_list.append(Pct(requisicaoID, i, num_pacs, self.mss+self.ovh_frame))
            print('Requisição: %s Pacote: %s saiu do roteador: %.2f' % (requisicaoID, i, env.now))

    def makeAPctServerNav(self, requisicaoID, sizeDoc):
        #calcular quantos datagramas esta requisicao esta consumindo
        #inicialmente 1 requisicao = datagrama

        #converte de kb para byte
        tamPac = sizeDoc*1024
        #e ver quantos pacotes essa requisição requer
        num_pacs = int(tamPac/(self.mss - self.ovh_frame)) + 1
        print("size documento: %s num packs: %s" % (sizeDoc, num_pacs))

        #para cada pacote, é esperado um tempo de latencia
        #e depois é enviado e passado para outro pacote
        #ate o envio de todos
        for i in range(0, num_pacs):
            yield self.env.timeout(self.latencia_rout)
            Pct_list.append(Pct(requisicaoID, i, num_pacs, self.mss+self.ovh_frame))
            print('Requisição: %s Pacote: %s saiu do roteador: %.2f' % (requisicaoID, i, env.now))

def requests (env, router, requestID, sizeDoc):
    print('Requisição: %s chegou com tempo: %.2f' % (requestID, env.now))
    with router.conexao.request() as request:
        yield request

        #ficara nisso ate todos os pacotes serem enviados
        yield env.process(router.makeAPctNavServer(requestID, sizeDoc))
        print('Requisição: %s foi atendida no tempo: %.2f' %(requestID, env.now))

def requestLinkSai(env, linksai, pacote):
    with linksai.conexao.request() as request:
        yield request

            #ficara nisso ate todos os pacotes serem enviados
        yield env.process(linksai.takePct(pacote))
            #print('Requisição: %s foi atendida no tempo: %.2f' %(requestID, env.now))

def setup (env):
    #Criando o Roteador
    router = Router(env, NumMicrosActive, TaxaBrowser, RouterLatencia, MSS, OvhdFrame)
    linkSai = LinkSai(env, RttAtrasoNet, TaxaDadosNet)

    #primeiro id de requisição
    RequestID = 0
    for i in range(4):
        #cria um processo no roteador
        env.process(requests(env, router, RequestID, PedidoHTTPMedio))
        RequestID = RequestID + 1

    while True:
        yield env.timeout(TaxaBrowser / NumMicrosActive)
        env.process(requests(env, router, RequestID, PedidoHTTPMedio))
        RequestID = RequestID + 1

        if len(Pct_list) > 0:
            pacote = Pct_list.pop(0)

            #ficara nisso ate todos os pacotes serem enviados
            env.process(requestLinkSai(env, linkSai, pacote))


env = simpy.Environment()
env.process(setup(env))

env.run(until=SIM_TIME)
