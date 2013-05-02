# -*- coding: utf-8 -*- 
# Author: HW <todatamining@gmail.com>
# See LICENSE.txt for details.
#!/usr/bin/env python
import urllib2
import os
import sys
import os.path,subprocess

def getMainContent(url):
    rslt = "ERROR"
    try:
        p1 = subprocess.Popen(["/usr/bin/java","-cp","./boilerpipe/create_jar/:./boilerpipe/boilerpipe-1.2.0.jar:./boilerpipe/lib/*", "Getwebcontent",url], stdout=subprocess.PIPE)
        print "getting ",url[0:50]
        rslt = p1.stdout.read()
        rsltList = rslt.split("\n")
        rslt = "\n".join([i for i in rsltList if i!=""][1:])
        rslt = "ERROR" if ""==rslt else rslt
    except urllib2.HTTPError:
        print "ERROR",url
    except urllib2.URLError, e:
        print "There was an error: %r" % e
    return rslt

inf = open('./urls.txt','r')
otestfile = open("../tobeevaluated.txt", 'w')
cnt = 0
kind=""

if not os.path.exists("./output"):
    os.makedirs("./output")

for url in inf:
    if url[0] == '@':
        continue
    if url[0] == '#':
        kind=(url.strip())[1:]
        continue
    content = getMainContent(url)
    if "ERROR" != content:
        cnt+=1
        filename = '{0}'.format(cnt).zfill(4)
        filename = "./output/{0}_{1}.html".format(filename,kind)
        outf = open(filename, 'w')
        outf.write(content)
        otestfile.write("{0} {1}/{2}\n".format(kind,os.getcwd(),filename))
    else:
        print("ERROR OCCUR for {0}".format(url))
print("{0} file retrieved.".format(cnt))

