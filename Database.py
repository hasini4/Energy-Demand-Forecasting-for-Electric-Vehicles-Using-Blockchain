import pymysql

def connect():
    con=pymysql.connect(host="localhost",user="root",password="root",database="e_demand",charset="utf8")
    return con
