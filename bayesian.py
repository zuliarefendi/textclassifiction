# -*- coding: utf-8 -*- 
# Author: HW <todatamining@gmail.com>
# See LICENSE.txt for details.
#!/usr/bin/env python

import math
import time
import utility as UT
from globalvariable import *
                
class BayesianResultCache(object):
    wordsInEachCategory={}
    filesInEachCategory={}
    VocalbularyCnt=0

def getV():
    if (BayesianResultCache.VocalbularyCnt!=0):
        return BayesianResultCache.VocalbularyCnt
    lst = []
    for dirname in UT.getFileInsideDir(TRAININGSET_DIR):
        lst.extend(getAllWordsByCategory(dirname))
    lst=list(set(lst))
    BayesianResultCache.VocalbularyCnt = len(lst)
    return BayesianResultCache.VocalbularyCnt

def getAllWordsByCategory(category):
    if(category in BayesianResultCache.wordsInEachCategory):
        return BayesianResultCache.wordsInEachCategory[category]
    else:
        lst = []
        BayesianResultCache.filesInEachCategory[category] = 0
        for f in UT.getFileInsideDir(TRAININGSET_DIR+category):
            lst.extend(UT.extractWordList(TRAININGSET_DIR+category+"/"+f))    
            BayesianResultCache.filesInEachCategory[category]+=1
        BayesianResultCache.wordsInEachCategory[category] = lst
        return lst

def pWiCj(w,category): #p(wi|cj) term w occurance in all docs whose category is category
                     #category is dir name /category name
    lst = getAllWordsByCategory(category)
    nij = lst.count(w.lower())
    return (nij+1.)/(len(lst)+getV())

def getPcj(category): #category category probility
    categorycnt = len(UT.getFileInsideDir(TRAININGSET_DIR+category))
    totalcnt = 0.;
    for dirname in UT.getFileInsideDir(TRAININGSET_DIR):
        totalcnt += len(UT.getFileInsideDir(TRAININGSET_DIR+dirname))
    return categorycnt/totalcnt


def evaluate(tobeEvaFile):
    if tobeEvaFile[0:4].upper()=="HTTP" or tobeEvaFile[0:4].upper()=="WWW.":
        tobeEvaFile = UT.getMainContent(tobeEvaFile)
    st = time.time()
    result={}
    result_log={}
    testsetlst = UT.extractWordList(tobeEvaFile)
    for category in UT.getFileInsideDir(TRAININGSET_DIR):
        p=getPcj(category) #non-log
        p_log=math.log(getPcj(category),10) #log
        for term in testsetlst:
            #print(p*pWiCj(item,category),abs(math.log(p*pWiCj(item,category))))
            p_log += (math.log(pWiCj(term,category),10)) #log
            p *= pWiCj(term,category) #non-log
        result_log[category]=p_log  #log
        result[category]=p          #non-log
    sr = sorted(result.items(), lambda x, y: cmp(y[1], x[1]))
    srl = sorted(result_log.items(), lambda x, y: cmp(y[1], x[1]))

    #print result
    UT.myprint("-----------------------------------------------------------statistics infomation")
    for category in BayesianResultCache.filesInEachCategory:
        UT.myprint ('\t traingfiles of {0:15}:{1:3},   words:{2:5}'.format(category,BayesianResultCache.filesInEachCategory[category],len(BayesianResultCache.wordsInEachCategory[category])))

    UT.myprint ("\t vocabulary of training set number:{0}".format(BayesianResultCache.VocalbularyCnt))
    UT.myprint ("\t words in test set:".format(len(testsetlst)))
    UT.myprint("-------------------------------------------------------------------------non-log")
    for item in sr:
        UT.myprint("\t{0}".format(item))
    UT.myprint("-------------------------------------------------------------------------after log")
    result = ""
    for item in srl:
        select = ""
        if item[0].strip()==(srl[0][0]).strip():
            select = "<----- SELECTED"
            result = item[0].strip()
        UT.myprint("\t{0} {1}".format(item,select))
        #print "\t",item,"<----- SELECTED" if item[0].strip()==(srl[0][0]).strip() else ""
    UT.myprint("-------------------------------------------------------------------------running time")
    UT.myprint("\t {0} seconds".format(time.time()-st))    
    return result


 
