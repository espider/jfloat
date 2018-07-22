#!/usr/bin/python
# coding:utf-8

import re
import time
import datetime
from decimal import Decimal
from command import *
from display import *
from colorstyle import *


class JMemory(object):
    """ """
    __heap_config__ = {}
    __gc_stat__ = {}
    # EC:Current eden space capacity (KB)
    # EP:Eden space utilization percent
    # SC0/1:Current survivor space 0 or 1 max capacity (KB)
    # SP0/1:Current survivor space 0 or 1 utilization percent
    # OC:Current old space capacity (KB)
    # OP:Old space utilization percent
    # MC:Current meta space capacity (KB)
    # MP:Meta space utilization percent
    # YGC:Young generation GC events increment
    # FGC:Full GC events increment
    # Y/FT:Young or full GC collection time
    __gc_stat_head__ = ['EC', 'EP', 'SC0/1', 'SP0/1', 'OC', 'OP', 'MC', 'MP', 'YGC', 'FGC', 'GCT']
    pass

    @staticmethod
    def get_heap_info(pid=None):
        if pid:
            cmd_heap_info = 'jmap -heap %d' % pid
            out_heap_info = Command.run(cmd_heap_info)
            for line in out_heap_info:
                item = line.split()
                if len(item) > 0:
                    if 'MinHeapFreeRatio' == item[0]:
                        JMemory.__heap_config__['MinHeapFreeRatio'] = int(item[2])
                        pass
                    elif 'MaxHeapFreeRatio' == item[0]:
                        JMemory.__heap_config__['MaxHeapFreeRatio'] = int(item[2])
                        pass
                    elif 'MaxHeapSize' == item[0]:
                        JMemory.__heap_config__['MaxHeapSize'] = int(item[2])
                        pass
                    elif 'NewSize' == item[0]:
                        JMemory.__heap_config__['NewSize'] = int(item[2])
                        pass
                    elif 'MaxNewSize' == item[0]:
                        JMemory.__heap_config__['MaxNewSize'] = int(item[2])
                        pass
                    elif 'OldSize' == item[0]:
                        JMemory.__heap_config__['OldSize'] = int(item[2])
                        pass
                    elif 'NewRatio' == item[0]:
                        JMemory.__heap_config__['NewRatio'] = int(item[2])
                        pass
                    elif 'SurvivorRatio' == item[0]:
                        JMemory.__heap_config__['SurvivorRatio'] = int(item[2])
                        pass
                    elif 'MetaspaceSize' == item[0]:
                        JMemory.__heap_config__['MetaspaceSize'] = int(item[2])
                        pass
                    elif 'CompressedClassSpaceSize' == item[0]:
                        JMemory.__heap_config__['CompressedClassSpaceSize'] = int(item[2])
                        pass
                    elif 'MaxMetaspaceSize' == item[0]:
                        JMemory.__heap_config__['MaxMetaspaceSize'] = int(item[2])
                        pass
                    elif 'G1HeapRegionSize' == item[0]:
                        JMemory.__heap_config__['G1HeapRegionSize'] = int(item[2])
                        pass
                    elif 'PermSize' == item[0]:
                        JMemory.__heap_config__['PermSize'] = int(item[2])
                        pass
                    elif 'MaxPermSize' == item[0]:
                        JMemory.__heap_config__['MaxPermSize'] = int(item[2])
                        pass
                    else:
                        pass
            # print
            Display.show('-' * 50)
            Display.show('JVM Config Info')
            JMemory.show_heap_info_by_dic('NewSize', ischange=True)
            JMemory.show_heap_info_by_dic('NewRatio')
            JMemory.show_heap_info_by_dic('SurvivorRatio')
            JMemory.show_heap_info_by_dic('OldSize', ischange=True)
            JMemory.show_heap_info_by_dic('MinHeapFreeRatio')
            JMemory.show_heap_info_by_dic('MaxHeapFreeRatio')
            JMemory.show_heap_info_by_dic('MaxHeapSize', ischange=True)
            JMemory.show_heap_info_by_dic('MetaspaceSize', ischange=True)
            JMemory.show_heap_info_by_dic('PermSize')
        pass

    @staticmethod
    def show_heap_info_by_dic(name, ischange=False):
        if name in JMemory.__heap_config__:
            if ischange:
                Display.show('%s: %s' % (name, JMemory.get_max_byte_string(JMemory.__heap_config__[name])))
            else:
                Display.show('%s: %s' % (name, JMemory.__heap_config__[name]))
        pass

    @staticmethod
    def get_max_byte_string(byte_int, round_count=2):
        """ return human readable by bytes """
        if byte_int >= 1024:
            k_byte = byte_int * 1.0 / 1024
            if k_byte >= 1024:
                m_byte = k_byte / 1024
                if m_byte >= 1024:
                    g_byte = m_byte / 1024
                    return '%sG' % round(g_byte, round_count)
                return '%sM' % round(m_byte, round_count)
            return '%sK' % round(k_byte, round_count)
        else:
            return '%db' % byte_int
        pass

    @staticmethod
    def get_gc_stat(pid=None, count=10):
        if pid and 0 < count < 1000:
            cmd_gc_stat = 'jstat -gc %d 1000 %d' % (pid, count)
            out_heap_stat = Command.run(cmd_gc_stat)
            line_num = 0
            dic_name_index = {}
            for line in out_heap_stat:
                value_index = 0
                item = line.split()
                for value in item:
                    # print '---' + line
                    if line_num == 0:
                        if value not in JMemory.__gc_stat__:
                            JMemory.__gc_stat__[value] = {}
                        if value_index not in dic_name_index:
                            dic_name_index[value_index] = value
                        pass
                    else:
                        key_name = dic_name_index[value_index]
                        JMemory.__gc_stat__[key_name][line_num] = float(value)
                        """
                        if key_name in ['']:
                            JMemory.__gc_stat__[key_name][line_num] = Decimal(value)
                            pass
                        else:
                            JMemory.__gc_stat__[key_name][line_num] = value
                            pass
                        """
                        pass
                    value_index += 1
                line_num += 1
            # print JMemory.__gc_stat__
            if len(JMemory.__gc_stat__) > 0:
                for i in range(0, line_num):
                    line_temp = []
                    for item in JMemory.__gc_stat_head__:
                        if i == 0:
                            line_temp.append('{:>6}'.format(item))
                            # Display.show('')
                        elif i > 0:
                            if item in ['EC', 'OC', 'MC']:
                                line_temp.append('{:>6}'.format(
                                    JMemory.get_max_byte_string(JMemory.__gc_stat__[item][i] * 1024, 1)
                                ))
                            elif item == 'SC0/1':
                                if JMemory.__gc_stat__['S0U'][i] > 0:
                                    line_temp.append('{:>6}'.format(
                                        JMemory.get_max_byte_string(JMemory.__gc_stat__['S0C'][i] * 1024, 1)))
                                elif JMemory.__gc_stat__['S1U'][i] > 0:
                                    line_temp.append('{:>6}'.format(
                                        JMemory.get_max_byte_string(JMemory.__gc_stat__['S1C'][i] * 1024, 1)))
                                else:
                                    if JMemory.__gc_stat__['S0C'][i] > JMemory.__gc_stat__['S1C'][i]:
                                        line_temp.append('{:>6}'.format(
                                            JMemory.get_max_byte_string(JMemory.__gc_stat__['S0C'][i] * 1024, 1)))
                                    else:
                                        line_temp.append('{:>6}'.format(
                                            JMemory.get_max_byte_string(JMemory.__gc_stat__['S1C'][i] * 1024, 1)))
                            elif item == 'SP0/1':
                                if JMemory.__gc_stat__['S0U'][i] > 0:
                                    line_temp.append('{:>5}%'.format(JMemory.get_percent('S0U', 'S0C', i, 1)))
                                elif JMemory.__gc_stat__['S1U'][i] > 0:
                                    line_temp.append('{:>5}%'.format(JMemory.get_percent('S1U', 'S1C', i, 1)))
                                else:
                                    line_temp.append('{:>5}%'.format('0'))
                            elif item == 'EP':
                                line_temp.append('{:>5}%'.format(JMemory.get_percent('EU', 'EC', i, 1)))
                            elif item == 'OP':
                                line_temp.append('{:>5}%'.format(JMemory.get_percent('OU', 'OC', i, 1)))
                            elif item == 'MP':
                                line_temp.append('{:>5}%'.format(JMemory.get_percent('MU', 'MC', i, 1)))
                            elif item in ['YGC', 'FGC']:
                                if i == 1:
                                    line_temp.append('{:>6}'.format('-'))
                                else:
                                    current = JMemory.__gc_stat__[item][i]
                                    last = JMemory.__gc_stat__[item][i - 1]
                                    if (current - last) > 0:
                                        line_temp.append('{:>6}'.format('+' + str(int(current - last))))
                                    else:
                                        line_temp.append('{:>6}'.format('-'))
                            elif item == 'GCT':
                                if i == 1:
                                    line_temp.append('{:>6}'.format('-'))
                                else:
                                    current = JMemory.__gc_stat__[item][i]
                                    last = JMemory.__gc_stat__[item][i - 1]
                                    if (current - last) > 0:
                                        line_temp.append('{:>4}ms'.format(int((current - last) * 1000)))
                                    else:
                                        line_temp.append('{:>6}'.format('-'))
                                pass
                            else:
                                line_temp.append('{:>6}'.format(' '))
                            pass
                    Display.show('  '.join(line_temp))
                    if i == 0:
                        Display.show('  '.join(['------' for _ in range(0, 11)]))

        pass

    @staticmethod
    def get_percent(numerator_key, denominator_key, i, round_count=2):
        return_str = ''
        if i > 0 and numerator_key in JMemory.__gc_stat__ and denominator_key in JMemory.__gc_stat__ and \
                        i in JMemory.__gc_stat__[numerator_key] and i in JMemory.__gc_stat__[denominator_key]:
            if JMemory.__gc_stat__[denominator_key][i] > 0:
                return_str = str(
                    round(JMemory.__gc_stat__[numerator_key][i] * 100.0 / JMemory.__gc_stat__[denominator_key][i],
                          round_count))
            pass
        return return_str

    @staticmethod
    def get_object_stat(pid=None, is_live=False, sleep_time=10):
        if pid and 3600 > sleep_time > 0:
            dic_start = JMemory.get_object_jmap(pid, is_live)
            # print sleep_time
            # print datetime.datetime.now()
            time.sleep(sleep_time)
            # print datetime.datetime.now()
            dic_end = JMemory.get_object_jmap(pid, is_live)

            total_change = dic_end['total'] - dic_start['total']
            Display.show('total increase object count :%d' % total_change)
            Display.show('-' * 50)
            # increase too fast objects top 10
            # class|+-increase count|current count
            dic_increase_key = {}
            for k, v in dic_end['detail'].items():
                if k in dic_start['detail']:
                    dic_increase_key[k] = v - dic_start['detail'][k]
                    dic_start['detail'].pop(k)
                else:
                    dic_increase_key[k] = v
            for k, v in dic_start['detail'].items():
                if k not in dic_increase_key:
                    dic_increase_key[k] = -v

            increase_10 = JMemory.sort_dic_value_top(dic_increase_key, top=10, reverse=True, min_value=0)
            if len(increase_10) > 0:
                Display.show('increase top 10 object:')
                head_increase = []
                head_increase.append('{:>9}'.format('+count'))
                head_increase.append('{:>9}'.format('current'))
                head_increase.append('class')

                Display.show('  '.join(head_increase))
                Display.show('  '.join(['-' * 9 for _ in range(0, 3)]))
                for item in increase_10:
                    line_list = []
                    line_list.append('{:>9}'.format(item[1]))
                    line_list.append('{:>9}'.format(dic_end['detail'][item[0]]))
                    line_list.append(str(item[0]))
                    Display.show('  '.join(line_list))
                Display.show('-' * 50)

            decrease_10 = JMemory.sort_dic_value_top(dic_increase_key, top=10, max_value=0)
            if len(decrease_10) > 0:
                Display.show('decrease top 10 object:')
                head_decrease = []
                head_decrease.append('{:>9}'.format('-count'))
                head_decrease.append('{:>9}'.format('current'))
                head_decrease.append('class')

                Display.show('  '.join(head_decrease))
                Display.show('  '.join(['-' * 9 for _ in range(0, 3)]))
                for item in decrease_10:
                    line_list = []
                    line_list.append('{:>9}'.format(item[1]))
                    if item[0] in dic_end['detail']:
                        line_list.append('{:>9}'.format(dic_end['detail'][item[0]]))
                    else:
                        line_list.append('{:>9}'.format('0'))
                    line_list.append(str(item[0]))
                    Display.show('  '.join(line_list))
                Display.show('-' * 50)

            pass
            # max count object top 10
            # class|current count
        pass

    @staticmethod
    def sort_dic_value_top(dic, top, reverse=False, min_value=None, max_value=None):
        """ sort dic by value >min_value or <max_value """
        list_item = []
        if dic and top > 0:
            for k, v in sorted(dic.items(), key=lambda d: d[1], reverse=reverse):
                if reverse and min_value is not None and v <= min_value:
                    break
                if not reverse and max_value is not None and v >= max_value:
                    break
                list_item.append((k, v))
                if len(list_item) >= top:
                    break
                pass
        return list_item
        pass

    @staticmethod
    def get_object_jmap(pid=None, is_live=False):
        dic = {'total': 0, 'detail': {}}
        if pid:
            cmd_object_stat = 'jmap -histo%s %d '
            if is_live:
                cmd_object_stat = cmd_object_stat % (':live', pid)
            else:
                cmd_object_stat = cmd_object_stat % ('', pid)
            out_object_stat = Command.run(cmd_object_stat)
            if not out_object_stat:
                return
            start = False
            for line in out_object_stat:
                if '---' in line:
                    start = True
                    continue
                if start:
                    item = line.split()
                    if item[0] == 'Total':
                        dic['total'] = int(item[1])
                        continue
                    key = item[3]
                    count = int(item[1])
                    if key not in dic['detail']:
                        dic['detail'][key] = count
            pass
        return dic
