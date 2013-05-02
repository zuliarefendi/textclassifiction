# -*- coding: utf-8 -*- 
# Author: HW <todatamining@gmail.com>
# See LICENSE.txt for details.
#!/usr/bin/env python
import imp
import os
this_dir,this_filename = os.path.split(os.path.abspath(__file__))

print "------------------",this_dir,this_filename

UT = imp.load_source('utility', os.path.join(this_dir,'../utility.py'))
GV = imp.load_source('globalvariable', os.path.join(this_dir,'../globalvariable.py'))


def mycount():
    flst = UT.getFileInsideDir(os.path.join(this_dir,'./output/'))
    print GV.KEY_SPORTS
    for f in sorted(flst):
        cntlst=[]
        wlst = UT.extractWordList(os.path.join(this_dir,'./output/',f))
        for key in GV.KEY_SPORTS:
            cntlst.append(wlst.count(key))
        print f,cntlst
