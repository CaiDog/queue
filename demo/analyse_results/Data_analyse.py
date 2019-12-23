import numpy as np
import pandas as pd
import demo.setting.Data_acquisition as da
import demo.setting.Tools as tool
import datetime
from scipy import stats


mat_code = ['10201000030000', '10201000120000', '10201000220000', '10201000270000', '10301000050000',
                  '10301000170000', '10301000180000', '10301000250000', '10302000010000', '10302000020000',
                  '10302000050000', '10302000130000', '10302000150000', '10302000160000', '10302000170000',
                  '11002000010000', '11002000110000']
warehouse_code = ['R02W0H01000', 'R02W0Y11B00', 'R02W2Y01D01', 'R02W0Y13000', 'R02W5Y01B00', 'R02W4Y01B00',
                  'R02W3Y03A00', 'R02W0Y06D00', 'R09W1Y01000', 'R02W0Y14D00', 'R02W0Y06C00', 'R02W0Y06A00',
                  'R02W0Y06E00', 'R01WAY01B00']
warehouse_dict = {'R02W0H01000': [], 'R02W0Y11B00': [], 'R02W2Y01D01': [], 'R02W0Y13000': [], 'R02W5Y01B00': [],
                  'R02W4Y01B00': [], 'R02W3Y03A00': [], 'R02W0Y06D00': [], 'R09W1Y01000': [], 'R02W0Y14D00': [],
                  'R02W0Y06C00': [], 'R02W0Y06A00': [], 'R02W0Y06E00': [], 'R01WAY01B00': []}
data = da.entry_queue_data_acquisition()
data = data[['TASK_ID', 'KIND_CODE', 'SUB_KIND_CODE', 'MAT_CODE', 'QUEUE_START_TIME', 'WAREHOUSE_CODE',
             'ENTRY_NOTICE_TIME', 'ENTRY_TIME', 'FINISH_TIME']]

for index, row in data.iterrows():
    # print(index, datetime.datetime.now(), row['TASK_ID'])
    if row['SUB_KIND_CODE'] == 'GJYK':
        data.at[index, 'SUB_KIND_CODE'] = 30
    elif row['SUB_KIND_CODE'] == 'PSFL':
        data.at[index, 'SUB_KIND_CODE'] = 50
    elif row['SUB_KIND_CODE'] == 'GCYK':
        data.at[index, 'SUB_KIND_CODE'] = 40

# 数据分析1：找同一品种去不同仓库的比例
def data_analyse1(data):
    for mat in mat_code:
        df = data[data['MAT_CODE'] == mat]
        warehouse_code = set(df['WAREHOUSE_CODE'].tolist())
        if len(warehouse_code) == 1:
            print('物料名：' + mat + '只有一个仓库去向')
            print(warehouse_code)
        else:
            for warehouse in warehouse_code:
                w = len(df[df['WAREHOUSE_CODE'] == warehouse])
                print('物料名：' + mat + ' 仓库：' + warehouse + '占比：' + str(w / len(df)))

# 数据分析2：找一个仓库去不同品种的比例
def data_analyse2(data):
    for warehouse in warehouse_code:
        df = data[data['WAREHOUSE_CODE'] == warehouse]
        mat_code = set(df['MAT_CODE'].tolist())
        mat_code = list(mat_code)
        if len(mat_code) == 1:
            # print('仓库名：' + warehouse + '只有一种物料来')
            print(warehouse, ':', mat_code[0])
        else:
            print(warehouse,':')
            for mat in mat_code:
                m = len(df[df['MAT_CODE'] == mat])
                # print('仓库名：' + warehouse + ' 物料：' + mat + '占比：' + str(m / len(df)))
                print(mat, ',')


# 统计仓库卸货时间
def data_analyse3(data):
    result = list()
    data['COST_TIME'] = (
                data['FINISH_TIME'].apply(da.To_Date) - data['ENTRY_TIME'].apply(da.To_Date)).apply(
        lambda x: x.total_seconds())
    for warehouse in warehouse_code:
        df = data[data['WAREHOUSE_CODE'] == warehouse]
        df = df['COST_TIME'].tolist()
        df.sort()
        if len(df) == 0:
            continue
        temp = list()
        temp.append(warehouse)
        temp.append(df[0])
        index = len(df) // 3
        df = df[0: index + 1]
        temp.append(np.mean(df))
        result.append(temp)
    df = pd.DataFrame(result, columns=['warehouse_code', 'minTime', 'minorTime'])
    df.to_excel('unloadTime.xls', index=False)

# 统计仓库工作强度
def data_analyse4(data):
    result = list()
    hour = datetime.timedelta(hours=1)
    half_hour = datetime.timedelta(minutes=30)
    time = '2019-10-25 00:00:00'
    while time != '2019-11-29 00:00:00':
        for warehouse in warehouse_code:
            num = len(data[(data['WAREHOUSE_CODE'] == warehouse) & (data['ENTRY_TIME'] < time)
            & (data['FINISH_TIME'] > time)])
            warehouse_dict[warehouse].append(num)
            # print(warehouse, '在', time, '的时候有', num, '辆车')
        time = tool.datetime_to_string(tool.string_to_datetime(time) + hour)

    for warehouse in warehouse_code:
        j = 0
        for i in range(len(warehouse_dict[warehouse])):
            if warehouse_dict[warehouse][j] == 0:
                warehouse_dict[warehouse].pop(j)
            else:
                j += 1
        temp = list()
        temp.append(warehouse)
        temp.append(stats.mode(warehouse_dict[warehouse])[0][0])
        temp.append(max(warehouse_dict[warehouse]))
        # print(warehouse, '的众数是：', stats.mode(warehouse_dict[warehouse])[0][0])
        # print(warehouse, '的max是：', max(warehouse_dict[warehouse]))
        warehouse_dict[warehouse].sort(reverse=True)
        temp.append(int(np.mean(warehouse_dict[warehouse][0: len(warehouse_dict[warehouse]) // 3 + 1])))
        result.append(temp)
        # print(warehouse, '的较大值是：', np.mean(warehouse_dict[warehouse][0: len(warehouse_dict[warehouse]) // 3 + 1]))
    df = pd.DataFrame(result, columns=['warehouse_code', 'mode', 'max', 'minorMax'])
    df.to_excel('warehouseLimit.xls', index = False)

# 求每个仓库的ENTRY_TIME-NOTICE_TIME的平均值
def data_analyse5(data):
    result = list()
    for warehouse in warehouse_code:
        df = data[data['WAREHOUSE_CODE'] == warehouse]
        df['COST_TIME'] = (
                df['ENTRY_TIME'].apply(da.To_Date) - df['ENTRY_NOTICE_TIME'].apply(da.To_Date)).apply(
            lambda x: x.total_seconds())
        df = df['COST_TIME'].tolist()
        temp = list()
        temp.append(warehouse)
        temp.append(np.mean(df))
        result.append(temp)
    df = pd.DataFrame(result, columns=['warehouse_code', 'preparation_time'])
    df.to_excel('preparationTime.xls', index=False)

data_analyse1(data)


