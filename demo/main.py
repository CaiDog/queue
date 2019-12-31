import pandas as pd
import demo.setting.Data_acquisition as Data_acquisition
import demo.setting.Tools as Tool
import demo.OutFactory as OutFactory
import datetime


now_time = '2019-10-25 00:00:00'

data = Data_acquisition.entry_queue_data_acquisition()
out_factory = OutFactory.OutFactory(now_time)
# out_factory.get_inFactory().cal_mat_priority(now_time)
# out_factory.cal_cars_priority(now_time)
# for warehouse in out_factory.get_inFactory().get_warehouse():
#     for car in warehouse.get_cars():
#         car.set_finish_time(Tool.datetime_to_string(Tool.string_to_datetime(car.get_entry_time()) + datetime.timedelta(seconds=warehouse.get_unloadTime())))
# for car in out_factory.get_ready_cars():
#     for warehouse in out_factory.get_inFactory().get_warehouse():
#         if car.get_target_warehouse() == warehouse.get_warehouse_code():
#             car.set_entry_time(Tool.datetime_to_string(Tool.string_to_datetime(car.get_notice_time()) + datetime.timedelta(seconds=warehouse.get_preTime())))
#             car.set_finish_time(Tool.datetime_to_string(Tool.string_to_datetime(car.get_entry_time()) + datetime.timedelta(seconds=warehouse.get_unloadTime())))

pre_time = now_time

for i in range(1, 10):
    time = Tool.time_window(pre_time, i * Tool.interval)    # 更新时间
    new_cars = data[(data['QUEUE_START_TIME'] >= pre_time) & (data['QUEUE_START_TIME'] <= time)]    # 读取在这个时间段新来的车辆
    queue_cars = Tool.car_init(new_cars, 'out')     # 初始化排队车辆，形成列表
    out_factory.update(time, queue_cars)    # 更新
    pre_time = time




print(out_factory)

