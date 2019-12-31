import demo.setting.Tools as Tool
import datetime


class Warehouse(object):
    """
    仓库模块：记录正在仓库卸货的车辆
    flag1：工作上限取的是mode、max还是minorMax
    flag2：合理工作强度取工作上限的百分之多少
    """
    def __init__(self, warehouse_code, mat_list, cars_list, flag1, flag2, flag3):
        self.__warehouse_code = warehouse_code  # 仓库编码
        self.__mat_list = mat_list  # 物料   可能是列表，也可能是一个
        self.__limit = int(Tool.warehouse_limit[Tool.warehouse_limit['warehouse_code'] == warehouse_code][flag1])  # 仓库工作上限
        self.__unloadTime = int(Tool.warehouse_unloadTime[Tool.warehouse_unloadTime['warehouse_code'] == warehouse_code][flag3])
        self.__preTime = int(Tool.warehouse_preTime[Tool.warehouse_preTime['warehouse_code'] == warehouse_code]['preparation_time'])
        self.__cars_list = self.cars_init(cars_list)  # dict {task_id:Car} 该仓库工作的所有车辆    update
        self.__act = len(self.__cars_list)    # 仓库活跃度，也就是正在工作车辆数 update
        self.__rea = int(self.__limit * flag2 + 0.5)  # 仓库合理工作强度

    def cars_init(self, cars_list):
        new_cars_list = cars_list
        for car in new_cars_list:
            car.set_finish_time(Tool.datetime_to_string(Tool.string_to_datetime(car.get_entry_time()) + datetime.timedelta(seconds=self.__unloadTime)))
            if car.get_finish_time() < '2019-10-25 00:00:00':
                car.set_finish_time('2019-10-25 00:00:00')
        return new_cars_list

    def get_warehouse_code(self):
        return self.__warehouse_code

    def get_cars(self):
        return self.__cars_list

    def get_mat_list(self):
        return self.__mat_list

    def get_limit(self):
        return self.__limit

    def get_act(self):
        return self.__act

    def get_rea(self):
        return self.__rea

    def set_mat_priority(self, priority):
        for i in range(len(self.__mat_list)):
            self.__mat_list[i].set_priority(priority[i])

    def get_unloadTime(self):
        return self.__unloadTime

    def get_preTime(self):
        return self.__preTime

    def update(self, time, car_list):
        # 删除已经到结束时间的车辆
        temp_list = self.__cars_list
        for car in temp_list:
            if car.get_finish_time() < time:
                self.__cars_list.remove(car)
        # 加入新进厂的车辆
        for car in car_list:
            self.__cars_list.append(car)
        # 修改仓库活跃度
        self.__act = len(self.__cars_list)




