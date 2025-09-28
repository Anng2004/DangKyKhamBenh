import pyodbc
from utils.message_utils import error, success, info, print_separator

CONN_STR = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"                   
    "Database=DangKyKhamBenh;"           
    "UID=SA;"                            
    "PWD=Admin@123;"                     
    "TrustServerCertificate=yes;"
)

MASTER_CONN_STR = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;" 
    "Database=master;"
    "UID=SA;"
    "PWD=Admin@123;"
    "TrustServerCertificate=yes;"
)

def create_database_if_not_exists():
    try:
        import re
        db_match = re.search(r'Database=([^;]+)', CONN_STR)
        if not db_match:
            error("Không tìm thấy tên database trong connection string")
            return False
        
        database_name = db_match.group(1)
        print(f"🔍 Kiểm tra database: {database_name}")
        
        conn = pyodbc.connect(MASTER_CONN_STR)
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

def get_conn():
    try:
        return pyodbc.connect(CONN_STR)
    except Exception as e:
        error(f"Lỗi kết nối database: {e}")
        raise

def init_db(seed: bool = True) -> None:
    if not create_database_if_not_exists():
        return False
    
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='user' AND xtype='U')
    CREATE TABLE [user] (
        user_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        username NVARCHAR(50) UNIQUE NOT NULL,
        role NVARCHAR(20) NOT NULL,
        pass NVARCHAR(50) NOT NULL,
        created_at DATETIME DEFAULT GETDATE()
    );
    """)

    cur.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='PhongKham' AND xtype='U')
    CREATE TABLE PhongKham (
        PK_ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        MaPhong NVARCHAR(20) UNIQUE NOT NULL,
        TenPhong NVARCHAR(100) NOT NULL,
        BS_ID UNIQUEIDENTIFIER NULL,
        user_created UNIQUEIDENTIFIER,
        created_at DATETIME DEFAULT GETDATE()
    );
    """)

    cur.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='DM_DichVuKyThuat' AND xtype='U')
    CREATE TABLE DM_DichVuKyThuat (
        dv_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        MaDichVu NVARCHAR(20) UNIQUE NOT NULL,
        TenDichVu NVARCHAR(100) NOT NULL,
        GiaDichVu INT NOT NULL,
        user_created UNIQUEIDENTIFIER,
        created_at DATETIME DEFAULT GETDATE()
    );
    """)

    cur.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='BenhNhan' AND xtype='U')
    CREATE TABLE BenhNhan (
        BN_ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        PID NVARCHAR(8) UNIQUE NOT NULL,
        HoTen NVARCHAR(100) NOT NULL,
        GioiTinh NVARCHAR(10) NOT NULL,
        NgaySinh DATE NULL,
        NamSinh INT,
        SoCCCD NVARCHAR(20) UNIQUE,
        SoCMND NVARCHAR(20),
        PhuongXa NVARCHAR(200),
        Tinh NVARCHAR(50),
        user_created UNIQUEIDENTIFIER,
        created_at DATETIME DEFAULT GETDATE()
    );
    """)

    cur.execute("""
    IF COL_LENGTH('BenhNhan', 'NgaySinh') IS NULL
        ALTER TABLE BenhNhan ADD NgaySinh DATE NULL;
    """)

    cur.execute("""
    IF COL_LENGTH('BenhNhan', 'PID') IS NULL
        ALTER TABLE BenhNhan ADD PID NVARCHAR(8) NULL;
    """)

    cur.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='BacSi' AND xtype='U')
    CREATE TABLE BacSi (
        BS_ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        MaBacSi NVARCHAR(20) UNIQUE NOT NULL,
        HoTen NVARCHAR(100) NOT NULL,
        ChuyenKhoa NVARCHAR(100),
        SoDienThoai NVARCHAR(15),
        Email NVARCHAR(100),
        user_created UNIQUEIDENTIFIER,
        created_at DATETIME DEFAULT GETDATE()
    );
    """)

    cur.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='TiepNhan' AND xtype='U')
    CREATE TABLE TiepNhan (
        TiepNhan_ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        MaTiepNhan NVARCHAR(20) UNIQUE NOT NULL,
        BN_ID UNIQUEIDENTIFIER NOT NULL,
        LyDoKham NVARCHAR(200),
        Dv_ID UNIQUEIDENTIFIER NULL,
        PK_ID UNIQUEIDENTIFIER NULL,
        BS_ID UNIQUEIDENTIFIER NULL,
        user_created UNIQUEIDENTIFIER,
        created_at DATETIME DEFAULT GETDATE()
    );
    """)

    
    cur.execute("""
    IF EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_PhongKham_BacSi')
    ALTER TABLE PhongKham DROP CONSTRAINT FK_PhongKham_BacSi
    """)
    
    cur.execute("""
    IF EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_TiepNhan_BenhNhan')
    ALTER TABLE TiepNhan DROP CONSTRAINT FK_TiepNhan_BenhNhan
    """)
    
    cur.execute("""
    IF EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_TiepNhan_DichVu')
    ALTER TABLE TiepNhan DROP CONSTRAINT FK_TiepNhan_DichVu
    """)
    
    cur.execute("""
    IF EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_TiepNhan_PhongKham')
    ALTER TABLE TiepNhan DROP CONSTRAINT FK_TiepNhan_PhongKham
    """)
    
    cur.execute("""
    IF EXISTS (SELECT * FROM sys.foreign_keys WHERE name = 'FK_TiepNhan_BacSi')
    ALTER TABLE TiepNhan DROP CONSTRAINT FK_TiepNhan_BacSi
    """)
    
    cur.execute("""
    ALTER TABLE PhongKham ADD CONSTRAINT FK_PhongKham_BacSi 
    FOREIGN KEY (BS_ID) REFERENCES BacSi(BS_ID) ON DELETE NO ACTION
    """)
    
    cur.execute("""
    ALTER TABLE TiepNhan ADD CONSTRAINT FK_TiepNhan_BenhNhan
    FOREIGN KEY (BN_ID) REFERENCES BenhNhan(BN_ID) ON DELETE NO ACTION
    """)
    
    cur.execute("""
    ALTER TABLE TiepNhan ADD CONSTRAINT FK_TiepNhan_DichVu
    FOREIGN KEY (Dv_ID) REFERENCES DM_DichVuKyThuat(dv_id) ON DELETE NO ACTION
    """)
    
    cur.execute("""
    ALTER TABLE TiepNhan ADD CONSTRAINT FK_TiepNhan_PhongKham
    FOREIGN KEY (PK_ID) REFERENCES PhongKham(PK_ID) ON DELETE NO ACTION
    """)
    
    cur.execute("""
    ALTER TABLE TiepNhan ADD CONSTRAINT FK_TiepNhan_BacSi
    FOREIGN KEY (BS_ID) REFERENCES BacSi(BS_ID) ON DELETE NO ACTION
    """)

    if seed:
        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM [user] WHERE username = 'admin')
        BEGIN
            DECLARE @admin_id UNIQUEIDENTIFIER = NEWID()
            INSERT INTO [user](user_id, username, role, pass) 
            VALUES (@admin_id, 'admin', 'ADMIN', 'admin')
            
            -- Tạo phòng khám và dịch vụ mặc định
            INSERT INTO PhongKham(MaPhong, TenPhong, user_created) 
            VALUES ('PK001','Phòng Nội tổng quát', @admin_id)
            
            INSERT INTO DM_DichVuKyThuat(MaDichVu, TenDichVu, GiaDichVu, user_created) 
            VALUES ('DV001','Khám tổng quát', 150000, @admin_id)
        END
        """)

    conn.commit()
    conn.close()
    return True


if __name__ == "__main__":
    print_separator(60,"=")
    print("     🏥 KHỞI TẠO DATABASE - HỆ THỐNG QUẢN LÝ KHÁM BỆNH")
    try:
        success = init_db(seed=True)
        if success:
            success("Khởi tạo database thành công!")
        else:
            error("Khởi tạo database thất bại!")
    except Exception as e:
        error(f" Lỗi: {e}")
