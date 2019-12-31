# import pandas as pd
#
# import demo.setting.Data_acquisition as Data_acquisition
import demo.setting.Tools as Tool
# import ssl
# import demo.OutFactory as OutFactory
# import datetime
import numpy as np
import sklearn.preprocessing as preprocessing
import math




a = int((Tool.string_to_datetime('2019-10-25 11:00:00') - Tool.string_to_datetime('2019-10-25 10:00:00')).total_seconds())
print(a)

