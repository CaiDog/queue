import pandas as pd

import demo.setting.Data_acquisition as Data_acquisition
import demo.setting.Tools as Tool
import ssl
import demo.OutFactory as OutFactory

out_factory = OutFactory.OutFactory('2019-10-25 00:00:00')
out_factory.cal_cars_priority()
print(out_factory)