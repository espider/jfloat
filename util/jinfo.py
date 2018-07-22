#!/usr/bin/python
# coding:utf-8

from command import *
from display import *
from colorstyle import *


class JInfo(object):
    __key_point__ = ('java.runtime.version =',
                     'os.name =',
                     'user.name =',
                     'file.encoding =',
                     'java.specification.version =',
                     'java.vm.specification.version =',
                     'sun.arch.data.model =',
                     'sun.java.command =',
                     'java.home =',
                     'java.version =',
                     'java.class.path =',
                     'file.separator =',
                     'sun.cpu.endian =',
                     'VM Flags:',
                     'Non-default VM flags:')

    @staticmethod
    def dump_info(pid=None):
        if pid:
            out = Command.run('jinfo {0}'.format(pid))
            for item in out:
                for point in JInfo.__key_point__:
                    if item.startswith(point):
                        Display.show(
                            '%s%s' % (point, use_style_level(important_level['high2'], item.replace(point, ''))))
                        pass
                pass
                # Display.show(out)
        pass
