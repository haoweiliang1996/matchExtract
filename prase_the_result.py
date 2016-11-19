import sys
import json
import re
import os
import copy
from pprint import  pprint as pprint
from functools import reduce
from collections import OrderedDict

data_name=sys.argv[1]
word_name=sys.argv[2]
with open('spmf_out/'+data_name+'/BIDE+_'+word_name+'.out','r') as f:
    f_line=[line.strip('\n') for line in f.readlines()]

TAIL_INFO_NUM=1  #每个句子最后面有一个项保存sup
r=re.compile(' -1 ')
f_line=list(map(lambda x:r.split(x),f_line))
f_line_range=range(len(f_line))
###
f_abstract=[] #去除文字,只保留词性表示
#print (f_line)
for sentence in copy.deepcopy(f_line):
    ### 去除matail,myhead
    cmp = lambda x, goal: len(x) > len(goal) and x[-len(goal):] == goal
    if cmp(sentence[0], '_myhead'):
        sentence[0]=sentence[0][0:-len('_myhead')]
    if cmp(sentence[-1-TAIL_INFO_NUM],'_mytail'):
        sentence[-1-TAIL_INFO_NUM]=sentence[-1-TAIL_INFO_NUM][0:-len('_mytail')]
    ###
    temp=''
    for word in sentence[0:-1]:
        word=word.lower()
        if word[-1]=='a' or word[-1]=='n' or word[-1]=='v':
            temp+=('/'+str(len(word)-len('/a'))+word[-1])
        else:
            idx_of_divide=0
            for i in range(-1,-4,-1):
                if word[i]=='/':
                    idx_of_divide=i
                    break
            temp+=(word[idx_of_divide:])
        temp+=' '
    f_abstract.append(temp)
#print(f_abstract)
###

###
f_abstract_withkey=[]
for sentence in copy.deepcopy(f_line):
    ### 去除matail,myhead
    cmp = lambda x, goal: len(x) > len(goal) and x[-len(goal):] == goal
    if cmp(sentence[0], '_myhead'):
        sentence[0]=sentence[0][0:-len('_myhead')]
    if cmp(sentence[-1-TAIL_INFO_NUM],'_mytail'):
        sentence[-1-TAIL_INFO_NUM]=sentence[-1-TAIL_INFO_NUM][0:-len('_mytail')]
    ###
    temp=''
    key=word_name
    cmp_key=lambda x:len(x)>len(key) and x[0:len(key)]==key
    for word_i in range(len(sentence[0:-1])):
        word=sentence[word_i].lower()
        temp+=str(word_i)
        if cmp_key(word):
            temp+='/ke'
        else:
            idx_of_divide=0
            for i in range(-1,-4,-1): #[-1，,3] 因为最长是三个 比如/nr
                if word[i]=='/':
                    idx_of_divide=i
                    break
            temp+=(word[idx_of_divide:])
        temp+=' '
    f_abstract_withkey.append(temp)
###

def filter_the_phase_base_word(i):
    ll=f_line[i]
    kount=len(ll)
    cmp=lambda x,goal:len(x)>len(goal) and x[-len(goal):]==goal
    if cmp(ll[0],'myhead') or cmp(ll[-1-TAIL_INFO_NUM],'mytail'):
        return True
    if kount<2+TAIL_INFO_NUM:
        return False
    return True

def filter_the_phase_base_partsOfSpeech(i):
    r=re.compile('([2-9](n|v|a))|f|i|l|t|q|m')
    return r.search(f_abstract[i]) != None

f_filter_withkey=[]
def filter_the_phase_base_keyword(i):
    rule=[['ke','.','r'],
          ['ke','.','v','v'],
          ['ke','.','n'],
          ['ke','.','f'],
          ['ke','.','v'],
          ['ke','.','c','v'],
          ['ke','.','p','.','v']
          ]
    formulation=lambda  a:'[0-9]+/'+a+' '
    put_rule_together=lambda  rule_list:reduce(lambda  a,b:a+'|'+b,rule_list)
    for id in range(len(rule)):
        rule[id]=list(map(formulation,rule[id]))
        rule[id]=''.join(rule[id])
    rule_str=str(put_rule_together(rule))
    #print(rule_str)
    r=re.compile(rule_str)
    res=r.search(f_abstract_withkey[i])
    if res==None:
        return False
    else:
        startId_char,endId_char=res.span()
        str_cut=f_abstract_withkey[i][startId_char:endId_char]
        str_cut=re.sub('/[a-z]+','',str_cut)#只保留下标，去除词性
        str_cut=str_cut.strip(' ')#去除尾部多余的一个空格
        startId_word,endId_word=int(str_cut.split(' ')[0]),int(str_cut.split(' ')[-1])
        f_filter_withkey.append((startId_word,endId_word+1)) #+1是为了左闭右开
        #print(rule_str)
        print(f_abstract_withkey[i])
        print(f_line[i])
        print(f_filter_withkey[-1])
        return True

res=f_line_range
#res=list(filter(filter_the_phase_base_partsOfSpeech,res))
#res=list(filter(filter_the_phase_base_word,res))
#print(res[0])
res=list(filter(filter_the_phase_base_keyword,res))

path_name='spmf_out/'+data_name+'/after_prase'
if not os.path.exists(path_name):
    os.makedirs(path_name)
with open(path_name+'/'+'BIDE+_after_prase_'+word_name+'.out','w') as f:

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
        #print(phase)
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

    # pprint(dic)
#print(res)

