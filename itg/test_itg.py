# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 17:17:20 2018

@author: david
"""

from itg import ahlta_template
from itg import item_parser
from itg import ControlFlag

# ===========================================================================+
#  Load the AHLTA template
# ===========================================================================+
template_obj = ahlta_template('ahlta_template.txt')
#template2 = ahlta_template('TSWF-Peds General.txt')
#print(template.info())
#print(template.form_backcolor)
#template.print_by_page(0)
#print(template.parse_page_names())
#print(template.info())


# extract page names

# ============================================================================
#  Template validation
# ============================================================================
def validate_item_options(item):
    def_options = ['K','T','S','W','B','I','F','Z','U','C','N','L','O','P']
    checkbox_options = ['Y']
    frame_options = ['H','T']
    browsetree_options = ['I','B','S']
    grid_options = ['E','O','A','P','R','W']
    ribbon_options = ['G','T','R','Y','B','C','S','H','O']
    tabstrip_options = ['BS','CB','DF','EM','FB','HHL','MR','NB','PB','PL',
                        'PS','ROS','TP','TWS','V']
    medcin_options = ['O']
    list_options = ['G','O']
    valuebox_options = ['V']
    picture_options = ['MR','O']
    
    
    valid_options = True
    
    print(f'Flag: {item_parser.FLAGS(item)}')
    print(f'Controls: {item_parser.parse_flags(item_parser.FLAGS(item))}')
    controls = item_parser.parse_flags(item_parser.FLAGS(item)).split('|')
    
    
    
    
    if ('CHKY' in controls or 'CHKN' in controls):
        print('chck present')
    #if 
    

def validate_form_signature(form_signature):
    # line should contain 1 entry, enclosed in " "
    valid_count = True
    valid_entries = True
    
    form_signature = form_signature.rstrip() # remove newline
    # use list comprehension to split and strip at once
    tokens = [x.strip() for x in form_signature.split(',')]
    if (len(tokens) != 1):
        valid_count = False
        print(f'   Error [Form Signature]:  invalid number of entries ({len(tokens)}); should be 1.')
        
    if (form_signature[0] != r'"' or form_signature[len(form_signature) - 1] != r'"'):
        valid_entries = False
        print(f'   Error [Form Signature]:  \'{form_signature}\' is not enclosed in double quotes (\"...")')
    
    return (valid_count and valid_entries) 
    

def validate_form_identification(form_identification):
    # line should contain 3 or 4 entries, each enclosed in " "
    valid_count = True
    valid_entries = True
    
    # use list comprehension to split and strip at once
    tokens = [x.strip() for x in form_identification.split(',')]
    if (len(tokens) < 3 or
        len(tokens) > 4):
        valid_count = False
        print(f'   Error [Form Identification]:  invalid number of entries ({len(tokens)}); should be 3 or 4.')
        
    for token in tokens:
        if (token[0] != r'"' or token[(len(token)-1)] != r'"'):
            valid_entries = False
            print(f'   Error [Form Identification]:  \'{token}\' is not enclosed in double quotes (\"...")')
    
    return (valid_count and valid_entries) 
    
def validate_form_obj(form_obj):
    valid_form_obj = True
    tokens = [x.strip() for x in form_obj.split(',', maxsplit=9)]

    # Vulnerability: doesn't check for >10 fields b/c too lazy to distinguish DESCRIPTION
    if (len(tokens) < 10):
        valid_form_obj = False
        print(f'   Error [Form Object]: invalid number of fields ({len(tokens)}) (should be 10)')
    
    if int(item_parser.FLAGS(form_obj)) != ControlFlag.FORM:
        valid_form_obj = False
        print('   Error [Form Object]: Incorrect ControlFlag (should be 1048576)')
        
    # ToDo:
    #   PAGE should be 0
    #   LEFT and TOP should be int and 0
    #   RIGHT and BOTTOM should be int and >0
    #   MEDCIN_ID should be 0
    #   PREFIX should be ""
    #   ITEM_DATA should be ""
    #   DESCRIPTION should be ""
        
    return valid_form_obj
    
    
def validate_tabstrip_obj(tabstrip_obj):
    pass
    # ToDo:
    # ControlFlag should be 32
    # PAGE should be last page
    # LEFT, TOP, RIGHT, BOTTOM should be 5,377,295,395 (but I don't know why)
    # MEDCIN_ID should be 0
    # valid PREFIX: 26 entries (even if blank; don't strip whitespace)
    # valid ITEM_DATA: no invalid entries
    # valid DESCRIPTION: page label count == PAGE
    5,5,377,295,395,0,32,
    " |||||||0|0||0|0|||0|||0|0|0|0|0|0|||",
    "L=V=13:DF=1:PS=1:TP=0:MR=T:BS=0:TWS=0:PB=2:NB=3:ROS=1:PL=1:FB=1:EM=1:CB=2:HHL=F",
    ":-2147483633:Provider|%3Development|%2Screening|Procedures|Resources"
    
def validate_browsetree_obj(browsetree_obj):
    pass

def validate_form_item(form_item):
    return len(form_item.split(',', maxsplit=9)) == 10

template = []
with open('ahlta_template.txt', 'r') as f:
    template = f.readlines()

#raw = r'1,440,225,585,245,112344,8449,"R1|||||||19|80|YCN|0|0|X|X|0|||0|0|1|1|0||||","F=Arial|Y=6|K=16777215|T=T","Complete  ROS~A complete review of systems was performed and was negative, except as detailed above (minimum 10 systems).~ "'
#raw2 = r'"one","two","three",  "four"'

print(f'Form Signature:       {validate_form_signature(template[0])}')
print(f'Form Identification:  {validate_form_identification(template[1])}')
print(f'Form Object:          {validate_form_obj(template[2])}')
print(f'Tabstrip Object:      {validate_tabstrip_obj(template[3])}')
print(f'BrowseTree Object:    {validate_browsetree_obj(template[4])}')
print(f'Form Item:            {validate_form_item(template[5])}')
print("")

#validate_item_options(raw)

raw3 = r'""'
raw4 = r'"F=Arial|K=16777215|T=T"'
raw5 = r'"L=V=13:DF=1:PS=1:TP=0:MR=T:BS=0:TWS=0:PB=2:NB=3:ROS=1:PL=1:FB=1:EM=1:CB=2:HHL=F"'

item_parser.parse_options(raw5)