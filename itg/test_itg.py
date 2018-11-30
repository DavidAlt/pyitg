# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 17:17:20 2018

@author: david
"""

import itg
from template_models import AhltaTemplate


# ===========================================================================+
#  Load the AHLTA template
# ===========================================================================+
template_obj = AhltaTemplate('ahlta_template.txt')
#template2 = ahlta_template('TSWF-Peds General.txt')
#print(template.info())
#print(template.form_backcolor)
#template.print_by_page(0)
#print(template.parse_page_names())
#print(template.info())


# extract page names



template = []
with open('ahlta_template.txt', 'r') as f:
    template = f.readlines()

#raw = r'1,440,225,585,245,112344,8449,"R1|||||||19|80|YCN|0|0|X|X|0|||0|0|1|1|0||||","F=Arial|Y=6|K=16777215|T=T","Complete  ROS~A complete review of systems was performed and was negative, except as detailed above (minimum 10 systems).~ "'
#raw2 = r'"one","two","three",  "four"'

print(f'Form Signature:       {itg.Validator.validate_form_signature(template[0])}')
print(f'Form Identification:  {itg.Validator.validate_form_identification(template[1])}')
print(f'Form Object:          {itg.Validator.validate_form_obj(template[2])}')
print(f'Tabstrip Object:      {itg.Validator.validate_tabstrip_obj(template[3])}')
print(f'BrowseTree Object:    {itg.Validator.validate_browsetree_obj(template[4])}')
print(f'Form Item:            {itg.Validator.validate_form_item(template[5])}')
print("")

#validate_item_options(raw)

raw3 = r'""'
raw4 = r'"F=Arial|K=16777215|T=T"'
raw5 = r'"L=V=13:DF=1:PS=1:TP=0:MR=T:BS=0:TWS=0:PB=2:NB=3:ROS=1:PL=1:FB=1:EM=1:CB=2:HHL=F"'

itg.Parser.parse_options(raw5)