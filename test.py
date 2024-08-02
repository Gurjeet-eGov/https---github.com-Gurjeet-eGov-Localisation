import json

with open('action_test.txt') as atf:
    at=json.load(atf)

with open('action_id_1.txt') as aif1:
    ai=json.load(aif1)

aid=[]
for i in ai:
    if i["rolecode"]=="EMPLOYEE":
        aid.append(i["actionid"])

print(len(aid))

ate=[]

for i in aid:
    for j in at: 
        if j['id'] == i:
            ate.append(j)

print(len(ate))
with open('export.txt', "w") as etf:
    json.dump(ate, etf)
