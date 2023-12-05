from ply.lex import lex
from logging import getLogger

'''step endstep stepto
   switch case default endswitch 
   welcome speak listen 
   exit call(py脚本调用)
   '''
class Lexer:
    reserved={
        'step':     'STEP',
        'endstep':  'ENDSTEP',
        'stepto':   'STEPTO',
        'switch':   'SWITCH',
        'case':     'CASE',
        'default':  'DEFAULT',
        'endswitch':'ENDSWITCH',
        'welcome':  'WELCOME',
        'speak':    'SPEAK',
        'listen':   'LISTEN',
        'EXIT':     'CALL'
    }

    tokens=['NEWLINE','VAR','STR','INT']+list(reserved.values())

