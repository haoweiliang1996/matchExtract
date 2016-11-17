import json


with open("json/in.json","r") as f:
    dic=json.load(f)
    print(dic)
dic['我们']=True
with open("json/in.json","w") as f:
    json.dump(dic,f,ensure_ascii=False)
