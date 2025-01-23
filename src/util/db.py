import mysql.connector


# 数据库操作类
class DBHandler:
    def __init__(self, host="127.0.0.1", port=13306, user='root', password='123456',
                 database='learn_managent', **kwargs):
        # 连接数据库服务器
        self.conn = mysql.connector.connect(host=host, port=port, user=user, password=password,
                                            database=database, **kwargs)
        # 获取游标
        self.cursor = self.conn.cursor(dictionary=True)

    # 执行查询操作
    def query(self, sql, args=None, one=True):
        self.cursor.execute(sql, args)
        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    # 执行增删改操作
    def exec(self, sql, args=None, one=True):
        if one:
            self.cursor.execute(sql, args)
        else:
            self.cursor.executemany(sql, args)
        self.conn.commit()
        return self.cursor.rowcount

    def get_insert_id(self):
        return self.cursor.lastrowid

    def close(self):
        self.cursor.close()
        self.conn.close()
