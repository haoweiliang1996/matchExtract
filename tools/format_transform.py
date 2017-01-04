#将BIDE+的输出转换为BIDE+的输入格式
import json
import re
import sys

def main():
    open_file_path=sys.argv[1]
    with open(open_file_path,'r') as f:
        f_lines=list(map(lambda  x:x.strip('\n'),f.readlines()))
    f_lines=list(map(lambda x:re.sub('  #SUP.*',' -2',x),f_lines))
    output_file_path=sys.argv[2]
    with open(output_file_path,'w') as f:
        for str in f_lines:
            f.write(str+'\n')

if __name__== '__main__':
    main()