import demo.setting.Tools as Tool
class Warehouse(object):

    """
    仓库模块：记录正在仓库卸货的车辆
    flag1：工作上限取的是mode、max还是minorMax
    flag2：合理工作强度取工作上限的百分之多少
    """
    def __init__(self, warehouse_code, mat_list, cars, flag1, flag2):
        self.__warehouse_code = warehouse_code  # 仓库编码
        self.__mat_list = mat_list  # 物料   可能是列表，也可能是一个
        self.__cars = cars   # dict {task_id:Car} 该仓库签到过的所有车辆
        self.__limit = int(Tool.warehouse_limit[Tool.warehouse_limit['warehouse_code'] == warehouse_code][flag1])  # 仓库工作上限
        self.__act = len(self.__cars)    # 仓库活跃度，也就是正在工作车辆数
        self.__rea = int(self.__limit * flag2)  # 仓库合理工作强度

    def get_warehouse_code(self):
        return self.__warehouse_code

    def get_cars(self):
        return self.__cars

    def get_mat_list(self):
        return self.__mat_list

    def get_limit(self):
        return self.__limit

    def get_act(self):
        return self.__act

    def get_rea(self):
        return self.__rea


