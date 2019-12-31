import demo.setting.Tools as Tool
import numpy as np
from demo.Warehouse import Warehouse
from demo.Material import Material
import datetime
import demo.setting.Data_acquisition as Data_acquisition


class InFactory(object):

    """
    模块说明：
            1）	记录厂内所有车辆的信息（仓库签到了的车，以及在厂内活动的车）
            2）	记录厂内所有仓库的信息（包括各个仓库对象）
            3）	对进厂前多仓库的顺序推荐结果进行更新

    """
    def __init__(self, time):

        # Car类初始化，从数据中读取出在时间time下所有在厂内的车辆
        cars = Data_acquisition.inFactory_cars(time)
        self.__cars_list = Tool.car_init(cars, 'in')  # 所有在厂内的carlist
        self.__warehouse_list = self.warehouse_init(self.__cars_list, 'minorMax', 0.7, 'minorTime')    # 仓库类列表

    # 厂内各个仓库信息初始化
    def warehouse_init(self, cars, flag1, flag2, flag3):
        warehouse_list = list()
        for warehouse_code in Tool.warehouse_code:
            mat_list = list()   # 原料类列表
            cars_list = list()  # 正在该仓库内卸货车辆的列表
            for car in cars:
                if car.get_target_warehouse() == warehouse_code:
                    cars_list.append(car)
            for mat_code in Tool.warehouse_mat[warehouse_code]:
                # 外购废钢看小品名
                if mat_code == '11002000010000':
                    for sub_kind_name in Tool.sub_kind_name:
                        mat_list.append(Material(mat_code, sub_kind_name))
                # 其他原料看物料名
                else:
                    mat_list.append(Material(mat_code, None))
            warehouse_list.append(Warehouse(warehouse_code, mat_list, cars_list, flag1, flag2, flag3))
        return warehouse_list

    def cal_mat_priority(self, now_time):
        # 计算 rest剩余未完成量、(now_time-last_time)距离上次plan_day修改时间、（仓库合理工作强度-当前车辆工作数）的softmax函数
        rest_list = list()
        time_list = list()
        cars_num_list = list()
        for warehouse in self.__warehouse_list:
            for mat in warehouse.get_mat_list():
                rest_list.append(mat.get_rest())
                time_list.append(int((Tool.string_to_datetime(now_time) - Tool.string_to_datetime(mat.get_last_time())).total_seconds()))
                cars_num_list.append(warehouse.get_rea() - warehouse.get_act())
        rest = Tool.softmax(rest_list)
        last_time = Tool.softmax(time_list)
        cars_num = Tool.softmax(cars_num_list)
        # 计算优先级
        index = 0
        for i in range(len(self.__warehouse_list)):
            priority_list = list()
            for j in range(len(self.__warehouse_list[i].get_mat_list())):
                if cars_num[i] == 0:
                    priority_list.append(0)
                else:
                    priority_list.append((rest[index] * last_time[index]) / cars_num[index])
                index += 1
            self.__warehouse_list[i].set_mat_priority(priority_list)
            print(priority_list)


    def get_cars_list(self):
        return self.__cars_list

    def get_warehouse(self):
        return self.__warehouse_list

    def update(self, time, cars_list):
        # 删除出厂的车
        temp_list = self.__cars_list
        for car in temp_list:
            if car.get_finish_time() <= time:
                self.__cars_list.remove(car)
        warehouse_car_dict = Tool.warehouse_dict
        # 加入新入厂的车辆
        for car in cars_list:
            self.__cars_list.append(car)
            warehouse_car_dict[car.get_target_warehouse()].append(car)
        # 更新仓库信息
        for warehouse in self.__warehouse_list:
            warehouse.update(time, warehouse_car_dict[warehouse.get_warehouse_code()])





















