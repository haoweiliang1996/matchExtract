import os
import re
import sys
from functools import reduce

import json


def pre_prase(dir='',file_name=''):
    print(file_name)
    #pa="[0-9`~@#$^&*()=|{}\':;\',[].<>/?!~@#&*%{}《》、.、\“\”——’（）()--『』、、“”：]"#"[A-Za-z0-9\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]"
    with open("exp_data/"+dir+'/'+file_name+".data","r") as f:
        content=f.read()
    pa = ".*-.*-.*-.*/m  "  # 去掉前面的年份 如19980113-12-005-001/m
    str1=re.sub(pa,"",content)  #去掉多余符号
    print('1')
    pa=" [^ ]+/m"
    str1=re.sub(pa," mym/m",str1)
    pa=" [^ ]+/nr"
    str1=re.sub(pa," mynr/m",str1)
    #以结尾符将“句子单元”分开
    print('2')

    r=re.compile("[，。；！？]/w|\n+")
    itemsSet=r.split(str1)
    print('3')

    r1=re.compile(" +")
    itemsSet=list(map(lambda x:x.split(' '),itemsSet)) #将句子中的词放进句子的list中
    itemsSet=list(map(lambda x:list(filter(lambda y:len(y),x)),itemsSet)) #去除因为词间有多个空格导致的空str
    itemsSet=list(filter(lambda x:len(x),itemsSet))
    print('fiter ok')

    for items in itemsSet:
        items[0]+="_myhead"
        items[-1]+="_mytail"
    print('tail ok')

    print(file_name+'ok')
    return itemsSet

if __name__=='__main__':
    div_num=int(sys.argv[2])
    file_name=sys.argv[1]
    output_pathname='spmf_in/'+file_name+'/'+'before_prase'

    #查看存放某数据的结果的大文件夹是否存在
    if not os.path.exists(output_pathname):
        os.makedirs(output_pathname)
        print('make dir')
    #else:
     #   input('')
        #os.removedirs('spmf_in/'+file_name)
        #os.makedirs('spmf_in/' + file_name)

    #载入需要筛选的词
    json_in_filename = 'json/in.json'
    with open(json_in_filename, 'r') as f:
        dic = json.load(f)

    task= [a for a, b in dic.items() if b == False]
    print(task)

    def search_database(data_base):
        dic_of_output = {}
        for word in task:
            dic_of_output[word] = []
            for sentence_id in range(len(data_base)):
                sentence = data_base[sentence_id]
                for word_cmp in sentence:
                    if len(word_cmp) >= len(word) and word_cmp[0:len(word)] == word:
                        dic_of_output[word].append(sentence_id)
                        break
        return dic_of_output

    for i in range(div_num):
        data_base=pre_prase(file_name,file_name+'_'+str(i))
        dic_of_output=search_database(data_base)

        for word in task:
            with open(output_pathname+'/'+word+'_spmf'+'.in','a') as f_result:
                for sentence_id in dic_of_output[word]:
                    str1 = str(reduce(lambda a, b: a + ' -1 ' + b, data_base[sentence_id]))
                    str1 += ' -1 -2\n'
                    f_result.write(str1)

            #记录已经做好的word
            if i==div_num-1:
                dic[word] = True
                with open(json_in_filename, 'w') as f:
                    json.dump(dic, f, ensure_ascii=False)

