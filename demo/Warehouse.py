import demo.setting.Tools as Tool
class Warehouse(object):

    """
    仓库模块：记录正在仓库卸货的车辆
    flag1：工作上限取的是mode、max还是minorMax
    flag2：合理工作强度取工作上限的百分之多少
    """
    def __init__(self, warehouse_code, mat_code, cars, flag1, flag2):
        self.__warehouse_code = warehouse_code  # 仓库编码
        self.__mat_code = mat_code  # 物料号   可能是列表，也可能是一个
        self.__cars = cars   # dict {task_id:Car} 该仓库签到过的所有车辆
        self.__limit = int(Tool.warehouse_limit[Tool.warehouse_limit['warehouse_code'] == warehouse_code][flag1])  # 仓库工作上限
        self.__act = len(self.__cars)    # 仓库活跃度，也就是正在工作车辆数
        self.__rea = int(self.__limit * flag2)  # 仓库合理工作强度
        self.__rest = 0       # 仓库需求剩余未完成量
        self.__last_time = 0 # 上一次plan_day修改时间，秒
        self.__priority = None  # 优先级

    def get_warehouse_code(self):
        return self.__warehouse_code

    def get_cars(self):
        return self.__cars

    def get_mat_code(self):
        return self.__mat_code

    def get_limit(self):
        return self.__limit

    def get_act(self):
        return self.__act

    def get_rea(self):
        return self.__rea

    def set_rest(self, rest):
        self.__rest = rest

    def get_rest(self):
        return self.__rest

    def get_last_time(self):
        return self.__last_time

    def set_priority(self, priority):
        self.__priority = priority

