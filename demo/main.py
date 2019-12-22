import demo.OutFactory as OutFactory
import demo.setting.Tools as Tool


def match():
    pass

time = '2019-10-25 00:00:00'
plan_day = Tool.init_plan_day()
outFactory = OutFactory.OutFactory(time)
for i in range(500):
    time = Tool.time_window(time, 120)

