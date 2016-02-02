#coding:utf-8
#
#cpu.py
from collections import OrderedDict
#import util
import os
import time
from PollsterClass import Pollster

'''
Read cpu info from /proc/cpuinfo
'''

class CPUInfoPollster(Pollster):
    def __init__(self, name='cpu_info'):
        super(CPUInfoPollster, self).__init__(name=name)

    def getSample(self):
        cpu_info = OrderedDict()
        proc_info = OrderedDict()

        nprocs = 0

        try:
            #if util.is_exist('/proc/cpuinfo'):
            if os.path.exists('/proc/cpuinfo'):
                with open('/proc/cpuinfo') as f:
                    for line in f:
                        if not line.strip():
                            cpu_info['proc%s' % nprocs] = proc_info
                            nprocs += 1
                            proc_info = OrderedDict()
                        else:
                            if len(line.split(':')) == 2:
                                proc_info[line.split(':')[0].strip()] = line.split(':')[1].strip()
                            else:
                                proc_info[line.split(':')[0].strip()] = ''
        except:
            print "Unexpected error:", sys.exc_info()[1]
        finally:
	    #print cpu_info
	    #print proc_info
            return cpu_info
#if __name__=="__main__":
#	c = CPUInfoPollster()
#	c.getSample()
