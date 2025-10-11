from typing import List, Optional
import pyodbc
from utils.message_utils import error, success, info, print_separator
from DKKB_mvc import AbcUser, AbcPhongKham, AbcBacSi, AbcDichVu, AbcBenhNhan, AbcTiepNhan

class MSSQLConnection:
    def __init__(self, driver = "{ODBC Driver 13 for SQL Server}", server = "HOME\GIOAN", database = "DangKyKhamBenh", username = "SA", password = "123456"):
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f"Driver={self.driver};"
                f"Server={self.server};"
                f"Database={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
                "TrustServerCertificate=yes;"
            )
            success("Kết nối thành công!")
        except Exception as e:
            error(f"Lỗi kết nối: ", e)
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
            error(f"Lỗi truy vấn: ", e)
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
            error(f"Lỗi cập nhật: ", e)
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
            error(f"Lỗi chèn dữ liệu: ", e)
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
            error(f"Lỗi xóa dữ liệu: ", e)
            return None
    def close(self):
        if self.connection:
            self.connection.close()
            success("Đóng kết nối thành công!")
        else:
            info("Kết nối đã được đóng hoặc chưa được mở.")
if __name__ == "__main__":
    # Sử dụng class MSSQLConnectionL để kết nối và thực hiện các thao tác
    conn = MSSQLConnection(database="DangKyKhamBenh")
    conn.connect()
    dt = conn.query("SELECT * FROM [dbo].[user]")
    print(dt)
    conn.close()
class InitDB:
    @staticmethod
    def create_database_if_not_exists():
        try:
            import re
            db_match = re.search(r'Database=([^;]+)',database_name= "DangKyKhamBenh")
            if not db_match:
                error("Không tìm thấy tên database trong connection string")
                return False
            
            database_name = db_match.group(1)
            print(f"🔍 Kiểm tra database: {database_name}")
            
            conn = MSSQLConnection(database="master")
            conn.autocommit = True
            cur = conn.cursor()
            
            cur.execute("SELECT name FROM sys.databases WHERE name = ?", (database_name,))
            if not cur.fetchone():
                print(f"🔧 Tạo database {database_name}...")
                cur.execute(f"CREATE DATABASE [{database_name}]")
                success("Database được tạo thành công!")
            else:
                info(f"Database {database_name} đã tồn tại")
            
            conn.close()
            return True
        except Exception as e:
            error(f"Lỗi khi tạo database: {e}")
            return False

    @staticmethod
    def get_conn():
        try:
            return MSSQLConnection(database="DangKyKhamBenh")
        except Exception as e:
            error(f"Lỗi kết nối database: {e}")
            raise

    @staticmethod
    def init_db(seed: bool = True) -> None:
        if not InitDB.create_database_if_not_exists():
            return False
        
        conn = InitDB.get_conn()
        # Tiếp tục với việc khởi tạo bảng và dữ liệu mẫu nếu cần thiết
        conn.close()
