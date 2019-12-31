import demo.setting.Tools as Tool


class Material(object):

    """
    原料模块
    """

    def __init__(self, mat_code, sub_kind_name):
        self.__mat_code = mat_code          # 物料号
        self.__sub_kind_name = sub_kind_name    #小品名 有小品名的看小品名
        self.__last_time = '2019-10-25 00:00:00'     # 上次plan_day修改的时间  update
        self.__rest = 0  # 剩余未完成量               # update
        self.__sum = 0   # 全天累计量
        self.__priority = None  # 优先级

    def set_last_time(self, last_time):
        self.__last_time = last_time

    def get_last_time(self):
        return self.__last_time

    def sub_rest(self):
        self.__rest -= 1

    def get_rest(self):
        return self.__rest

    def get_mat_code(self):
        return self.__mat_code

    def get_sub_kind_name(self):
        return self.__sub_kind_name

    def set_priority(self, priority):
        self.__priority = priority

    def get_priority(self):
        return self.__priority

    def get_sum(self):
        return self.__sum

    def add_sum(self):
        self.__sum += 1

    def update(self, last_time, rest):
        self.__last_time = last_time
        self.__rest = rest
