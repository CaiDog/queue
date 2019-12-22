import pandas as pd
import datetime
import demo.setting.SQLConnect as connect

def entry_queue_data_acquisition():
    sql = "SELECT TASK_ID, KIND_CODE, TRUCK_NO, SUB_KIND_NAME, SUB_KIND_CODE, MAT_NAME, MAT_CODE, GATE_CODE, VENDOR_CODE, WAREHOUSE_CODE, WAREHOUSE_NAME, " \
          " NET_WEIGHT, QUEUE_START_TIME, ENTRY_NOTICE_TIME, ENTRY_TIME, FINISH_TIME" \
          " FROM t_disp_entry_queue WHERE QUEUE_START_TIME >= '2019-10-24' AND QUEUE_START_TIME < '2019-11-29' " \
          "AND WAREHOUSE_CODE IS NOT NULL AND QUEUE_START_TIME IS NOT NULL AND ENTRY_NOTICE_TIME IS NOT NULL AND " \
          "ENTRY_TIME IS NOT NULL AND FINISH_TIME IS NOT NULL"

    connect.cursor_dispatch.execute(sql)
    time_data = connect.cursor_dispatch.fetchall()
    time_data = Listize(time_data)
    time_columns = connect.cursor_dispatch.description
    time_columns = Columns_Get(time_columns)
    time_pd = pd.DataFrame(time_data, columns=time_columns)
    return time_pd

def outFactory_cars(time):
    sql = "SELECT TASK_ID, KIND_CODE, TRUCK_NO, SUB_KIND_NAME, SUB_KIND_CODE, MAT_NAME, MAT_CODE, GATE_CODE, VENDOR_CODE, WAREHOUSE_CODE, WAREHOUSE_NAME, " \
          " NET_WEIGHT, QUEUE_START_TIME, ENTRY_NOTICE_TIME, ENTRY_TIME, FINISH_TIME" \
          " FROM t_disp_entry_queue WHERE QUEUE_START_TIME < '{0}' AND ENTRY_NOTICE_TIME > '{1}' " \
          "AND WAREHOUSE_CODE IS NOT NULL AND QUEUE_START_TIME IS NOT NULL AND ENTRY_NOTICE_TIME IS NOT NULL AND " \
          "ENTRY_TIME IS NOT NULL AND FINISH_TIME IS NOT NULL".format(time, time)

    connect.cursor_dispatch.execute(sql)
    time_data = connect.cursor_dispatch.fetchall()
    time_data = Listize(time_data)
    time_columns = connect.cursor_dispatch.description
    time_columns = Columns_Get(time_columns)
    time_pd = pd.DataFrame(time_data, columns=time_columns)
    return time_pd

def inFactory_cars(time):
    sql = "SELECT TASK_ID, KIND_CODE, TRUCK_NO, SUB_KIND_NAME, SUB_KIND_CODE, MAT_NAME, MAT_CODE, GATE_CODE, VENDOR_CODE, WAREHOUSE_CODE, WAREHOUSE_NAME, " \
          " NET_WEIGHT, QUEUE_START_TIME, ENTRY_NOTICE_TIME, ENTRY_TIME, FINISH_TIME" \
          " FROM t_disp_entry_queue WHERE ENTRY_TIME < '{0}' AND FINISH_TIME > '{1}' " \
          "AND WAREHOUSE_CODE IS NOT NULL AND QUEUE_START_TIME IS NOT NULL AND ENTRY_NOTICE_TIME IS NOT NULL AND " \
          "ENTRY_TIME IS NOT NULL AND FINISH_TIME IS NOT NULL".format(time, time)

    connect.cursor_dispatch.execute(sql)
    time_data = connect.cursor_dispatch.fetchall()
    time_data = Listize(time_data)
    time_columns = connect.cursor_dispatch.description
    time_columns = Columns_Get(time_columns)
    time_pd = pd.DataFrame(time_data, columns=time_columns)
    return time_pd

def ready_cars(time):
    sql = "SELECT TASK_ID, KIND_CODE, TRUCK_NO, SUB_KIND_NAME, SUB_KIND_CODE, MAT_NAME, MAT_CODE, GATE_CODE, VENDOR_CODE, WAREHOUSE_CODE, WAREHOUSE_NAME, " \
          " NET_WEIGHT, QUEUE_START_TIME, ENTRY_NOTICE_TIME, ENTRY_TIME, FINISH_TIME" \
          " FROM t_disp_entry_queue WHERE ENTRY_NOTICE_TIME < '{0}' AND ENTRY_TIME > '{1}' " \
          "AND WAREHOUSE_CODE IS NOT NULL AND QUEUE_START_TIME IS NOT NULL AND ENTRY_NOTICE_TIME IS NOT NULL AND " \
          "ENTRY_TIME IS NOT NULL AND FINISH_TIME IS NOT NULL".format(time, time)

    connect.cursor_dispatch.execute(sql)
    time_data = connect.cursor_dispatch.fetchall()
    time_data = Listize(time_data)
    time_columns = connect.cursor_dispatch.description
    time_columns = Columns_Get(time_columns)
    time_pd = pd.DataFrame(time_data, columns=time_columns)
    return time_pd

def read_plan_day():
    sql = " SELECT update_time,plan_date,kind_code,kind_name,sub_kind_name,warehouse_code,warehouse_name,add_weight," \
          "act_weight,status FROM db_data_seience.plan_day_OctNov where status like '修改%'"

    connect.cursor_dispatch.execute(sql)
    time_data = connect.cursor_dispatch.fetchall()
    time_data = Listize(time_data)
    time_columns = connect.cursor_dispatch.description
    time_columns = Columns_Get(time_columns)
    time_pd = pd.DataFrame(time_data, columns=time_columns)
    return time_pd

# def SQLExecute(cursor, sql):
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     data = Listize(data)
#     data_columns = cursor.description
#     data_columns = Columns_Get(data_columns)
#     data_pd = pd.DataFrame(data, columns=data_columns)
#     return data_pd

def Listize(tuple):
    new_list = list()
    for tu in tuple:
        new_list.append(list(tu))
    return new_list

def Columns_Get(columns_info):
    new_columns = list()
    for column in columns_info:
        new_columns.append(column[0])
    return new_columns

def To_Date(data):
    return datetime.datetime.strptime(data, '%Y-%m-%d %H:%M:%S')

# def read_car():
#     sql = "SELECT * FROM t_disp_entry_queue where QUEUE_START_TIME > '2019-10-24' and " \
#           "QUEUE_START_TIME < '2019-11-29' and WAREHOUSE_CODE != ' ' order by QUEUE_START_TIME"
#
#     connect.cursor_Dispatch.execute(sql)
#     time_data = connect.cursor_Dispatch.fetchall()
#     time_data = Listize(time_data)
#     time_columns = connect.cursor_Dispatch.description
#     time_columns = Columns_Get(time_columns)
#     time_pd = pd.DataFrame(time_data, columns=time_columns)
#     return time_pd
#
# def read_schedule():
#     sql = "SELECT * FROM ods_db_trans_t_schedule_plan"
#
#     connect.cursor_Schedule.execute(sql)
#     time_data = connect.cursor_Schedule.fetchall()
#     time_data = Listize(time_data)
#     time_columns = connect.cursor_Schedule.description
#     time_columns = Columns_Get(time_columns)
#     time_pd = pd.DataFrame(time_data, columns=time_columns)
#     return time_pd