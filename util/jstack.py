#!/usr/bin/python
# coding:utf-8

import re
import datetime
from command import *
from display import *
from colorstyle import *


class JStack(object):
    """ find the threads that make high CPU. """
    __max_high_count__ = 8
    __threshold_cpu__ = 50
    __re_top_title__ = re.compile(ur'PID(\s+)USER')
    __re_stack_id__ = re.compile(ur'tid=([0-9a-z]+)(\s+)nid=([0-9a-z]+)(\s+)')
    __thread_info__ = {}

    @staticmethod
    def dump_stack(pid=None):
        """ call stack of all thread by pid """
        if pid:
            cmd_thread_stack = 'jstack -l %d' % pid
            out_threads_stack = Command.run(cmd_thread_stack, split_char='\n\n')
            return out_threads_stack

    @staticmethod
    def find_high_cpu(pid=None):
        """ find the threads that make high CPU """
        if pid:
            JStack.get_thread_cpu(pid)

            JStack.get_thread_stack(pid)

    @staticmethod
    def get_thread_cpu(pid):
        """ get top thread ids that high CPU """
        JStack.__thread_info__ = {}
        cmd_find_top_thread = 'top -b -Hp %d -n 1' % pid
        out_threads = Command.run(cmd_find_top_thread)
        loop_count = 0
        for thread_line in out_threads:
            if JStack.__re_top_title__.search(thread_line):
                loop_count += 1
                array_col = thread_line.split()
                index_pid = None
                index_cpu = None
                for i in range(len(array_col)):
                    if array_col[i] == 'PID':
                        index_pid = i
                    elif array_col[i] == '%CPU':
                        index_cpu = i
                continue
            if 0 < loop_count <= JStack.__max_high_count__:
                loop_count += 1
                array_val = thread_line.split()
                if len(array_val) > index_pid and len(array_val) > index_cpu:
                    if float(array_val[index_cpu]) > JStack.__threshold_cpu__:
                        JStack.__thread_info__[int(array_val[index_pid])] = (
                            hex(int(array_val[index_pid])), float(array_val[index_cpu]))
        # print Jstack.__thread_info__
        pass

    @staticmethod
    def get_thread_stack(pid):
        """ get thread call back by nid """
        nid_list = {}
        last_nid = None
        out_threads_stack = JStack.dump_stack(pid)
        for thread_stack in out_threads_stack:
            id_group = JStack.__re_stack_id__.search(thread_stack)
            if id_group:
                last_nid = id_group.group(3)
                nid_list[last_nid] = [thread_stack]
            else:
                if last_nid:
                    nid_list[last_nid].append(thread_stack)

        for k, v in sorted(JStack.__thread_info__.items(), key=lambda d: d[1][1], reverse=True):
            if v[0] in nid_list:
                Display.show('-' * 50)
                Display.show('nid:[{0}] CPU:[{1}%]'.format(
                    use_style_level(important_level['high2'], v[0]),
                    use_style_level(important_level['high2'], str(v[1]))))
                Display.show('\n'.join(nid_list[v[0]]))
        pass
