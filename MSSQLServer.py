from typing import List, Optional
import pyodbc
from utils.message_utils import error, success, info, print_separator

class MSSQLConnection:
    def __init__(self, driver = "{ODBC Driver 13 for SQL Server}", server = "HOME\\GIOAN", database = "master", username = "sa", password = "123456"):
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
    def connect(self):
        try:
            self.connection = pyodbc.connect((
                f"Driver={self.driver};"
                f"Server={self.server};"
                f"Database={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"),
                autocommit=True)
            success("Kết nối thành công!")
        except Exception as e:
            error(f"Lỗi kết nối: {e}")
    def query(self,sql):
        if self.connection is None:
            error("Chưa kết nối đến cơ sở dữ liệu.")
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except Exception as e:
            error(f"Lỗi truy vấn: {e}")
            return None
    def update(self,sql):
        if self.connection is None:
            error("Chưa kết nối đến cơ sở dữ liệu.")
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            success("Cập nhật thành công!")
        except Exception as e:
            error(f"Lỗi cập nhật: {e}")
            return None
    def insert(self,sql):
        if self.connection is None:
            error("Chưa kết nối đến cơ sở dữ liệu.")
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            success("Chèn dữ liệu thành công!")
        except Exception as e:
            error(f"Lỗi chèn dữ liệu: {e}")
            return None
    def delete(self,sql):
        if self.connection is None:
            error("Chưa kết nối đến cơ sở dữ liệu.")
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            success("Xóa dữ liệu thành công!")
        except Exception as e:
            error(f"Lỗi xóa dữ liệu: {e}")
            return None
    def close(self):
        if self.connection:
            self.connection.close()
            success("Đóng kết nối thành công!")
        else:
            info("Kết nối đã được đóng hoặc chưa được mở.")
    def cursor(self):
        if self.connection is None:
            error("Chưa kết nối đến cơ sở dữ liệu.")
            return None
        try:
            return self.connection.cursor()
        except Exception as e:
            error(f"Lỗi tạo con trỏ: {e}")
            return None
    def commit(self):
        if self.connection is None:
            error("Chưa kết nối đến cơ sở dữ liệu.")
            return None
        try:
            self.connection.commit()
            success("Commit thành công!")
        except Exception as e:
            error(f"Lỗi commit: {e}")
            return None
if __name__ == "__main__":
    # Sử dụng class MSSQLConnectionL để kết nối và thực hiện các thao tác
    conn = MSSQLConnection(database="master")
    conn.connect()
    dt = conn.query("SELECT * FROM [dbo].[user]")
    print(dt)
    conn.close()