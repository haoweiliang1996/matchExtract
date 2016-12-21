import subprocess
import json
import tools.myLogger
import shlex

def main(data_name):
    with open('json/serialization_prase_the_result.json','r') as f:
        d=json.load(f)
        todo=[]
        for key in d.keys():
            if d[key] == True:
                todo.append(key)

    subRate=0.01*0.1
    input_pathName='spmf_in/'+data_name+'/'+'after_prase/'
    output_pathName=''
    for task in todo:
        cmd='java -jar java/spmf.jar run BIDE+_with_strings '+' '+input_pathName+task+' '+task+'BIDE+.out '+str(subRate)
        cmdl=shlex.split(cmd)
        subprocess.run(cmdl)