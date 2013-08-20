from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory   
from twisted.internet import reactor, protocol, task
import sys, os, time, atexit, string,socket
from signal import SIGTERM
from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTwisted
from twisted.application import internet, service
import os,sys,urllib,urllib2,urlparse
from twisted.web import static, server
from twisted.python import log
import conf
hostTmp = conf.hostTmp
def getIP(dn):
    return dn.split("_")[0]
def kill_request(host,port):
     connection = urllib2.build_opener().open(urllib2.Request("http://%s:%s/admin?port=%s"%(host,hiveNode[host],port)))
     send_sms("kill hive to restart ","%s:%s "%(host,port))
def send_sms(body,ip):
    data = {}
    data["to"]=conf.notify_mail
    b_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    msg="%s : %s hive kill to  restart"%(b_time,ip)
    data["subject"]=msg
    data["body"]=body
    post(conf.notify_url, data)
def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()

hiveNode={}
for dn in hostTmp.keys():
    hiveNode[getIP(dn)]="%d"%conf.manage_port
hostMap={}
hostMap=hostTmp
hostMapIt= iter(hostMap)
blackList={}
#base key get ip
def isvalid(ip,port):
    log.msg("valid %s :%s "%(ip,port))
    sql=conf.hive_valid_sql
    try:
        transport = TSocket.TSocket(ip, int(port))
        transport.setTimeout(80000)
        transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        client = ThriftHive.Client(protocol)
        transport.open()
        client.execute(sql)
        rows = client.fetchAll()
        transport.close()
        return 1
    except Thrift.TException, tx:
        log.msg("Thrift.TException, tx%s"%tx)
        transport.close()
        return 0
    except socket.error, e:
        log.msg("socket.error, e%s"%e)
        transport.close()
        return 0
    except Exception,tx:
        log.msg("Exception,tx %s"%tx)
        transport.close()
        return 0
    except :
        transport.close()
        return 0
    return 0

class ForwardServer(Protocol):   
    def __init__(self):
        self.data = ""
        self._connected = False
    def dataReceived(self, data):
        if conf.send_sql_debug >0:
           log.msg("send  query : %s"%(data))
        self.data += data   
        if self._connected and (len(self.data) > 0):
            self.connector.transport.write(self.data)   
            self.data = ""
    def connectionMade(self):
        global hostMapIt
        isValid=0
        tmp={}
        while isValid <1:
            while 1:
              try:
                 self.host=hostMapIt.next()
              except StopIteration:
                 hostMapIt = iter(hostMap)
                 self.host=hostMapIt.next()
              if not blackList.has_key(self.host):
                  break
              if blackList.keys().__len__()==hostMap.keys().__len__():
                  break

            self.port = hostMap[self.host]
            self.host = getIP(self.host)
            isValid=isvalid(self.host,self.port)
            if isValid < 1:
                blackList["%s_%s"%(self.host,self.port)] = self.port
                if conf.server_stat_debug >0:
                  log.msg("server put to blacklist: %s port %s connect "%(self.host,self.port))
            else:
                if conf.server_stat_debug >0:
                  log.msg("server alive: %s port %s connect "%(self.host,self.port))
        self.connector = reactor.connectTCP(self.host, int(self.port), ForwardClientFactory(self))
        if conf.server_stat_debug>0:
           log.msg(  "Client connected to ",self.host)
    def setConnected(self, flag):
        if flag:   
            self.onConnected()   
        else:   
            self.transport.loseConnection()   
        self._connected = flag   
  
    def onConnected(self):   
        if len(self.data) > 0:   
            self.connector.transport.write(self.data)   
            self.data = ""   
  
    def connectionLost(self, reason):   
        self.connector.transport.loseConnection()   
        self._connected = False
        if conf.server_stat_debug >0:
           log.msg("Client disonnected")
  
class ForwardClient(Protocol):   
    def __init__(self, forward):   
        self.forward = forward   
  
    def dataReceived(self, data):   
        if data.find("SemanticException")>0:
            if conf.rec_error_debug >0:
              log.msg( "SQL EXEC ERROR: %s"%(data))
        self.forward.transport.write(data)   
  
    def connectionMade(self):
        if conf.server_stat_debug >0:
           log.msg(  "Connected to server")
        self.forward.setConnected(True)   
  
    def connectionLost(self, reason):   
        self.forward.setConnected(False)
        if conf.server_stat_debug >0:
           log.msg(  "Disconnected from server")
  
class ForwardServerFactory(ServerFactory):
    def __init__(self):
        pass
    def buildProtocol(self, addr):
        return ForwardServer() #self.host, self.port)
  
class ForwardClientFactory(ClientFactory):   
    def __init__(self, forward):   
        self.forward = forward   
  
    def buildProtocol(self, addr):   
        return ForwardClient(self.forward)   
  
    def clientConnectionFailed(self, connector, reason):   
        self.forward.transport.loseConnection()
def timer_do():
     lc = task.LoopingCall(trythrift)
     lc.start(conf.black_check_time*60)
def trythrift():
    global  blackList
    if conf.server_stat_debug >0 :
       log.msg("every %d min to check blackList")
    tmp={}
    if blackList.__len__()>0:
      for host in  blackList.keys():
        if not blackList.has_key(host):
           continue
        if isvalid(getIP(host),blackList[host])>0:
            if conf.server_stat_debug >0:
               log.msg("host remove from blackList",host)
        else:
            tmp[host]=blackList[host]
            kill_request(getIP(host),blackList[host])
        blackList = tmp
from twisted.application import internet,service
server_factory = ForwardServerFactory()
listen_port=conf.ha_port
application = service.Application("HiveKeeper")
timer_do()
internet.TCPServer(listen_port,server_factory).setServiceParent(application)
