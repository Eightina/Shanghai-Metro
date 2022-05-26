'''
Filename: c:\python\shanghai_metro\playground.py
Path: c:\python\shanghai_metro
Created Date: Wednesday, May 12th 2021, 10:11:48 pm
Author: SEELE a317

Copyright (c) 2021@625,7,YouYuan 
'''
import csv
import math

with open('shanghai_metro_line.csv', 'r', encoding='utf-8')as f:
    f_csv = csv.reader(f)
    rows = [row for row in f_csv]
dataset = []


def distance(MLatA, MLonA, MLatB, MLonB):
    C = math.sin(MLatA)*math.sin(MLatB)*math.cos(MLonA-MLonB) + \
        math.cos(MLatA)*math.cos(MLatB)
    return 6371.004*math.acos(C)*math.pi/180


for i in range(20):
    dataset.append([])
for i in dataset:
    for m in range(40):
        i.append([])
for i in rows[1:]:
    if len(i[0]) <= 2:
        dataset[int(i[0])][int(i[2])] = [int(i[0]), int(i[2]), i[3],
                                        # (float(i[8])+float(i[10])/2),
                                        # (float(i[9])+float(i[11])/2),
                                        float(i[4]),
                                        float(i[5]),
                                        [],
                                        [],
                                        float("inf"),
                                        [],
                                        False]


# 0线，1序号，2站点名，3经度，4纬度，5[可换乘线]，6[相连点的[线，序号]]，7到起点距离]，8父节点[线，序号]

for i in range(len(dataset)):
    for j in range(len(dataset[i])):
        if dataset[i][j]:
            st_name = dataset[i][j][2]
            for m in range(len(dataset)):
                for n in range(len(dataset[m])):
                    if dataset[m][n]:
                        if dataset[m][n][2] == st_name and m != i:
                            dataset[i][j][5].append(m)
                            dataset[i][j][6].append([m, n])

# print(dataset[8][22])

line_length = {1: 28, 2: 30, 3: 29, 4: 26, 5: 11,
                6: 28, 7: 32, 8: 30, 9: 35, 10: 32,
                11: 36, 12: 32, 13: 31, 16: 13, 17: 13}
for i in range(len(dataset)):
    for j in range(len(dataset[i])):
        if dataset[i][j]:
            station = dataset[i][j]
            if station[1] == 1:
                station[6].append([i, j+1])
            elif station[1] == line_length[i]:
                station[6].append([i, j-1])
            else:
                station[6].append([i, j+1])
                station[6].append([i, j-1])

# print(dataset[8][22])

st_station = dataset[8][22]
ed_station = dataset[11][34]
st0 = st_station[0]
st1 = st_station[1]
ed0 = ed_station[0]
ed1 = ed_station[1]
dataset[st0][st1][7] = 0
# 0线，1序号，2站点名，3经度，4纬度，5[可换乘线]，6[相连点的[线，序号]]，7到起点费用，8父节点[线，序号]

transfer={(10,11):1/60,
        (11,10):1/60,
        (8,11):2/60,(11,8):2/60,
        (11,1):1/60,(1,11):1/60,
        (8,1):6/60,(1,8):6/60,
        (11,2):4/60,(2,11):4/60,
        (2,8):4/60,(8,2):4/60,
        (11,3):3/60,(3,11):3/60,
        (3,8):5/60,(8,3):5/60,
        (11,9):2/60,(9,11):2/60,
        (9,8):3/60,(8,9):3/60,
        (11,4):3/60,(4,11):3/60,
        (4,10):4/60,(10,4):4/60,
        (11,13):1/60,(13,11):1/60,
        (13,12):2/60,(12,13):2/60,
        (12,8):2/60,(8,12):2/60,
        (2,10):3/60,(10,2):3/60}

def get_time_cost(a, b):
    station1 = dataset[a[0]][a[1]]
    station2 = dataset[b[0]][b[1]]
    if station2[2]=="四平路":
        return 0
    elif a[0] == b[0]:
        x1, y1 = station1[3], station1[4]
        x2, y2 = station2[3], station2[4]
        if b[0] == 10:
            return (distance(x1, y1, x2, y2)/75+0.025)
        elif b[0] == 3:
            return (distance(x1, y1, x2, y2)/75+0.025)
        else:
            return distance(x1, y1, x2, y2)/75+0.025
    else:
        return transfer.get((a[0],b[0]),0.15)+10
    


def update_cost(st):
    m, n = st[0], st[1]
    for i in dataset[m][n][6]:
        st_line, st_num = i[0], i[1]
        # dataset[st_line][st_num][7]=min(get_relate_cost([station0[0],station0[1]],i)+station0[7],
        #                                 dataset[st_line][st_num][7])
        new_cost = get_time_cost([m, n], i)+dataset[m][n][7]
        # print([m,n])
        # print(i)
        # print()
        # print(new_cost)
        if new_cost < dataset[st_line][st_num][7]:
            dataset[st_line][st_num][7] = new_cost
            dataset[st_line][st_num][8] = [m, n]


def done():
    for i in dataset[ed0][ed1][6]:
        if dataset[i[0]][i[1]][7] == float("inf"):
            return False
    return True


cnt = 0
st2upd = st_station
while not done():
    dis = []
    index_list = []
    cnt += 1
    update_cost(st2upd)
    st2upd[9] = True
    for i in range(len(dataset)):
        for j in range(len(dataset[i])):
            relate_st = dataset[i][j]
            if relate_st:
                if relate_st[9] == False:
                    dis.append(relate_st[7])
                    index_list.append([i, j])
    index = dis.index(min(dis))
    tar = index_list[index]
    st2upd = dataset[tar[0]][tar[1]]

    # if relate_st[9]==False and relate_st[7]<dis:
    #     dis=relate_st[7]
    #     st2upd=dataset[relate_st[0]][relate_st[1]]
print('turn'+str(cnt))
print('done!')


def get_chain(st):
    if st[8]:
        up = st[8]
        return dataset[up[0]][up[1]]
    else:
        return False


st = dataset[ed0][ed1]

while get_chain(st):
    print(st[0], st[1], st[2], st[7])
    st = get_chain(st)
