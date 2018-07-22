#!/usr/bin/python
# coding:utf-8


class Display(object):
    @staticmethod
    def show(message=None, new_line=True):
        """print function 
        message: message to print
        new_line: print with newline,True by default
        """
        if new_line:
            print message
        else:
            print message,
        pass
