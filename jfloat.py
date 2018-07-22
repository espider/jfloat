#!/usr/bin/python
# coding:utf-8

# help for check jvm
# Copyright (c) 2018, chengliang
# All rights reserved.

import os
import sys
import logging
import datetime
import argparse

from util.display import Display
from util.command import Command
from util.jinfo import JInfo
from util.colorstyle import *
from util.jstack import JStack
from util.jmemory import JMemory

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig()
logger = logging.getLogger('jfloat')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
file_handler = logging.FileHandler(filename='./jfloat_{0}.txt'.format(datetime.datetime.now().strftime('%Y-%m-%d')),
                                   encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def main():
    """ main func """
    Display.show('welcome jfloat.')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pid', dest='pid', action='store', required=True,
                        help='PID for java process', type=int)
    parser.add_argument('-i', '--info', dest='info', action='store_true', required=False,
                        help='dump base info for java process')
    parser.add_argument('-s', '--stack', dest='stack', action='store_true', required=False,
                        help='find which threads that make high CPU')
    parser.add_argument('-m', '--map', dest='map', action='store_true', required=False,
                        help='dump the heap info for JVM ')
    parser.add_argument('-g', '--gcstat', dest='gcstat', action='store', required=False,
                        help='get statistics of the garbage collected heap', type=int)
    parser.add_argument('-o', '--object', dest='object', action='store', required=False,
                        help='get object count change by seconds', type=int)

    args = parser.parse_args()

    if args.pid:
        Display.show('pid %s' % use_style_level(important_level['high2'], args.pid))
    else:
        Display.show('need pid')

    # show base info java process
    if args.info:
        print 'args.info'
        JInfo.dump_info(args.pid)

    # find the threads that make high CPU
    if args.stack:
        print 'args.stack'
        JStack.find_high_cpu(args.pid)

    # dump the heap info for JVM
    if args.map:
        print 'args.map'
        JMemory.get_heap_info(args.pid)

    # get statistics of the garbage collected heap
    if args.gcstat:
        print 'args.gcstat%s' % args.gcstat
        JMemory.get_gc_stat(args.pid, args.gcstat)

    if args.object:
        print 'args.object%s' % args.object
        JMemory.get_object_stat(pid=args.pid, sleep_time=args.object)
    pass


if __name__ == "__main__":
    main()
