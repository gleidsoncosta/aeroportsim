import simpy
import random
import datetime
import time
from Statistics import StatisticsRouter
from Statistics import StatisticsLinkSai
from Statistics import StatisticsLinkEn


Seed = time.time()

LargBandaLan = 10                                       #largura da banda LAN em mgbits
OvhdFrame = 18                                          #numero de bytes no inicio de um pacote
MSS = 1460                                              #bytes tamanho maximo de um pacote
RouterLatencia = 0.00005                                #Tempo latencia entre pacotes 50 μs/pct == 0.00005s/pct

LargBandaLink = 7                                       # 56Kbps == 7 Kbyte/s
RttAtrasoNet = 0.1                                      # 100 ms = 0.1 s
TaxaDadosNet = 2.5                                      # 20Kbps == 2.5 Kbyte/s

TaxaBrowser = 0.3                                       #num pedidos por segundo

NumMicros = 150                                         #num micros na rede
PorcMicrosUsage = 10/100                                #porcentagem de micros ativos
NumMicrosActive = NumMicros * PorcMicrosUsage           #num micros ativos na rede

PedidoHTTPMedio = 290                                   #bytes, tamanho medio da requisicao http para servidor

TamanhoMedioDocs = 22.23                                #kb

TamanhoDocs = [0.8, 5.5, 80, 800]                       # KByte
FrequenciaDocs = [35, 50, 14, 1]                        # %


RequestID = 0

Pct_list = []
Req_list = []
Doc_list = []

SIM_TIME = 20

EstatisticasLinkSai = StatisticsLinkSai
EstatisticasLinkEn = StatisticsLinkEn
EstatisticasRouter = StatisticsRouter

class Pct(object):
    def __init__(self, requisicaoID, partePCT, numPartsTotal, sizePct):
        self.requisicaoID = requisicaoID
        self.partePCT = partePCT
        self.numPartsTotal = numPartsTotal
        self.sizePct = sizePct

class Requisicao(object):
    def __init__(self, requisicaoID, size, complete):
        self.requisicaoID = requisicaoID
        self.size = size
        self.complete = complete

class Doc(object):
    def __init__(self, requisicaoID, size):
        self.requisicaoID = requisicaoID
        self.size = size

class LinkSai(object):
    def __init__(self, env, rttAtrasoNet, taxaDadosNet):
        self.env = env
        self.rttAtrasoNet = rttAtrasoNet
        self.taxaDadosNet = taxaDadosNet
        self.conexao = simpy.Resource(env, 1)

        self.req_list = []

    def takePct(self, pacote):
        found = False
        for req in self.req_list:
            if pacote.requisicaoID == req.requisicaoID:
                found = True
                req.size = req.size + pacote.sizePct - OvhdFrame
                if pacote.partePCT == (pacote.numPartsTotal):
                    req.complete = True

            break

        if not found:
            complete = False
            if pacote.partePCT == (pacote.numPartsTotal):
                complete = True
            self.req_list.append(Requisicao(pacote.requisicaoID, pacote.sizePct, complete))

        for req in self.req_list:
            print(req.complete)
            if req.complete:
                time_to_pass = int((req.size/1024)/self.taxaDadosNet) + 1
                for i in range(0, time_to_pass):
                    yield self.env.timeout(self.rttAtrasoNet)
                    print('Requisição: %s tamreq: %s saiu do Link Saida: %.2f' %
                          (req.requisicaoID, req.size, env.now))
                Req_list.append(req)

class LinkEn(object):
    def __init__(self, env, rttAtrasoNet, taxaDadosNet):
        self.env = env
        self.rttAtrasoNet = rttAtrasoNet
        self.taxaDadosNet = taxaDadosNet
        self.conexao = simpy.Resource(env, 1)

    def makeDoc(self, req):
        doc_size = random.choice(TamanhoDocs)

        time_to_pass = int((doc_size/1024)/self.taxaDadosNet) + 1
        yield self.env.timeout(self.rttAtrasoNet * time_to_pass)
        print('Requisição: %s doc size: %s saiu para o roteador: %.2f' %
                  (req.requisicaoID, doc_size, env.now))
        Doc_list.append(Doc(req.requisicaoID, doc_size))



class Router (object):
    def __init__(self, env, numMicros, taxa_browser, latencia_rout, mss, ovh_frame, largura_banda_link):
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

        self.largura_banda_link = largura_banda_link

    def makeAPctNavServer(self, requisicaoID, sizeDoc):
        #calcular quantos datagramas esta requisicao esta consumindo
        #inicialmente 1 requisicao = datagrama

        #converte de kb para byte
        #tamPac = sizeDoc*1024
        #e ver quantos pacotes essa requisição requer
        num_pacs = int(sizeDoc/(self.mss - self.ovh_frame)) + 1
        EstatisticasRouter.creatingPackages(num_pacs, env.now)
        #para cada pacote, é esperado um tempo de latencia
        #e depois é enviado e passado para outro pacote
        #ate o envio de todos
        for i in range(0, num_pacs):
            yield self.env.timeout(self.latencia_rout)
            yield self.env.timeout((self.mss/1024)/(self.largura_banda_link))
            Pct_list.append(Pct(requisicaoID, i, num_pacs-1, self.mss+self.ovh_frame))
            print('Requisição: %s Pacote: %s saiu do roteador: %.2f' % (requisicaoID, i, env.now))
            EstatisticasRouter.sendPackages(env.now)

    def makeAPctServerNav(self, requisicaoID, sizeDoc):
        #calcular quantos datagramas esta requisicao esta consumindo
        #inicialmente 1 requisicao = datagrama

        #converte de kb para byte
        tamPac = sizeDoc*1024
        #e ver quantos pacotes essa requisição requer
        num_pacs = int(tamPac/(self.mss - self.ovh_frame)) + 1
        EstatisticasRouter.creatingPackages(num_pacs, env.now)
        print("size documento: %s num packs: %s" % (sizeDoc, num_pacs))

        #para cada pacote, é esperado um tempo de latencia
        #e depois é enviado e passado para outro pacote
        #ate o envio de todos
        for i in range(0, num_pacs):
            yield self.env.timeout(self.latencia_rout)
            yield self.env.timeout((self.mss/1024)/(self.largura_banda_link))
            #Pct_list.append(Pct(requisicaoID, i, num_pacs-1, self.mss+self.ovh_frame))
            print("num pack: %s, num packs: %s" % (i, num_pacs-1))
            print('Requisição: %s Pacote: %s saiu do roteador: %.2f' % (requisicaoID, i, env.now))
            EstatisticasRouter.sendPackages(env.now)

def requests (env, router, requestID, sizeDoc, navServ):
    if navServ:
        print('Requisição Cliente ID NavServ: %s chegou com tempo: %.2f' % (requestID, env.now))
    else:
        print('Requisição Cliente ID ServNav: %s chegou com tempo: %.2f' % (requestID, env.now))
    with router.conexao.request() as request:
        yield request

        #ficara nisso ate todos os pacotes serem enviados
        if navServ:
            yield env.process(router.makeAPctNavServer(requestID, sizeDoc))
        else:
            yield env.process(router.makeAPctServerNav(requestID, sizeDoc))
        print('Requisição Cliente ID: %s foi atendida no tempo: %.2f' %(requestID, env.now))


def requestLinkSai(env, linksai, pacote):
    print('Pacote LinkSai ID: %s chegou com tempo: %.2f' % (pacote.requisicaoID, env.now))
    EstatisticasLinkSai.recivePackage(env.now)
    with linksai.conexao.request() as request:
        yield request

        #ficara nisso ate todos os pacotes serem enviados
        yield env.process(linksai.takePct(pacote))
        EstatisticasLinkSai.sendPackage(env.now)
        print('Requisição LinkSai ID: %s foi atendida no tempo: %.2f' %(pacote.requisicaoID, env.now))


def requestLinkEn(env, linken, req):
    print('Pacote LinkEn ID : %s chegou com tempo: %.2f' % (req.requisicaoID, env.now))
    EstatisticasLinkEn.reciveRequest (env.now)
    with linken.conexao.request() as request:
        yield request

        #ficara nisso ate todos os pacotes serem enviados
        yield env.process(linken.makeDoc(req))
        EstatisticasLinkEn.sendDoc(env.now)
        print('Requisição LinkEn ID: %s foi atendida no tempo: %.2f' %(req.requisicaoID, env.now))

def setup (env):
    #Criando o Roteador
    router = Router(env, NumMicrosActive, TaxaBrowser, RouterLatencia, MSS, OvhdFrame, LargBandaLink)
    linkSai = LinkSai(env, RttAtrasoNet, TaxaDadosNet)
    linkEn = LinkEn(env, RttAtrasoNet, TaxaDadosNet)

    #primeiro id de requisição
    RequestID = 0
    #for i in range(4):
    #    #cria um processo no roteador
    #    env.process(requests(env, router, RequestID, PedidoHTTPMedio))
    #    RequestID = RequestID + 1

    while True:
        yield env.timeout(TaxaBrowser / NumMicrosActive)
        env.process(requests(env, router, RequestID, PedidoHTTPMedio, True))
        RequestID = RequestID + 1

        if len(Pct_list) > 0:
            pacote = Pct_list.pop(0)

            #ficara nisso ate todos os pacotes serem enviados
            env.process(requestLinkSai(env, linkSai, pacote))

        if len(Req_list) > 0:
            req = Req_list.pop(0)

            #ficara nisso ate todos os pacotes serem enviados
            env.process(requestLinkEn(env, linkEn, req))

        if len(Doc_list) > 0:
            doc = Doc_list.pop(0)

            #ficara nisso ate todos os pacotes serem enviados
            env.process(requests(env, router, doc.requisicaoID, doc.size, False))




env = simpy.Environment()
env.process(setup(env))

env.run(until=SIM_TIME)

print("***************** Estatisticas *****************")
print("********* Roteador *********")
#print('Numero de Pacotes Enviados: %s' % EstatisticasRouter.numPackagesCreated)