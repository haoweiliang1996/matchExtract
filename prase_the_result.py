# -*- coding: utf-8 -*-
# 利用长短，词性，搭配的词性组摘取短句
import sys
import json
import re
import os
import copy
from pprint import pprint as pprint
from functools import reduce
from collections import OrderedDict
import logging

logger = logging.getLogger()
import subprocess

# 获取当前运行的pid
import psutil

pid = psutil.Process(os.getpid())
print_Mem_Occupy = lambda: logger.info("系统内存情况：" + str(psutil.virtual_memory()) + '程序内存情况：' + str(pid.memory_info()))

'''
data_name 文件名
word_name 主要挖掘这个word的搭配
'''


def prase_the_result_a_word(data_name, word_name):
    with open('spmf_in/' + data_name + '/' + 'before_prase/' + word_name + '_spmf.in', 'r') as f:
        f_line = [line.strip('\n') for line in f.readlines()]

    TAIL_INFO_NUM = 1  # 每个句子最后面有一个项保存sup
    r = re.compile(' -1 ')
    f_line = list(map(lambda x: r.split(x), f_line))
    f_line_range = range(len(f_line))
    ###
    f_abstract = []  # 去除文字,只保留词性表示
    # print (f_line)
    logOk = lambda x: logger.debug(word_name + x + ' ok!')
    for sentence in copy.deepcopy(f_line):
        ### 去除matail,myhead
        cmp = lambda x, goal: len(x) > len(goal) and x[-len(goal):] == goal
        if cmp(sentence[0], '_myhead'):
            sentence[0] = sentence[0][0:-len('_myhead')]
        if cmp(sentence[-1 - TAIL_INFO_NUM], '_mytail'):
            sentence[-1 - TAIL_INFO_NUM] = sentence[-1 - TAIL_INFO_NUM][0:-len('_mytail')]
        ###
        temp = ''
        for word in sentence[0:-1]:
            word = word.lower()
            if word[-1] == 'a' or word[-1] == 'n' or word[-1] == 'v':
                temp += ('/' + str(len(word) - len('/a')) + word[-1])
            else:
                idx_of_divide = 0
                for i in range(-1, -4, -1):
                    if word[i] == '/':
                        idx_of_divide = i
                        break
                temp += (word[idx_of_divide:])
            temp += ' '
        f_abstract.append(temp)
    logOk('f_abstract')
    # print(f_abstract)
    ###

    ###
    f_abstract_withkey = []
    for sentence in copy.deepcopy(f_line):
        ### 去除matail,myhead
        cmp = lambda x, goal: len(x) > len(goal) and x[-len(goal):] == goal
        if cmp(sentence[0], '_myhead'):
            sentence[0] = sentence[0][0:-len('_myhead')]
        if cmp(sentence[-1 - TAIL_INFO_NUM], '_mytail'):
            sentence[-1 - TAIL_INFO_NUM] = sentence[-1 - TAIL_INFO_NUM][0:-len('_mytail')]
        ###
        temp = ''
        key = word_name
        cmp_key = lambda x: len(x) > len(key) and x[0:len(key)] == key
        for word_i in range(len(sentence[0:-1])):
            word = sentence[word_i].lower()
            temp += str(word_i)
            if cmp_key(word):
                temp += '/ke'
            else:
                idx_of_divide = 0
                for i in range(-1, -4, -1):  # [-1，,3] 因为最长是三个 比如/nr
                    if word[i] == '/':
                        idx_of_divide = i
                        break
                temp += (word[idx_of_divide:])
            temp += ' '
        f_abstract_withkey.append(temp)
    logOk('abstract_with_key')

    ###

    def filter_the_phase_base_word(i):
        ll = f_line[i]
        kount = len(ll)
        cmp = lambda x, goal: len(x) > len(goal) and x[-len(goal):] == goal
        if cmp(ll[0], 'myhead') or cmp(ll[-1 - TAIL_INFO_NUM], 'mytail'):
            return True
        if kount < 2 + TAIL_INFO_NUM:
            return False
        return True

    def filter_the_phase_base_partsOfSpeech(i):
        r = re.compile('([2-9](n|v|a))|f|i|l|t|q|m')
        return r.search(f_abstract[i]) != None

    f_filter_withkey = []
    with open('原料/prase_clas_out.in', 'r') as f:
        dic_temp = json.load(f)
        if dic_temp.get(word_name) is None:
            logger.warning('json.in中的词没有包含在种子库中 ' + word_name)
            return
        rule = list(map(lambda x: re.split(' +', x), dic_temp[word_name].keys()))
        logger.info('现在都是将第一个处理为key')
        for id in range(len(rule)):
            rule[id][0] = 'ke'
        # 将原来的种子模式改造成正则表达式
        formulation = lambda a: '[0-9]+/' + a + ' '
        put_rule_together = lambda rule_list: reduce(lambda a, b: a + '|' + b, rule_list)
        for id in range(len(rule)):
            rule[id] = list(map(formulation, rule[id]))
            rule[id] = ''.join(rule[id])
        rule_str = str(put_rule_together(rule))
        r = re.compile(rule_str)
        logOk('open rule of key')
        logger.info('word' + word_name + 'rule:' + str(rule) + '\n')

    def filter_the_phase_base_keyword(i):
        res = r.search(f_abstract_withkey[i])
        if i % 10000 == 0:
            logger.debug(str(i) + ' OK')
            print_Mem_Occupy()
        if res is None:
            return False
        else:
            startId_char, endId_char = res.span()
            str_cut = f_abstract_withkey[i][startId_char:endId_char]
            str_cut = re.sub('/[a-z]+', '', str_cut)  # 只保留下标，去除词性
            str_cut = str_cut.strip(' ')  # 去除尾部多余的一个空格  ???怎么产生的 生成的时候每个都都加了一个空格，而spilt最后的空格不能有，否则会有个空的
            startId_word, endId_word = int(str_cut.split(' ')[0]), int(str_cut.split(' ')[-1])
            f_filter_withkey.append((startId_word, endId_word + 1))  # +1是为了左闭右开
            # print(rule_str)
            if i % 10000 == 0:
                logger.info(f_abstract_withkey[i])
                logger.info(f_line[i])
                logger.info(f_filter_withkey[-1])
            return True

    res = f_line_range
    # res=list(filter(filter_the_phase_base_partsOfSpeech,res))
    # logOk('filter_the_phase_base_partsOfSpeech')
    res = list(filter(filter_the_phase_base_word, res))
    logOk('filter_the_phase_base_word')
    # print(res[0])
    res = list(filter(filter_the_phase_base_keyword, res))
    logOk('filter_the_phase_base_keyword')
    path_name = 'spmf_in/' + data_name + '/after_prase/'
    if not os.path.exists(path_name):
        os.makedirs(path_name)
        logger.info(path_name + ' created!')

    # 结果写入文件
    with open(path_name + 'spmf_in_after_prase_' + word_name + '.in', 'w') as f:
        '''
        dic=OrderedDict()
        for phase_id in range(len(res)):
            phase_id_in_res=res[phase_id]
            begId,endId=f_filter_withkey[phase_id]
            #print(f_filter_withkey[phase])
            #print(f_line[phase])
            phase=str(f_line[phase_id_in_res][begId:endId])
            if dic.get(phase) == None:
                dic[phase]=1
            else:
                dic[phase]+=1

        #json.dump(dic,f,ensure_ascii=False)
        '''
        for phase_id in range(len(res)):
            phase_id_in_res = res[phase_id]
            begId, endId = f_filter_withkey[phase_id]
            # print(f_filter_withkey[phase])
            # print(f_line[phase])
            phase = f_line[phase_id_in_res][begId:endId]
            # print(phase)
            strtemp = ''
            for word in phase:
                strtemp += word + ' -1 '
            strtemp += '-2\n'
            # f.write(key+' '+str(dic[key]))
            # f.write('\n')
            f.write(strtemp)
        '''
        for key in dic.keys():
            f.write(key+' '+str(dic[key]))
            f.write('\n')
        '''
        # pprint(dic)
        # print(res)


def main():
    sys.argv.append('exp_1-2000w')
    data_name = sys.argv[1]
    # init a looger to console and file

    # if not os.path.exists('spmf_in/'+data_name+"/"+'log.log'):
    #  f_temp=open('spmf_in/'+data_name+"/"+'log.log','w')
    #  f_temp.close()

    fh = logging.FileHandler('spmf_in/' + data_name + "/" + 'log.log')
    ch = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(ch)

    # load  a sequence of what to prase
    seria_in_filename_with_path = 'json/serialization_prase_the_result.json'
    if not os.path.exists(seria_in_filename_with_path):
        with open('json' + '/' + 'in.json', 'r') as f:
            d = json.load(f)
            d_keys = list(d.keys())
        with open(seria_in_filename_with_path, 'w') as f:
            d = {}
            for word in d_keys:
                d[word] = False
            json.dump(d, f, ensure_ascii=False)
    with open(seria_in_filename_with_path, 'r') as f:
        d = json.load(f)

    total_ToDo = 0
    for value in d.values():
        if value == False:
            total_ToDo += 1
    logger.info('总共需要处理的词：' + str(len(d)) + '本次需要处理的词：' + str(total_ToDo))
    finish_Do = 1
    for word_name in d.keys():
        if d[word_name] == False:
            logger.info('-' + word_name + ' begin-')
            prase_the_result_a_word(data_name, word_name)
            with open(seria_in_filename_with_path, 'w') as f:
                d[word_name] = True
                finish_Do += 1
                logger.info(word_name + ' OK!')
                logger.info('finish_Do' + str(finish_Do) + 'left_Do' + str(total_ToDo - finish_Do))
                json.dump(d, f, ensure_ascii=False)
        else:
            logger.info(word_name + 'has already done')
            finish_Do += 1


if __name__ == '__main__':
    main()
