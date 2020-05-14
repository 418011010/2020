#-*-coding:utf-8-*-
import multiprocessing
import baostock as bs
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import mysql.connector
pymysql.install_as_MySQLdb()

#多线程导入
def main():
    pool = multiprocessing.Pool(processes=4)
    result = []
    for num in range(400, 500):
        stcode = ('sz.' + "{:0>6d}".format(num))
        result.append(pool.apply_async(hello, (stcode, )))
    pool.close()
    pool.join()
    for res in result:
        print(res.get())
    print("all done.")
    #bs.logout()


def hello(stc):
    lg = bs.login()
    #print('login respond error_code:' + lg.error_code)
    #print('login respond  error_msg:' + lg.error_msg)
    rs = bs.query_history_k_data_plus(stc,
                                      "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                                      start_date='2019-01-01', end_date='2020-04-26',
                                      frequency="d", adjustflag="3")  # frequency="d"取日k线，adjustflag="3"默认不复权
    print(stc + ' query_history_k_data_plus respond error_code:' + rs.error_code)
    print(stc + ' query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    #### 结果集输出到csv文件 ####
    #result.to_csv("D:/history_k_data.csv", encoding="gbk", index=False)
    #print(data_list)

    if data_list:
        ce = create_engine('mysql+mysqlconnector://root:coship@localhost:3306/stock?charset=utf8')
        result.to_sql('stock_{}'.format(stc).lower(), ce, if_exists='append', index=False)
    return "done " + stc


if __name__ == "__main__":
    main()

