# -*- coding: utf-8 -*-
# Author: HW <todatamining@gmail.com>
# See LICENSE.txt for details.
#!/usr/bin/env python

import re
import os
import math
import sys
import pickle
from nltk.stem.wordnet import WordNetLemmatizer
import os.path,subprocess

lmtzr = WordNetLemmatizer()
this_dir,this_filename = os.path.split(os.path.abspath(__file__))

sys.path.append(this_dir)
import en
from globalvariable import *

CACHE_DIR = "./.cache"
def myprint(sstr):
    if DEBUG_ON:
        print sstr

def saveObj(obj,writeTo):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    with open(CACHE_DIR+"/"+writeTo,"wb") as f:
        pickle.dump(obj,f)

def loadObj(loadFrom):
    try:
        with open(CACHE_DIR+"/"+loadFrom,"rb") as f:
            return pickle.load(f)
    except:
        return None


def genFullPath(category,filename):
    return TRAININGSET_DIR+category+"/"+filename

def contents(filename):
    with file(filename) as f: return f.read()

def convertNoun(srclst): 
    return [lmtzr.lemmatize(item) for item in srclst]

def convertVerb(srclst):
    dstlst = []
    itemnew=""
    for item in srclst:
        #print(item)  ############################when nos lib give error
        #if (item.endswith("ed") or item.endswith("ing")) \
        if en.is_verb(item) \
            and (not en.is_noun(item)) \
            and (not en.is_adjective(item)) \
            and (not en.is_adverb(item)) \
            and (item not in WIERDWORDS):
            try:
                itemnew = en.verb.present(item) 
            except:
                print "unrecognized word:",item
                itemnew = item
        else:
            itemnew = item;
        dstlst.append(itemnew)
    return dstlst
 
def removeWithStoplist(srclst,stopfile):
    contt = contents(stopfile)
    stoplist = contt.split("\n")
    return [item.lower() for item in srclst if item.lower() not in stoplist]

def getFileInsideDir(dirname):
    return os.listdir(dirname)

def extractWordList(filename):
    contt = contents(filename)
    contt=contt.replace("’", "'");
    contt=contt.replace("“", "'");
    contt=contt.replace("”", "'");
    contt=contt.replace("—", "-");
    contt=contt.replace("-", " ");
    contt=contt.replace("_", " ");
    contt=contt.replace("'s", "");
    contt=contt.replace("/", " ");
    contt=contt.replace("\\", " ");
    contt=re.sub(r'\b[^a-zA-Z]{2,}\b',r' ',contt);
    contt=re.sub(r'\b[^a-zA-Z]{2,}',r' ',contt);
    contt=re.sub(r'[\n\r\t\(\)\.",\?:;!+]+',r' ',contt);
    lst = contt.split(" ")

    a1=len(lst)
    lst=removeWithStoplist(lst,os.path.join(this_dir,"./stoplist1"))
    lst=removeWithStoplist(lst,os.path.join(this_dir,"./stoplist2"))
    lst=convertVerb(lst)
    lst=convertNoun(lst)
    #lst=list(set(lst))
    a2=len(lst)
    #print(a1,a2)
    return lst

def getMainContent(url):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    tmpfile = "./.cache/tmp.txt"
    otestfile = open(tmpfile, 'w')
    otestfile.write("")
    rslt = "ERROR"
    try:
        p1 = subprocess.Popen(["/usr/bin/java","-cp","./gettestset/boilerpipe/create_jar/:./gettestset/boilerpipe/boilerpipe-1.2.0.jar:./gettestset/boilerpipe/lib/*", "Getwebcontent",url], stdout=subprocess.PIPE)
        print "extract main content of ",url[0:50]+"..."
        rslt = p1.stdout.read()
        rsltList = rslt.split("\n")
        rslt = "\n".join([i for i in rsltList if i!=""][1:])
        rslt = "ERROR" if ""==rslt else rslt
    except urllib2.HTTPError:
        print "ERROR",url
    except urllib2.URLError, e:
        print "There was an error: %r" % e
    otestfile.write(rslt)
    return tmpfile

