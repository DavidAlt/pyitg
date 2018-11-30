# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 17:15:29 2018

@author: david alt
"""

# ============================================================================
#  Setup logging
# ============================================================================

import logging
logging.basicConfig(level=logging.CRITICAL,
                    format='%(levelname)-9s: %(name)s : %(funcName)s() : %(message)s')
log = logging.getLogger('itg')
log.setLevel(logging.DEBUG)



# ============================================================================
#  CONSTANTS (enums, flags)
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



# ============================================================================
#  PARSER: extracts info from a template or item strings
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
#  VALIDATOR: validates template or item data
# ============================================================================

