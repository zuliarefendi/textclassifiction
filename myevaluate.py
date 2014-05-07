# -*- coding: utf-8 -*- 
# Author: HW <todatamining@gmail.com>
# See LICENSE.txt for details.
#!/usr/bin/env python

import os
import time
import sys
import os.path
from globalvariable import *
import knn
import bayesian
from time import gmtime, strftime

# merged = list(set(start("B")+start("K")))
# combine knn and baysian --->multi stategy
# K ----- KNN
# B ----- Baysian
def start(which,ratio = 0.01):
    GlobalCanModify.TERM_SELECTION_RATE = ratio 
    inf = open('./tobeevaluated.txt','r')
    evaluatelog = open('./evaluate.log','a')
    st = time.time()
    evaluatelog.write("\n{0},ratio:{1} start at:{2}\n".format("[KNN]" if "K" == which.upper() else "[Bayesian]" ,ratio,strftime("%Y-%m-%d %H:%M:%S", gmtime())))

    rsltList = []
    correctlst = []
    totalcnt = 0
    okcnt = 0
    for f in inf:
        totalcnt +=1
        listf = f.split()
        get = "UNKNOWN"
        if "K" == which.upper():
            get = knn.evaluate(listf[1],True)
        else:
            get = bayesian.evaluate(listf[1])
        rslt = "ok" if listf[0] == get else "failed-"+get
        if "ok" == rslt:
            okcnt += 1
            correctlst.append(totalcnt)
        rsltList.append("{0:25}{1:80}".format(rslt,f))
    print "====================================================================================================="
    i = 1
    for r in rsltList:
        print("{0:3}:{1}".format(i,r.rstrip())) 
        evaluatelog.write("{0:3}:{1}\n".format(i,r.rstrip()))
        i+=1
    print "====================================================================================================="
    te = "{0:20}:{1}".format("Total evaluated",totalcnt)
    ct = "{0:20}:{1}".format("Correct",okcnt)
    cl = "{0:20}:{1}".format("Correct list",correctlst)
    print(te)
    evaluatelog.write(te+"\n")
    print (ct)
    evaluatelog.write(ct+"\n")
    print(cl)
    evaluatelog.write(cl+"\n")
    cost = time.time()-st
    evaluatelog.write("Total used {0:.2f} seconds, {1:.2f} each\n\n".format(cost,cost/i))
    return correctlst

