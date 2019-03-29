#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""

File_name:

"""

import os
import sys
import getopt

phpStr="php -f {fileName}"

def main(argv):

    for arg in argv:
        print arg;

    fName=argv[1]
    print fName
    
    cmd=phpStr.format(fileName=fName)
    print cmd;

    os.system(cmd)
    

if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main(sys.argv)
