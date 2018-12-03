# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 17:17:20 2018

@author: david
"""
import itg
from template_models import AhltaTemplate

raw_blankquotes = r'""'
raw_item = r'1,440,225,585,245,112344,8449,"R1|||||||19|80|YCN|0|0|X|X|0|||0|0|1|1|0||||","F=Arial|Y=6|K=16777215|T=T","Complete  ROS~A complete review of systems was performed and was negative, except as detailed above (minimum 10 systems).~ "'
raw_form_obj = r'0,0,0,1158,2250,0,1048576,"","",""'
raw_item_data = r'"F=Arial|K=16777215|T=T"'
raw_tabstrip_data = r'"L=V=13:DF=1:PS=1:TP=0:MR=T:B S=0:TWS=0:PB=2:NB=3:ROS=1:PL=1:FB=1:EM=1:CB=2:HHL=F"'

dragon = AhltaTemplate('ahlta_template.txt')
#tswf = AhltaTemplate('TSWF-Peds General.txt')

#print(dragon.info())

#x = itg.FLAGS(raw_form_obj)
#y = itg.validate_form_obj(raw_form_obj)

#print(x)
#print(y)