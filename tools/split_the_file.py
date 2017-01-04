import os
import sys

def split_the_file():
    filePath='exp_data/'+sys.argv[1]
    fileName=filePath+'.data'
    if not os.path.exists(filePath):
        os.makedirs(filePath)

    div_num=int(sys.argv[2])

    with open(fileName,'r') as f:
        f_list=f.readlines()
        f_len=len(f_list)
        incr_step=int(f_len/div_num)
        cnt=0
        for beg_idx in range(0,f_len,incr_step):
            end_idx=min(f_len,beg_idx+incr_step)#左闭右开
            f_split_name=filePath+'/'+sys.argv[1]+'_'+str(cnt)+'.data'
            cnt+=1
            with open(f_split_name,'w') as f_split:
                for id in range(beg_idx,end_idx):
                    f_split.write("".join(f_list[id]))

def merge_the_file(file_name,div_num):
    print('')
