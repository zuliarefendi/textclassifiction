# -*- coding: utf-8 -*- 
# Author: HW <todatamining@gmail.com>
# See LICENSE.txt for details.
#!/usr/bin/env python

import math
import time
import vectorrelated as VR
import utility as UT
from globalvariable import *
from collections import Counter

class knnResultCache(object):
    fileMatrix = {}
       
#convert file to vector
def calWeightVector(filename,wordlstOfFile,termselection):
    lst = []
    if termselection:
        dimension = list(set(VR.VectorResultCache.getTermSelection()))
    else:
        dimension = list(set(VR.VectorResultCache.getVocabulary()))
        
    for t in dimension:
        lst.append(VR.weightij(t,filename,wordlstOfFile,VR.VectorResultCache.wordlstOfFile().values()))
    return lst


#compute the corresponding TF-IDF(weight) vector for each file in training set
# set termselection to None means turn off termselection
def evaluate(tobeEvaFile,termselection):
    if tobeEvaFile[0:4].upper()=="HTTP" or tobeEvaFile[0:4].upper()=="WWW.":
        tobeEvaFile = UT.getMainContent(tobeEvaFile)

    st = time.time();
    #training
 
    VR.VectorResultCache.usingTermSelection = termselection
    for f in VR.VectorResultCache.listOfAllFileNames():
        knnResultCache.fileMatrix[f] = calWeightVector(f,VR.VectorResultCache.wordlstOfFile()[f],termselection)
        #print("==============",f,knnResultCache.fileMatrix[f])
        UT.myprint("==calculate weight(TF.IDF) vector for {0}".format(f))

    #test
    testsetlst = VR.VectorResultCache.file2wordlst(tobeEvaFile)
    vectorOfTobeEvaluatedFile = calWeightVector(tobeEvaFile,testsetlst,termselection)

    result={}
    for key in knnResultCache.fileMatrix:
        dist = VR.pearsonDistance(vectorOfTobeEvaluatedFile,knnResultCache.fileMatrix[key])
        UT.myprint ('simularity to {0:80} is {1:20}'.format(key,dist))
        result[key]=dist
 
    #print result
    UT.myprint("-----------------------------------------------------------statistics infomation")
    #print VR.VectorResultCache.fileNameLstOfCategory()
    #print VR.VectorResultCache.wordlstOfFile()
    for category in VR.VectorResultCache.fileNameLstOfCategory():
        wordscnt=0
        for f in VR.VectorResultCache.fileNameLstOfCategory()[category]:
            wordscnt += len(VR.VectorResultCache.wordlstOfFile()[UT.genFullPath(category,f)])
#        UT.myprint "\t","trainingfiles of ",category," : ",len(VR.VectorResultCache.fileNameLstOfCategory()[category]), \
#                                                ",words:",wordscnt
        UT.myprint ('\t training files of {0:15}:{1:3},   words:{2:5}'.format(category,len(VR.VectorResultCache.fileNameLstOfCategory()[category]),wordscnt))
    UT.myprint ("\t vocabulary of training set number:{0}".format(len(list(set(VR.VectorResultCache.getVocabulary())))))
    UT.myprint ("\t words in test set:{0}".format(len(testsetlst)))

    sr = sorted(result.items(), lambda x, y: cmp(y[1], x[1]))
    UT.myprint("----------------------------------------------------------------------")
    i = 0
    categorylist = []
    for item in sr:
        i+=1
        if i<=5:
            categorylist.append(VR.VectorResultCache.getCategoryOfFile(item[0]))
        UT.myprint ('\t{0:80} cossim:{1:20}\t{2}'.format(item[0],item[1],"TOP "+str(i) if i<=5 else ""))
       
    UT.myprint("-------------------------------------------------------------------------running time")
    UT.myprint( "\t{0} seconds".format(time.time()-st))
    most_common,num_most_common = Counter(categorylist).most_common(1)[0]
    UT.myprint( "{0},{1}".format(most_common,num_most_common))
    return most_common
