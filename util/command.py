#!/usr/bin/python
# coding:utf-8

import os
import datetime
import shlex
import subprocess as sp

open_file = None


def log_content(content, path=None, writefile=True, newline=True):
    """ write log for command and output """
    if writefile:
        if not path:
            logfile = os.path.join(os.curdir, 'jfloat_{0}.log'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
        else:
            logfile = path
        write_type = 'w'
        if os.path.exists(logfile):
            write_type = 'a'
        else:
            pass
        f = open(logfile, write_type)
        if newline:
            f.write(content + '\n')
        else:
            f.write(content)


class Command(object):
    @staticmethod
    def run(cmd=None, split_char=None):
        """ run command and return iterator """
        if cmd:
            log_content(cmd)
            global open_file
            env = dict(os.environ)
            # print env
            open_file = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.STDOUT, env=env)
            # open_file = sp.Popen(shlex.split(cmd), shell=True, stdout=sp.PIPE, stderr=sp.STDOUT, env=env)
            out, err = open_file.communicate()
            if open_file.returncode != 0:
                print('Popen err:{0}'.format(err))
                return None
            log_content(out)
            if split_char:
                return out.split(split_char)
            else:
                return out.splitlines()
        pass
