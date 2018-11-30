# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 17:15:29 2018

@author: david
"""

# ============================================================================
#  Setup logging
# ============================================================================
import logging
# setup the root logger
logging.basicConfig(level=logging.CRITICAL,
                    format='%(levelname)-9s: %(name)s : %(funcName)s() : %(message)s')

log = logging.getLogger('itg')
log.setLevel(logging.DEBUG)


# ============================================================================
#  AHLTA item parsing
# ============================================================================

class item_parser:     

    # Simple parse (no subparsing)
    def PAGE(line): 
        tokens = line.rstrip().split(',', maxsplit=9)
        return int(tokens[0])

    def LEFT(line):
        tokens = line.rstrip().split(',', maxsplit=9)
        return int(tokens[1])

    def TOP(line):
        tokens = line.rstrip().split(',', maxsplit=9)
        return int(tokens[2])

    def RIGHT(line):
        tokens = line.rstrip().split(',', maxsplit=9)
        return int(tokens[3])

    def BOTTOM(line):
        tokens = line.rstrip().split(',', maxsplit=9)
        return int(tokens[4])

    def MEDCIN_ID(line):
        tokens = line.rstrip().split(',', maxsplit=9)
        return int(tokens[5])

    def FLAGS(line):
        tokens = line.rstrip().split(',', maxsplit=9)
        return int(tokens[6])

    # use with the Prefix enum for inner components
    def PREFIX(line):
        tokens = line.rstrip().split(',', maxsplit=9)
        return tokens[7]

    def ITEM_DATA(line):
        tokens = line.rstrip().split(',', maxsplit=9)
        return tokens[8]

    def DESCRIPTION(line):
        tokens = line.rstrip().split(',', maxsplit=9)
        return tokens[9]
    
    
    # Simple parse (no subparsing)
    def simple_parse(item):
        item = item.rstrip()
        tokens = item.split(',', maxsplit=9)
        return tokens
    
    
    # Detailed parse (subparsing of prefix etc)
    #   Only use for "typical" items
    #   Description may cause problems if doesn't have ~
    def detailed_parse(item):
        item = item.rstrip()
        tokens = item.split(',', maxsplit=9)
        prefix = tokens[7].replace('"','').split('|')
        itemdata = tokens[8]
        description = tokens[9].replace('"','').split('~')
        result = tokens[0:7]
        result += prefix
        result.append(itemdata)
        result += description
        return result


    # ToDo:
    #   function to generate flag (int) from controls (list)
    #   this really only works in a visual/gui sense

    def parse_flags(flags):
        if flags == 1:
            result = 'LINE'
        elif flags == 2:
            result = 'BOX'
        else:
            result = str(ControlFlag(flags)).replace('ControlFlag.','')
        return result

    
    def parse_options(item_data):
        log.warning('Does not parse L=V= properly')
        # ToDo:
        #   if empty, break
        #   elif invalid delimiters, break
        #   elif |, parse
        #   elif :, parse and check for L=V
        
        options = {}
        if item_data != r'""':
            
            if ':' in item_data:
                tokens = [x.strip('"') for x in item_data.split(':')]
            
            elif '|' in item_data:
                tokens = [x.strip('"') for x in item_data.split('|')]
                
            else:
                log.error('No valid delimiters ( | or : )')
            
            for token in tokens: 
                key = re.search('(.*?)(?==)', token).group(1)
                value = re.search('(?<==)(.*)', token).group(1)
                log.info(key + ' :: ' + value)
                options[key] = value            
            
            log.info(f'Tokens: {tokens}')
            log.info(f'Dictionary: {options}')
        
        else: 
            log.error('String didn\'t contain any options.')

        return options
# ============================================================================
#  AHLTA template
# ============================================================================


#from ahlta_item import item_parser as parse
#from itg_utils import control_flag
import re
class ahlta_template:
    
    # Constructor
    def __init__(self, fhand):
        self.header = []
        self.pages = {}
        
        with open(fhand, 'r') as f:
            self.template = f.readlines()
        
        self._import_template()
        self._parse_header()

        
    # Private Methods
    def _import_template(self):
        # Store items by page in a dictionary, using page numbers as keys
        line_num = 1
        for line in self.template:
            if line_num <= 5: # first five lines belong to the header
                self.header.append(line) 
            else:
                #line = line.rstrip() # strip any newline characters
                tokens = line.split(',', maxsplit=9) # split into tokens
                key = int(tokens[0]) # use the first token as the key
                if key not in self.pages:
                    self.pages[key] = [] # add that key with an empty (unnamed) list
                self.pages[key].append(line) # otherwise add the line to an existing list
            line_num += 1

            
    def _parse_header(self):
        # Extract template-level information
        self.form_signature = self.header[0].rstrip() #version of medcin form designer software
        self.form_name = self.header[1].split(',', maxsplit=9)[0]
        self.form_owner = self.header[1].split(',', maxsplit=9)[1]
        self.form_group = self.header[1].rstrip().split(',', maxsplit=9)[2]
        self.form_sid = 'none'
        if len(self.header[1].split(',', maxsplit=9)) == 4:
            self.form_sid = self.header[1].rstrip().split(',', maxsplit=9)[3]
        
        # get page names and count
        self.page_names = self._parse_page_names()
        #self.page_count = len(self.visible_page_names)
        self.page_count = len(self.pages)
        
        # Setup important header pieces
        self.form_obj = self.header[2]
        self.tabstrip = self.header[3]
        self.browsetree = self.header[4]
        
        # ensure we've got the Form line (3rd line of header) before getting width, height
        if int(item_parser.FLAGS(self.form_obj)) == ControlFlag.FORM:
            
            self.form_width = item_parser.RIGHT(self.form_obj)
            self.form_height = item_parser.BOTTOM(self.form_obj)
            
        else:
            print('ERROR: Incorrect flag on line 3 of header (should be 1048576')
            print(f'Line 3 of header:  {self.form_obj}')
            
        # ensure we've got the TabStrip obj
        if int(item_parser.FLAGS(self.tabstrip)) == ControlFlag.TABSTRIP:
            form_backcolor_search = re.search('(?<=:)(.*?)(?=:)', item_parser.DESCRIPTION(self.tabstrip))
            if form_backcolor_search:
                self.form_backcolor = form_backcolor_search.group(1)
                
            #self.form_border_style -BS
            #self.form_default_checkbox_style -CB
            #self.details_frame -DF
            #self.form_em_button -EM
            #self.form_flowsheet_button -FB
            #self.form_multirow -MR
            #self.form_negative_buttons -NB
            #self.form_positive_buttons -PB
            #self.form_picklist_button -PL
            #self.form_page_style -PS
            #self.form_ros_button -ROS
            #self.form_tabstrip_button_placement -TP
            #self.form_tabstrip_tab_width -TWS
            #self.form_version -V
            # often you see L=V= ... unclear why or if necessary
        else:
            print('ERROR: Incorrect flag on line 4 of header (should be 32)')
            print(f'Line 4 of header:  {self.tabstrip}')

    def _parse_page_names(self):
        # Page names need to be cleaned of prefixes and suffixes:
        #   :numbers: for page 1 indicates back color of the form
        #   # (no_browsing), < (left_lateral), > (right_lateral)
        #   %int denotes number of columns on the page
        #   ~int as a suffix denotes a narrative chapter assignment
        raw = item_parser.DESCRIPTION(self.header[3])
        
        tokens = raw.strip('\"').split('|')
        clean_tokens = []
        clean_tokens.append('<universal>')
        
        page_one = re.sub(r'\%\d','',tokens[0].split(':')[len(tokens[0].split(':')) - 1])
        clean_tokens.append(page_one)
        
        for page in range(len(tokens)):
            if page == 0:
                continue
            else:
                cleaned_page = re.sub(r'\%\d','',tokens[page])
            clean_tokens.append(cleaned_page)
        
        return clean_tokens
 
    def _parse_form_properties(self):
        pass
    # IMPORT VALIDATION: 
    #   header lines are in the expected place
    #   form_sid is accounted for
    #   specified page count matches number of page names (for visible pages, 
    #       ignoring page 0)
    #   Form object is the third item, and has a width and height
    #   TabStrip object is appropriate
    #   BrowseTree object is appropriate
    def _validate_header(self):
        pass
    
    
    
    # Public Methods
    def info(self):
        page_info = f'Pages ({self.page_count}):\n'
        for page, item_list in sorted(self.pages.items()):
            page_label = str(page) + f' [{self.page_names[page]}]'
            page_info += f'  {page_label}:  {len(item_list)} items\n'
            
        return(f'Template: {self.form_name}\n' +
               f'Owner: {self.form_owner}\n' +
               f'Group: {self.form_group}\n' +
               f'Software: {self.form_signature}\n' +
               f'Security ID: {self.form_sid}\n\n' +
               f'Width: {self.form_width} pixels\n' +
               f'Height: {self.form_height} pixels\n\n' +
               page_info +
               f'Total (including header): {len(self.template)} items'
               )
    
    def print_info(self):
        print(self.info())
        
    def print_header(self):
        for line in self.header:
            print(line)
            
    def print_by_page(self, page):
        print(f'Page: {page} ({(len(self.pages[page]))} items)')
        for line in self.pages[page]:
            print(line.rstrip())
        




# ===========================================================================+
#  XML-related functions
#      TODO: MOVE INTO ITEM_PARSER OR MAKE ITS OWN CLASS
# ===========================================================================+
import xml.etree.ElementTree as ET
#from ahlta_template import ahlta_template
#from ahlta_item import item_parser as ip

# Takes a parsed item (from parse_template_item) and returns an xml node
#   This WILL break if used for items without every property 
#   e.g., "" for prefix or description without a tilde
def detailed_parsed_item_to_xml(parsed_item, name='item'):
    subelements = [
        'page',
        'left', 'top', 'right', 'bottom',
        'medcin_id', 'flags', 
        'prefix', 'modifier', 'result',
        'status', 'value', 'link_group',
        'units', 'box_offset', 'inline_textbox_width',
        'component_sequence', 'index_to_reference_list',
        'narrative_group_assignment', 
        'chky_caption', 'chkn_caption', 'bit_flags',
        'limit_max', 'limit_min', 'ribbon_trigger_id',
        'cluster_id', 'parent_ribbon_id', 'radio_button_group',
        'image_id', 'hotspot_set_id', 'parent_frame',
        'code_mapping', 'user_assigned_subgroup',
        'item_data', 'caption', 'content'
    ]
    
    item_node = ET.Element(name)
    
    for i in range(len(subelements)):
        sub_el = ET.SubElement(item_node, subelements[i])
        sub_el.text = parsed_item[i]
    
    return item_node


def simple_parsed_item_to_xml(item, name):
    subelements = [
            'page',
            'left', 'top', 'right', 'bottom',
            'medcin_id', 'flags', 
            'prefix', 'item_data', 'description'
            ]
    
    item_node = ET.Element(name)
    
    for i in range(len(subelements)):
        sub_el = ET.SubElement(item_node, subelements[i])
        sub_el.text = item[i]
    
    return item_node   


def unparsed_item_to_xml(item, name):
    parsed = item.rstrip().split(',', maxsplit=9) # simple parse
    return simple_parsed_item_to_xml(parsed, name)     


def convert_template_to_xml(template):
    # TODO: Do we need to write xml version/encoding info first?
    
    template_xml = ET.Element('template')
    header = ET.SubElement(template_xml, 'header')
    
    for i in range(template.page_count+1): # +1 b/c page_count ignores page_0
        # setup the node for the page
        node_name = 'page_' + str(i)
        page_node = ET.SubElement(template_xml, node_name)
        
        for item in template.pages[i]:
            ctrl_flag = str(item_parser.FLAGS(item))
            item_node = unparsed_item_to_xml(item, ctrl_flag)
            page_node.append(item_node)
    
    # Use template name as filename
    f_out = template.form_name.strip('"') + '.xml'
    
    # Write to file with xml declaration
    ET.ElementTree(template_xml).write(f_out, encoding='utf-8', xml_declaration=True) 


#convert_template_to_xml(template)



# ============================================================================
#  ENUMS: Prefix and ControlFlag
# ============================================================================
from enum import Enum, IntFlag

class Prefix(Enum):
    # "0|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25"
    PREFIX = 0
    MODIFIER = 1
    RESULT = 2
    STATUS = 3
    VALUE = 4
    LINK_GROUP = 5
    UNITS = 6
    BOX_OFFSET = 7
    INLINE_TEXTBOX_WIDTH = 8
    COMPONENT_SEQUENCE = 9
    INDEX_TO_REFERENCE_LIST = 10
    NARRATIVE_GROUP_ASSIGNMENT = 11
    CHKY_CAPTION = 12
    CHKN_CAPTION = 13
    BIT_FLAGS = 14
    LIMIT_MAX = 15
    LIMIT_MIN = 16
    RIBBON_TRIGGER_ID = 17
    CLUSTER_ID = 18
    PARENT_RIBBON_ID = 19
    RADIO_BUTTON_GROUP = 20
    IMAGE_ID = 21
    HOTSPOT_SET_ID = 22
    PARENT_FRAME = 23
    CODE_MAPPING = 24
    USER_ASSIGNED_SUBGROUP = 25

class ControlFlag(IntFlag):
    NONE = 0
    #LINE = 1 # maybe this should just be removed ...
    #BOX = 2 # Frame object; maybe this should just be removed ...
    LEFT = 1  # left alignment, where applicable
    RIGHT = 2 # right alignment, where applicable
    TREE = 4 # Data entry tree
    GRID = 8 # Grid object
    RIBBON = 16 # Ribbon object
    TABSTRIP = 32 # Page control (tab strip)
    PICTURE = 64 # picture object
    REQ = 128 # Medcin entry is required
    CHKY = 256 # Medcin yes checkbox component
    CHKN = 512 # Medcin no checkbox component
    ROS = 1024 # Medcin ROS state
    VALUE = 2048 # Medcin textbox to enter value
    BROWSE = 4096 # Medcin button to browse children findings
    NOTE = 8192 # Medcin Note button to popup note box for Medcinid > 0.
    """
    When the flag value is identical to fc_Note and the Medcinid is 0, the record either: 
    (Page=0) the pre-defined chapter headings in the description and itemdata properties 
            (substrings are delimited with a tilde character), or 
    (Page=1) the pre-defined Encounter-specific User SubGroup headings in the description 
             and itemdata properties (substrings are Tab delimited)
    """
    LINK = 16384 # button to link to another form
    LABEL = 32768 # label for captions
    UPDOWN = 65536 # Medcin UpDown button
    HASDATA = 131072 # Logic display indicator
    REFERENCE = 262144 # reference document, or finding reference button
    ONSET = 524288 # Medcin Onset combo
    FORM = 1048576 # form size
    SEARCH = 2097152 # Word search toolbar
    ACTION = 2097152 # Action component
    TEXTBOX = 4194304 # Medcin free-text entry box
    DROPBOX = 8388608 # Medcin Picklist ' dropdown listbox
    LISTBOX = 16777216 # Medcin Picklist Full listbox
    LISTVIEW = 20971520 # Medcin Picklist ' multi-column listview
    INLINENOTE = 33554432 # Medcin inline textbox
    RICHTEXTBX = 37748736 # Medcin rich textbox
    PICKLIST = 134217728 # Picklist
    ROSTGL = 268435456 # Medcin ROS toggle button
    WINDOW = 536870912 # Window
    TIMING = 1073741824 # Timing Button component