import pandas as pd
import datetime
import demo.Car as Car
import demo.setting.Data_acquisition as Data_acquisition
import numpy as np
import sklearn.preprocessing as preprocessing

interval = 600

def Columns_Get(columns_info):
    new_columns = list()
    for column in columns_info:
        new_columns.append(column[0])

    return new_columns

def Listize(tuple):
    new_list = list()
    for tu in tuple:
        new_list.append(list(tu))
    return new_list


def datetime_to_string(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def string_to_datetime(st):
    return datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")


def cal_predict_finish_time(strtime, cost):
    h = cost // 3600
    m = cost % 3600 // 60
    s = cost % 60
    time = string_to_datetime(strtime)
    time = time + datetime.timedelta(hours=h, minutes=m, seconds=s)
    return datetime_to_string(time)


# 计算某物料、某车型、某仓库的剩余计划量
def cal_residual_plan(plan_day, plan_finish, key):
    a = plan_day[key]
    b = plan_finish[key]
    return a - b

# 时间窗口  now_time：字符串类型'2019-xx-xx xx:xx:xx'  add_time：秒为单位
def time_window(now_time, add_time):
    return datetime_to_string(string_to_datetime(now_time)+datetime.timedelta(seconds=add_time))

# 车辆初始化
def car_init(cars, flag):
    cars_list = list()
    # 厂外车辆初始化，仓库是列表类型，可能是多个，只能确定签到时间
    if flag == 'out':
        for index, row in cars.iterrows():
            car = Car.Car(row)
            car.set_target_warehouse(mat_warehouse[row['MAT_CODE']])
            cars_list.append(car)
    else:
        # 厂内和准备车辆初始化，准备车辆叫号且未进厂，只能确定签到和叫号时间，且仓库也确定为一个
        for index, row in cars.iterrows():
            car = Car.Car(row)
            car.init_target_warehouse(row)
            car.init_notice_time(row)
            # 若为厂内车辆，则还确定了进厂时间
            if flag == 'in':
                car.init_entry_time(row)
            cars_list.append(car)
    return cars_list


def init_plan_day():
    # 初始化plan_day
    df = Data_acquisition.read_plan_day()
    day = df['plan_date'].tolist()
    time = df['update_time'].tolist()
    for i in range(len(day)):
        time[i] = day[i] + ' ' + time[i]
    df = df.drop(columns=['plan_date', 'update_time'])
    df['update_time'] = time
    df = df[df['update_time'] > '2019-10-25']
    return df


mat_code = ['10201000030000', '10201000120000', '10201000220000', '10201000270000', '10301000050000',
                  '10301000170000', '10301000180000', '10301000250000', '10302000010000', '10302000020000',
                  '10302000050000', '10302000130000', '10302000150000', '10302000160000', '10302000170000',
                  '11002000010000', '11002000110000']
mat_dict = {'10201000030000': [], '10201000120000': [], '10201000220000': [], '10201000270000': [],
            '10301000050000': [], '10301000170000': [], '10301000180000': [], '10301000250000': [], '10302000010000': [],
            '10302000020000': [], '10302000050000': [], '10302000130000': [], '10302000150000': [], '10302000160000': [],
            '10302000170000': [], '11002000010000': [], '11002000110000': []}
warehouse_code = ['R02W0H01000', 'R02W0Y11B00', 'R02W2Y01D01', 'R02W0Y13000', 'R02W5Y01B00', 'R02W4Y01B00',
                  'R02W3Y03A00', 'R02W0Y06D00', 'R09W1Y01000', 'R02W0Y14D00', 'R02W0Y06C00', 'R02W0Y06A00',
                  'R02W0Y06E00', 'R01WAY01B00']
warehouse_dict = {'R02W0H01000': [], 'R02W0Y11B00': [], 'R02W2Y01D01': [], 'R02W0Y13000': [], 'R02W5Y01B00': [],
                  'R02W4Y01B00': [], 'R02W3Y03A00': [], 'R02W0Y06D00': [], 'R09W1Y01000': [], 'R02W0Y14D00': [],
                  'R02W0Y06C00': [], 'R02W0Y06A00': [], 'R02W0Y06E00': [], 'R01WAY01B00': []}
warehouse_mat = {'R02W0H01000': ['10201000120000', '10201000270000', '10201000220000', '10201000030000'],
                 'R02W0Y11B00': ['10301000050000'], 'R02W2Y01D01': ['10301000050000'],
                 'R02W0Y13000': ['10301000170000', '10301000050000'], 'R02W5Y01B00': ['10301000180000'],
                 'R02W4Y01B00': ['10301000180000'], 'R02W3Y03A00': ['10301000250000'],
                 'R02W0Y06D00': ['10302000170000', '10302000010000'], 'R09W1Y01000': ['10302000020000'],
                 'R02W0Y14D00': ['10302000130000', '10302000010000', '10302000050000', '10302000160000'],
                 'R02W0Y06C00': ['10302000130000', '10302000160000'], 'R02W0Y06A00': ['10302000150000'],
                 'R02W0Y06E00': ['10302000160000'], 'R01WAY01B00': ['11002000010000', '11002000110000']}
mat_warehouse = {'10201000030000': ['R02W0H01000'], '10201000120000': ['R02W0H01000'], '10201000220000': ['R02W0H01000'],
                 '10201000270000': ['R02W0H01000'], '10301000050000': ['R02W0Y11B00', 'R02W0Y13000', 'R02W2Y01D01'],
                 '10301000170000': ['R02W0Y13000'], '10301000180000': ['R02W5Y01B00', 'R02W4Y01B00'],
                 '10301000250000': ['R02W3Y03A00'], '10302000010000': ['R02W0Y14D00', 'R02W0Y06D00'],
                 '10302000020000': ['R09W1Y01000'], '10302000050000': ['R02W0Y14D00'],
                 '10302000130000': ['R02W0Y14D00', 'R02W0Y06C00'], '10302000150000': ['R02W0Y06A00'],
                 '10302000160000': ['R02W0Y06E00', 'R02W0Y14D00', 'R02W0Y06C00'],
                 '10302000170000': ['R02W0Y06D00'], '11002000010000': ['R01WAY01B00'],
                 '11002000110000': ['R01WAY01B00']}
sub_kind_name = ['破碎废钢', '统料废钢', '钢筋压块', '工厂压块', '刨花废钢', '统料压块', '薄片废钢', '硅钢片', '次新料压块', '硅钢片组', '钢筋切头']
# warehouse_limit = pd.read_excel('C:\\queue\\demo\\analyse_results\\warehouseLimit.xls')
# warehouse_unloadTime = pd.read_excel('C:\\queue\\demo\\analyse_results\\unloadTime.xls')
# warehouse_preTime = pd.read_excel('C:\\queue\\demo\\analyse_results\\preparationTime.xls')
warehouse_limit = pd.read_excel('/Users/pro/PycharmProjects/queue/demo/analyse_results/warehouseLimit.xls')
warehouse_unloadTime = pd.read_excel('/Users/pro/PycharmProjects/queue/demo/analyse_results/unloadTime.xls')
warehouse_preTime = pd.read_excel('/Users/pro/PycharmProjects/queue/demo/analyse_results/preparationTime.xls')

# def softmax(x):
#     """Compute softmax values for each sets of scores in x."""
#     pass  
#     x = np.array(x)
#     x = np.exp(x)
#     x.astype('float64')
#     if x.ndim == 1:
#         sumcol = sum(x)
#         for i in range(x.size):
#             x[i] = x[i]/float(sumcol)
#     if x.ndim > 1:
#         sumcol = x.sum(axis=0)
#         for row in x:
#             for i in range(row.size):
#                 row[i] = row[i]/float(sumcol[i])
#     return x

# def softmax(x):
#     x = np.array(x).reshape([-1, 1])
#     min_max_scaler = preprocessing.MinMaxScaler()
#     x_minmax = min_max_scaler.fit_transform(x)
#     x_minmax = x_minmax.reshape([1, -1])
#     return x_minmax.tolist()[0]

def softmax(x):
    """Compute the softmax of vector x in a numerically stable way."""
    shiftx = x - np.max(x)
    exps = np.exp(shiftx)
    return exps / np.sum(exps)




