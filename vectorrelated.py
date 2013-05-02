# -*- coding: utf-8 -*- 
# Author: HW <todatamining@gmail.com>
# See LICENSE.txt for details.
#!/usr/bin/env python
from __future__ import division
import math
import utility as UT
from globalvariable import *

class VectorResultCache(object):
    maxfreqOfTerm = {}
    fileNameLstOfCategory_ = {}   #not full path name
    wordlstOfFile_ = {}           #full path name
    listOfAllFileNames_ = []      #full path name
    vocabulary_ = []              #not distinct
    usingTermSelection = False
    termselection_ ={}
    @staticmethod
    def init():
        if len(VectorResultCache.vocabulary_) ==0 : #not init yet
            print "init..."
            print "start to get all training set"
            for category in UT.getFileInsideDir(TRAININGSET_DIR):
                filenamelst = UT.getFileInsideDir(TRAININGSET_DIR+category)
                VectorResultCache.fileNameLstOfCategory_[category] = filenamelst
                (VectorResultCache.listOfAllFileNames_).extend([UT.genFullPath(category,f) for f in filenamelst])
            print "start to convert all training file to word lst"
            for f in VectorResultCache.listOfAllFileNames_:
                (VectorResultCache.vocabulary_).extend(VectorResultCache.file2wordlst(f))
            #print VectorResultCache.vocabulary_
            if VectorResultCache.usingTermSelection: 
                print "start to calculate information gain"
                tmp = UT.loadObj("VectorResultCache.termselection_")
                if tmp is not None and GlobalCanModify.TERM_SELECTION_RATE in tmp:
                    VectorResultCache.termselection_ = tmp[GlobalCanModify.TERM_SELECTION_RATE]
                else:
                    for t in list(set(VectorResultCache.vocabulary_)):
                        ig = VectorResultCache.calIG(t)
                        if ig>GlobalCanModify.TERM_SELECTION_RATE:
                            VectorResultCache.termselection_[t] = ig
                        tmpdict={}
                        tmpdict[GlobalCanModify.TERM_SELECTION_RATE] = VectorResultCache.termselection_
                        UT.saveObj(tmpdict,"VectorResultCache.termselection_")
                print("Termselection:{0},{1}".format(len(VectorResultCache.termselection_.keys()),VectorResultCache.termselection_)) 
    @staticmethod
    def getVocabulary():
        return VectorResultCache.vocabulary_
    @staticmethod
    def getTermSelection():
        return VectorResultCache.termselection_.keys()
    @staticmethod
    def file2wordlst(filename):
        if filename in VectorResultCache.wordlstOfFile_:
            return VectorResultCache.wordlstOfFile_[filename]
        else:
            VectorResultCache.wordlstOfFile_[filename] = UT.extractWordList(filename)
            return VectorResultCache.wordlstOfFile_[filename];
    @staticmethod
    def listOfAllFileNames():
        VectorResultCache.init()
        return VectorResultCache.listOfAllFileNames_
    @staticmethod
    def wordlstOfFile():
        VectorResultCache.init()
        return VectorResultCache.wordlstOfFile_
    @staticmethod
    def fileNameLstOfCategory():
        VectorResultCache.init()
        return VectorResultCache.fileNameLstOfCategory_
    @staticmethod
    def getCategoryOfFile(fullpathfile):
        for category in UT.getFileInsideDir(TRAININGSET_DIR):
            for f in VectorResultCache.fileNameLstOfCategory_[category]:
                #print UT.genFullPath(category,f),fullpathfile
                if UT.genFullPath(category,f) == fullpathfile:
                    return category
        return None
#
    #G(t) = -SIGMA (p(ci)*log2(p(ci)))          --->v1
    #     +p(t)  SIGMA(p(ci|t)log2(p(ci|t)))     --->v2
    #     +p(~t) SIGMA(p(ci|~t))log2(p(ci|~t))   --->v3
    #
    #
    @staticmethod
    def calIG(term):
        #VectorResultCache.init()
        v1 = 0
        for category in VectorResultCache.fileNameLstOfCategory():
            p = len(VectorResultCache.fileNameLstOfCategory()[category]) / \
                    len(VectorResultCache.listOfAllFileNames())
            #print category,p
            v1 += -1*p*math.log(p,2)


        v2 = 0
        v3 = 0
        for category in VectorResultCache.fileNameLstOfCategory():
            cnt1 = len([f for f in VectorResultCache.fileNameLstOfCategory()[category] \
                                if term in VectorResultCache.wordlstOfFile()[UT.genFullPath(category,f)] ])
            p1 = cnt1/len([lst for lst in VectorResultCache.wordlstOfFile().values() if term in lst])
            cnt2 = len([f for f in VectorResultCache.fileNameLstOfCategory()[category] \
                                 if term not in VectorResultCache.wordlstOfFile()[UT.genFullPath(category,f)] ])
            p2 = cnt2/len([lst for lst in VectorResultCache.wordlstOfFile().values() if term not in lst])
            #print  "p({0}|{1}) = {2}".format(category,term,p1)
            #print  "p({0}|~{1}) = {2}".format(category,term,p2)
            v2 += (0 if p1==0 else p1*math.log(p1,2))
            v3 += (0 if p2==0 else p2*math.log(p2,2))

        pt = VectorResultCache.getVocabulary().count(term) / len(VectorResultCache.getVocabulary())
        v2 =  pt * v2
        v3 =  (1-pt) * v3
        return v1+v2+v3
    '''
        print "p({0}) = {1}".format(term,pt)
        print "v1",v1
        print "v2",v2
        print "v3",v3
        print term,v1+v2+v3
    '''
 
def pearsonDistance(v1,v2):
    #print v1,v2
    vmul=[i*j for i,j in zip(v1,v2)]
    v1s=[i*i for i in v1]
    v2s=[i*i for i in v2]
    return sum(vmul)/(math.sqrt(sum(v1s))*math.sqrt(sum(v2s))) + 0.0000000001

#        
#           freq of termi in docj
# TFij =  ---------------------------
#         max freq of all items in docj
#
#docj is a list of all items in docj
def TFij(termi,filename,docj):
    freq = docj.count(termi)
    if filename not in VectorResultCache.maxfreqOfTerm:
        maxfreq = 0.
        for t in list(set(docj)):
            maxfreq = max(docj.count(t),maxfreq) #max(docj.count(t),freq)
        VectorResultCache.maxfreqOfTerm[filename] = maxfreq
    #print freq,VectorResultCache.maxfreqOfTerm[filename],freq/VectorResultCache.maxfreqOfTerm[filename]
    return freq/VectorResultCache.maxfreqOfTerm[filename]
#
#
# DF =  # of docs which contain termi
#
# docList must be a list of doc
# doc is a list of all items in doc
#    
def DFi(termi,docsList):
    cnt = 0;
    for doc in docsList:
        if termi in doc:
            cnt+=1
    return cnt

#
#                # of all docs
# IDFi = log----------------------------------
#                     DFi    
# docList must be a list of doc
# doc is a list of all items in doc
def IDFi(termi,docsList):
    return len(docsList)/DFi(termi,docsList)

# docList must be a list of doc
# doc is a list of all items in doc
# TF.IDF
def weightij(termi,filename,docj,docsList):
    #print termi,docj, TFij(termi,docj),math.log(IDFi(termi,docsList),10)
    return (TFij(termi,filename,docj) * math.log(IDFi(termi,docsList),10)) + 0.0000000001
    
