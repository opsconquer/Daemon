#coding:utf-8
#
import sys, time, datetime
import json

from DaemonClass import Daemon
from collections import OrderedDict
from cpu import CPUInfoPollster
#import util
import re

class TestMonitor(Daemon):
    intvl = 10
    def __init__(self,
               pidfile='/tmp/test-monitor.pid',
               stdin='/dev/stdin',
               stdout='/dev/stdout',
               stderr='/dev/stderr',
               intvl=10,
               logfile='/opt/monitor.log'):
        Daemon.__init__(self, pidfile=pidfile, stdin=stdin, stdout=stdout, stderr=stderr)
        # Set poll interval
        TestMonitor.intvl = intvl
        # Set logfile
        self._logfile = logfile
    

    '''
    Basic poll task
    '''
    def _poll(self):
        # Get cpu info
        cpu_info = CPUInfoPollster().getSample()

        poll_info = OrderedDict()
    
        poll_info['cpu_info'] = cpu_info

        return cpu_info

    def run(self):
	c = 0
        while True:
            poll_info = self._poll()
            # Add timestamp
            content = time.asctime(time.localtime()) + '\n'
            for item in poll_info:
                content += '%s: %s\n' %(item, poll_info[item])
            content += '----------------------------\n\n'
	    file = open(self._logfile, "w" )  
            file.write( content )  
            file.close()  
            #util.appendFile(content, self._logfile)
            time.sleep(TestMonitor.intvl)
            c = c + 1
            
if __name__ == "__main__":
    daemon = TestMonitor(pidfile='/tmp/test-monitor.pid', 
                           intvl=10)
   
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print 'Unknown command'
            sys.exit(2)
    else:
        print 'USAGE: %s start/stop/restart' % sys.argv[0]
        sys.exit(2)

