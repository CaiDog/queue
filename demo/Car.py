import demo.setting.Tools as Tool


class Car(object):

    """
    车辆模块，用于记录车辆的基本信息
    """

    def __init__(self, queue_item):
        self.__task_id = queue_item['TASK_ID']  # 任务号
        self.__mat_code = queue_item['MAT_CODE']    # 物料号
        if self.__mat_code == '11002000010000':
            self.__sub_kind_name = queue_item['SUB_KIND_NAME']  # 小品种名
        else:
            self.__sub_kind_name = None
        self.__start_time = queue_item['QUEUE_START_TIME']  # 签到时间
        self.__notice_time = None   # 叫号时间
        self.__entry_time = None    # 进厂时间
        self.__finish_time = None   # 出厂时间
        self.__target_warehouse = None  # 目标仓库
        self.__priority = None  # 优先级

    def init_target_warehouse(self, queue_item):
        self.__target_warehouse = queue_item['WAREHOUSE_CODE']

    def init_notice_time(self, queue_item):
        self.__notice_time = queue_item['ENTRY_NOTICE_TIME']

    def init_entry_time(self, queue_item):
        self.__entry_time = queue_item['ENTRY_TIME']

    # 获取车辆任务号
    def get_task_id(self):
        return self.__task_id

    def get_mat_code(self):
        return self.__mat_code

    def get_sub_kind_name(self):
        return self.__sub_kind_name

    # 获取签到时间
    def get_queue_start_time(self):
        return self.__start_time

    def get_target_warehouse(self):
        return self.__target_warehouse

    def set_target_warehouse(self, warehouse_list):
        self.__target_warehouse = warehouse_list

    # 获取叫号时间
    def get_notice_time(self):
        return self.__notice_time

    # 设置叫号时间
    def set_notice_time(self, time):
        self.__notice_time = time

    # 获取进厂时间
    def get_entry_time(self):
        return self.__entry_time

    # 设置进厂时间
    def set_entry_time(self, time):
        self.__entry_time = time

    # 获取出厂时间
    def get_finish_time(self):
        return self.__finish_time

    # 设置出厂时间
    def set_finish_time(self, time):
        self.__finish_time = time

    # 获取厂外等待时间
    def get_wait_time(self):
        return Tool.string_to_datetime(self.__notice_time)-Tool.string_to_datetime(self.__entry_time)

    # 计算优先级
    def set_priority(self, priority):
        self.__priority = priority

    def get_priority(self):
        return self.__priority

