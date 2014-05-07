# -*- coding: utf-8 -*- 
# Author: HW <todatamining@gmail.com>
# See LICENSE.txt for details.
import os
this_dir,this_filename = os.path.split(os.path.abspath(__file__))
WIERDWORDS = [
                "download","restart","ensure",
                "encapsulate","embed","advertise","align","upload","reload",
                "minimise","outsource","resize","reuse","redefine","synchronise","defuse","remold","materialise","destabilize"
             ]
KEY_SPORTS=['league', 'march', 'played', 'season', 'receiver', 'bowl', 'guard', 'player', 'game', 'time', 'defensive', 'night', 'tackle', 'star', 'team']

TRAININGSET_DIR = os.path.join(this_dir,"./trainset/")         #business  entertainment  health  sport
#TRAININGSET_DIR = os.path.join(this_dir,"./trainset_2/")      #sports,nonsports
#TRAININGSET_DIR = os.path.join(this_dir,"./simpletrainset/")   #chinese,tokyo ,in order to verify bayesian
#TRAININGSET_DIR = os.path.join(this_dir,"./simpletrainset2/")  #c,not_c, cat,dog,mouse in order to verify infomation gain
DEBUG_ON = True

class GlobalCanModify(object):
    TERM_SELECTION_RATE  = 0.005 #infomation gain ratio

