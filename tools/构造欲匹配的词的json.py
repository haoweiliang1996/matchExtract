import json

with open("json/in.json","r") as f:
    d1=json.load(f)
    print(d1)
with open('原料/prase_clas_out.in','r') as f:
    d=json.load(f)

for keys in d.keys():
    if d1.get(keys) is None:
        d1[keys]=False
with open("json/in.json","w") as f:
    json.dump(d1,f,ensure_ascii=False)
