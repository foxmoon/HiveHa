from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
import cgi,os,time
from twisted.internet import defer
import conf
class FormPage(Resource):
    def render_GET(self, request):
        port=request.args["port"][0]
        log.msg("port : %s rec start"%port)
        if int(port)>10:
           log.msg("port start defer ")
           killHive(port)
        return '<html><body>succ</body></html>'
def killHive(port):
    log.msg("killHive port: %s "%port)
    rfile=os.popen("netstat -lnp | grep %s | grep -o .......java"%port,"r")
    r=rfile.read()
    rfile.close()
    if r.find("java")>0:
        cmd = "kill -9 "+r.split("/java")[0]
        log.msg(cmd)
        os.system(cmd)
        run_hive(port)
        return 1
    else:
        run_hive(port)
        return 1 
    return 0  
def run_hive(port):
    cmd="%s  %s &"%(conf.start_hive_cmd,port)
    log.msg(cmd)
    body=os.popen(cmd,"r")
    body.close()
    time.sleep(2)
root = Resource()
root.putChild("admin", FormPage())
from twisted.application import internet,service
server_factory = Site(root)
listen_port=conf.manage_port
application = service.Application("HiveKeeperNode")
internet.TCPServer(listen_port,server_factory).setServiceParent(application)
