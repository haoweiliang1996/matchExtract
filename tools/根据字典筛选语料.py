import json
import sys
import os
from functools import reduce

'''
找出包含一些词的句段
需要的词在in.json中提供 若为False 则代表还没有处理过，需要处理
处理完后，将in.json 中该词的项置为true
'''
def filter_some_phase():
    json_in_filename = 'json/in.json'
    with open(json_in_filename, 'r') as f:
        dic = json.load(f)

    task = [a for a, b in dic.items() if b == False]
    json_filename = "filter_in/" + sys.argv[1] + 'filter' + '.in'
    with open(json_filename, 'r') as f:
        data_base = json.load(f)
    # print(data_base)
    print(task)
    # print(data_base)
    dic_of_output = {}
    for word in task:
        dic_of_output[word] = []
        for sentence_id in range(len(data_base)):
            sentence = data_base[sentence_id]
            for word_cmp in sentence:
                if len(word_cmp) >= len(word) and word_cmp[0:len(word)] == word:
                    dic_of_output[word].append(sentence_id)
                    break

    if not os.path.exists('spmf_in/' + sys.argv[1]):
        os.makedirs('spmf_in/' + sys.argv[1])

    for word in task:
        with open('spmf_in/' + sys.argv[1] + '/' + word + '_spmf.in', 'w') as f:
            for sentence_id in dic_of_output[word]:
                # print(data_base[sentence_id])
                str1 = str(reduce(lambda a, b: a + ' -1 ' + b, data_base[sentence_id]))
                str1 += ' -1 -2\n'
                f.write(str1)
        dic[word] = True
        with open(json_in_filename, 'w') as f:
            json.dump(dic, f, ensure_ascii=False)


if __name__ == '__main__':
    filter_some_phase()
