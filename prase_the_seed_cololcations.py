#对最原始所给的种子库处理，去除‘词性’，尖括号等，所得结果去clas程序里面加tag
import re

with open('原料/collocation.in','r') as f:
    f_lines=list(map(lambda x:x.strip('\n'),f.readlines()))

#去掉注释
f_lines=list(filter(lambda x:re.search('//',x)==None and len(x)>0,f_lines))
#去掉 ！ 词类
f_lines = list(map(lambda x: re.sub('!|词类', '', x), f_lines))

f_lines = list(map(lambda x: re.sub('>|<', ' ', x), f_lines))

#去除行首的一个空格
for i in range(len(f_lines)):
    f_lines[i]=f_lines[i][1:]
f_lines=list(map(lambda x:re.sub('\* ','*',x),f_lines))
with open('0.in','w') as f:
    for line in f_lines:
        f.write(line+'\n')