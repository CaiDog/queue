import demo.setting.Data_acquisition as Data_acquisition
import demo.setting.Tools as Tool
from demo.InFactory import InFactory
import numpy as np
import datetime


class OutFactory(object):

    """
    厂外信息模块：
                1）	当车辆签到后，初始化该车辆的信息
                2）	根据排队规则排队车辆直接进厂或者在厂外排队
                3）	对于厂外排队的车辆进行等待时间的预测
                4）	对于需要去多仓库提货的车辆，进行仓库顺序的推荐
    """
    def __init__(self, time):

        # 从数据中读取出在时间time下所有在厂外排队的车辆
        queue_cars = Data_acquisition.outFactory_cars(time)
        # 从数据中读取出在时间time下所有叫号还没进厂的车
        ready_cars = Data_acquisition.ready_cars(time)
        # 排队的车 列表
        self.__queue_cars = Tool.car_init(queue_cars, 'out')
        # 小队列初始化，字典 {mat_code:cars_list}
        self.__queue = self.__queue_init(self.__queue_cars)
        # 厂内情况初始化
        self.__inFactory = InFactory(time)
        # 叫号还没进厂的车 列表
        self.__ready_cars = Tool.car_init(ready_cars, 'ready')

    # 排队队列初始化
    def __queue_init(self, cars_list):
        queue = dict()
        for mat in Tool.mat_code:
            queue[mat] = list()
        for car in cars_list:
            queue[car.get_mat_code()].append(car)
        return queue

    def get_inFactory(self):
        return self.__inFactory

    def get_cars_list(self):
        return self.__queue_cars

    def get_queue(self):
        return self.__queue

    def cal_cars_priority(self, now_time):
        time_list = list()
        warehouse_priority = list()
        # 计算每个车辆已等时间的softmax函数
        for car in self.__queue_cars:
            time_list.append((Tool.string_to_datetime(now_time) - Tool.string_to_datetime(car.get_queue_start_time())).total_seconds())
        time = np.array(time_list)
        time = np.exp(time) / sum(np.exp(time))
        # 计算每个仓库优先级的softmax函数
        for warehouse in self.__inFactory.get_warehouse():
            warehouse_priority.append(warehouse.get_priority())
        priority = np.array(warehouse_priority)
        priority = np.exp(priority) / sum(np.exp(priority))
        for i in range(len(self.__queue_cars)):
            count = int()
            weight = 1 / len(self.__queue_cars[i].get_target_warehouse())
            for j in range(len(self.__queue_cars[i].get_target_warehouse())):
                count += self.__queue_cars[i].get_target_warehouse()[j].get_priority() * weight
            self.__queue_cars[i].set_priority(time[i] * count)





