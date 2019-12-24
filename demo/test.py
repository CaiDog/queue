import pandas as pd

import demo.setting.Data_acquisition as Data_acquisition
import demo.setting.Tools as Tool
import ssl
import demo.OutFactory as OutFactory
import datetime


now_time = '2019-10-25 00:00:00'
plan_day = Tool.init_plan_day()
data = Data_acquisition.entry_queue_data_acquisition()
out_factory = OutFactory.OutFactory(now_time)
out_factory.get_inFactory().cal_mat_priority(now_time)
out_factory.cal_cars_priority(now_time)
for warehouse in out_factory.get_inFactory().get_warehouse():
    for car in warehouse.get_cars():
        car.set_finish_time(Tool.string_to_datetime(car.get_entry_time()) + datetime.timedelta(seconds=warehouse.get_unloadTime()))
for car in out_factory.get_ready_cars():
    car.

for i in range(1, 1000):
    time = Tool.time_window(now_time, i * 120)

print(out_factory)
