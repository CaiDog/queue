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
        queue_cars = Data_acquisition.queue_cars(time)
        # 从数据中读取出在时间time下所有叫号还没进厂的车
        ready_cars = Data_acquisition.ready_cars(time)
        # 排队的车 列表
        self.__queue_cars = Tool.car_init(queue_cars, 'out')    # update
        # 小队列初始化，字典 {mat_code:cars_list}
        # self.__queue = self.__queue_init(self.__queue_cars)
        # 厂内情况初始化
        self.__inFactory = InFactory(time)
        # 叫号还没进厂的车 列表
        self.__ready_cars = self.ready_cars_init(Tool.car_init(ready_cars, 'ready'))
        # plan_day
        self.plan_day = Tool.init_plan_day()

    # 排队队列初始化
    # def __queue_init(self, cars_list):
    #     queue = dict()
    #     for mat in Tool.mat_code:
    #         queue[mat] = list()
    #     for car in cars_list:
    #         queue[car.get_mat_code()].append(car)
    #     return queue
    def ready_cars_init(self, cars_list):
        # 准备车辆也确定了进厂时间和离厂时间
        new_cars_list = cars_list
        for car in new_cars_list:
            for warehouse in self.__inFactory.get_warehouse():
                if car.get_target_warehouse() == warehouse.get_warehouse_code():
                    car.set_entry_time(Tool.datetime_to_string(
                        Tool.string_to_datetime(car.get_notice_time()) + datetime.timedelta(
                            seconds=warehouse.get_preTime())))
                    if car.get_entry_time() < '2019-10-25 00:00:00':
                        car.set_entry_time('2019-10-25 00:00:00')
                    car.set_finish_time(Tool.datetime_to_string(
                        Tool.string_to_datetime(car.get_entry_time()) + datetime.timedelta(
                            seconds=warehouse.get_unloadTime())))
        return new_cars_list


    def get_inFactory(self):
        return self.__inFactory

    def get_queue_cars(self):
        return self.__queue_cars

    def get_ready_cars(self):
        return self.__ready_cars

    # def get_queue(self):
    #     return self.__queue

    def cal_cars_priority(self, now_time):
        time_list = list()
        mat_priority = list()
        # 计算每个车辆已等时间的softmax函数
        for car in self.__queue_cars:
            time_list.append(int((Tool.string_to_datetime(now_time) - Tool.string_to_datetime(car.get_queue_start_time())).total_seconds()))
        time_result = Tool.softmax(time_list)
        # 计算每个仓库中品种优先级的softmax函数
        for warehouse in self.__inFactory.get_warehouse():
            for mat in warehouse.get_mat_list():
                mat_priority.append(mat.get_priority())
        priority_result = Tool.softmax(mat_priority)
        # 计算每辆车得优先级
        for i in range(len(self.__queue_cars)):
            count = int()   # 用于保存多个仓库的优先级*权重之和
            # 遍历car的每个目的仓库
            for warehouse1 in self.__queue_cars[i].get_target_warehouse():
                index = 0
                # 遍历厂内所有仓库，目的是找出仓库内品种的优先级
                for warehouse2 in self.__inFactory.get_warehouse():
                    # 如果相等则匹配到了
                    if warehouse1 == warehouse2.get_warehouse_code():
                        # 遍历仓库内所有品种，目的是找出仓库内和车辆相同的品种
                        for mat in warehouse2.get_mat_list():
                            # 物料名和小品种要都相等才能确定
                            if mat == self.__queue_cars[i].get_mat_code() \
                                    and self.__queue_cars[i].get_sub_kind_name() == mat.get_sub_kind_name():
                                count += priority_result[index]
                                break
                            index += 1
                        break
                    else:
                        index += len(warehouse2.get_mat_list())
            x = time_result[i] * (count / len(self.__queue_cars[i].get_target_warehouse()))
            self.__queue_cars[i].set_priority(x)
            print(x)

    # 叫号函数   关键！！！！！
    def call(self, time):
        car_list = list()   # 存储本次叫号的车辆
        pre_time = Tool.datetime_to_string(Tool.string_to_datetime(time) - datetime.timedelta(seconds=Tool.interval))
        # 选取上一个时间段的plan_day
        plan_day = self.plan_day[(self.plan_day['update_time'] >= pre_time) & (self.plan_day['update_time'] <= time)]
        # 更新每个仓库内的每个原料的更新时间和剩余未完成量
        for warehouse in self.__inFactory.get_warehouse():
            for mat in warehouse.get_mat_list():
                if mat.get_mat_code() == '11002000010000':
                    mat_plan_day = plan_day[(plan_day['sub_kind_name'] == mat.get_sub_kind_name()) &
                                            (plan_day['warehouse_code'] == warehouse.get_warehouse_code())]['add_weight'].tolist()
                else:
                    mat_plan_day = plan_day[(plan_day['kind_code'] == mat.get_mat_code()) &
                                            (plan_day['warehouse_code'] == warehouse.get_warehouse_code())]['add_weight'].tolist()
                if len(mat_plan_day) == 0:
                    continue
                add_weight = int(mat_plan_day[-1])
                mat.update(time, add_weight - mat.get_sum())
        self.__inFactory.cal_mat_priority(time)     # 计算每个原料的优先级
        self.cal_cars_priority(time)    # 计算每辆车的优先级
        self.__queue_cars.sort(key=lambda x: x.get_priority())

        # for car in self.__queue_cars:

        # for car in self.__queue_cars:
        #     # 外购废钢看小品名
        #     if car.get_mat_code() == '11002000010000':
        #         for warehouse in self.__inFactory.get_warehouse():
        #             for mat in warehouse.get_mat_list():
        #                 if mat.get_sub_kind_name() == car.get_sub_kind_name():
        #                     if mat.get_rest() > 0:
        #                         car.set_notice_time(time)
        #                         car.set_entry_time(Tool.datetime_to_string
        #                                            (Tool.string_to_datetime(car.get_notice_time()) + datetime.timedelta
        #                                            (seconds=warehouse.get_preTime())))
        #                         car.set_finish_time(Tool.datetime_to_string
        #                                             (Tool.string_to_datetime(car.get_entry_time)) + datetime.timedelta
        #                         (seconds=warehouse.get_unloadTime()))
        #                         mat.add_sum()
        #                         mat.sub_rest()
        #                         car_list.append(car)
        #     # 其他看物料名
        #     else:
        #         for warehouse in self.__inFactory.get_warehouse():
        #             for mat in warehouse.get_mat_list():
        #                 if mat.get_mat_code() == car.get_mat_code():
        #                     if mat.get_rest() > 0:
        #                         car.set_notice_time(time)
        #                         car.set_entry_time(Tool.datetime_to_string
        #                                            (Tool.string_to_datetime(car.get_notice_time()) + datetime.timedelta
        #                                            (seconds=warehouse.get_preTime())))
        #                         car.set_finish_time(Tool.datetime_to_string
        #                                             (Tool.string_to_datetime(car.get_entry_time)) + datetime.timedelta
        #                         (seconds=warehouse.get_unloadTime()))
        #                         mat.add_sum()
        #                         mat.sub_rest()
        #                         car_list.append(car)
        return car_list

    def update(self, time, car_list):
        notice_car = self.call(time)
        # 删除队列中刚叫号的车辆
        for car in notice_car:
            self.__queue_cars.remove(car)
        # 新叫号的车辆
        for car in notice_car:
            self.__ready_cars.append(car)
        # 加入新签到的车辆
        for car in car_list:
            self.__queue_cars.append(car)
        # 删除已进厂的车辆
        entry_cars = list()
        temp_list = self.__ready_cars
        for car in temp_list:
            if car.get_entry_time() < time:
                self.__ready_cars.remove(car)
                entry_cars.append(car)
        self.__inFactory.update(time, entry_cars)







