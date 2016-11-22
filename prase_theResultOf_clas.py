# 处理postagger后的结果，形成以中心词为key的词典，该词典的vaule是以pos pattern为key，出现次数为vaule的dict
import re
from collections import OrderedDict
from pprint import  pprint
import json
with open('原料/00.out', 'r') as f:
    f_lines = list(map(lambda x: x.strip('\n'), f.readlines()))

temp = f_lines
f_ = list(filter(lambda x: re.search('\|', x) == None and len(x) != 0, temp))

# 去掉中文与/，将w 替换为.
r1 = re.compile('/|[\u4E00-\u9FFF]+')
r1s = re.compile('\*w')
# 只保留中文
r2 = re.compile('/|[a-z]|\*')

f_ab = list(map(lambda x: r1.sub('', x), f_))
f_ab = list(map(lambda x: r1s.sub('.', x), f_ab))
#f_ab = list(map(lambda x:re.split(' +',x),f_ab))

f_re = list(map(lambda x: r2.sub('', x), f_))
f_re_list = list(map(lambda x: re.split(' +', x), f_re))

d = OrderedDict()

#种子库中以第一个词为中心词
for items in f_re_list:
    d[items[0]]={}

for i in range(len(f_re_list)):
    if d[f_re_list[i][0]].get(f_ab[i]) is None:
        d[f_re_list[i][0]][f_ab[i]]=1
    else:
        d[f_re_list[i][0]][f_ab[i]]+=1
pprint(d)
with open('原料/prase_clas_out.in','w') as f:
    json.dump(d,f,ensure_ascii=False)