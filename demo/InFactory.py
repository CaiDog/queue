import demo.setting.Tools as Tool
import numpy as np
from demo.Warehouse import Warehouse
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
        self.__cars_list = Tool.car_init(cars, 'in')  # 所有在厂外的carlist
        self.__warehouse_list = self.__warehouse_init(self.__cars_list, 'minorMax', 0.7)    # 仓库类列表
        self.plan_day = Tool.init_plan_day()

    # 厂内各个仓库信息初始化
    def __warehouse_init(self, cars, flag1, flag2):
        warehouse_list = list()
        for warehouse_code in Tool.warehouse_code:
            cars_list = list()
            for car in cars:
                if car.get_target_warehouse() == warehouse_code:
                    cars_list.append(car)
            warehouse_list.append(Warehouse(warehouse_code, Tool.warehouse_mat[warehouse_code], cars_list, flag1, flag2))
        return warehouse_list

    def cal_warehouse_priority(self):
        # 计算 rest剩余未完成量、last_time距离上次plan_day修改时间、（仓库合理工作强度-当前车辆工作数）的softmax函数
        rest_list = list()
        last_time_list = list()
        cars_num_list = list()
        for warehouse in self.__warehouse_list:
            rest_list.append(warehouse.get_rest())
            last_time_list.append(warehouse.get_last_time())
            cars_num_list.append(warehouse.get_rea() - len(warehouse.get_cars()))
        rest = np.array(rest_list)
        last_time = np.array(last_time_list)
        cars_num = np.array(cars_num_list)
        rest = np.exp(rest) / sum(np.exp(rest))
        last_time = np.exp(last_time) / sum(np.exp(last_time))
        cars_num = np.exp(cars_num) / sum(np.exp(cars_num))
        # 计算优先级
        for i in range(len(self.__warehouse_list)):
            self.__warehouse_list[i].set_priority((rest[i] * last_time[i]) / cars_num[i])

    def get_cars_list(self):
        return self.__cars_list




















