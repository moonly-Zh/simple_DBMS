import ply.yacc as yacc
import re
import time
import os.path
import glob
import os
from datetime import datetime
from collections import OrderedDict
from Lex import *

'''
grammar:
    statement: SELECT select_statement from_statement where_statement
             | SELECT select_statement where_statement
             | SELECT where_statement

    select_statement: select_statement, NAME
                    | select_statement, SIZE
                    | select_statement, CTIME
                    | select_statement, MTIME
                    | select_statement, ATIME
                    | NAME
                    | SIZE
                    | CTIME
                    | MTIME
                    | ATIME
                    | *

    from_statement: FROM FNAME

    where_statement: WHERE condition_statement

    condition_statement: condition_statement OR and_condition
                       | and_condition

    and_condition: and_condition AND factor
                 | factor

    factor: name_factor
          | size_factor
          | ctime_factor
          | mtime_factor
          | atime_factor

    name_factor: NAME = FNAME
               | NAME LIKE FNAME

    size_factor: SIZE = NUMBER
               | SIZE > NUMBER
               | SIZE < NUMBER
               | SIZE >= NUMBER
               | SIZE <= NUMBER

    ctime_factor: CTIME = DATE
                | CTIME = DATETIME
                | CTIME > DATE
                | CTIME > DATETIME
                | CTIME >= DATE
                | CTIME >= DATETIME
                | CTIME < DATE
                | CTIME <= DATETIME

    mtime_factor: MTIME = DATE
                | MTIME = DATETIME
                | MTIME > DATE
                | MTIME > DATETIME
                | MTIME >= DATE
                | MTIME >= DATETIME
                | MTIME < DATE
                | MTIME <= DATETIME

    Atime_factor: ATIME = DATE
                | ATIME = DATETIME
                | ATIME > DATE
                | ATIME > DATETIME
                | ATIME >= DATE
                | ATIME >= DATETIME
                | ATIME < DATE
                | ATIME <= DATETIME
'''


def execute(s_stmt, f_stmt, w_stmt):
    pass


def travel_file_tree(start_point, accu_funcs, selector, printer):
    pass


def p_statement(p):
    '''
        statement : SELECT select_statement
    '''
    pass


def p_select_stmt(p):
    '''
        select_statement : fields_select_stmt
    '''
    p[0] = p[1]


def p_fields_select_stmt(p):
    '''
        fields_select_stmt : ID
    '''
    print('i get ', p[1])


# def p_from_stmt(p):
#     'from_statement : FROM ID'
#     p[0] = ('from', p[2])


def p_error(p):
    print('parse error, unexpected token:', p)


yacc.yacc()

if __name__ == '__main__':
    yacc.yacc()
    stmt = 'select $name, avg($size) from . where $size > 1'
    yacc.parse(stmt)
