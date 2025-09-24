import pyodbc

# Cấu hình kết nối SQL Server (bạn chỉnh DSN / SERVER / DBNAME / DRIVER theo máy mình)
CONN_STR = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"       # hoặc tên server ví dụ: DESKTOP-ABC\\SQLEXPRESS
    "Database=DangKyKhamBenh;"           # tên database
    "UID=SA;"                      # user SQL Server
    "PWD=Admin@123;"                  # mật khẩu
    "TrustServerCertificate=yes;"
)

def get_conn():
    return pyodbc.connect(CONN_STR)

def init_db(seed: bool = True) -> None:
    conn = get_conn()
    cur = conn.cursor()

    # Tạo bảng nếu chưa có
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
        NamSinh INT,
        SoCCCD NVARCHAR(20) UNIQUE,
        SoCMND NVARCHAR(20),
        PhuongXa NVARCHAR(50),
        Tinh NVARCHAR(50),
        user_created UNIQUEIDENTIFIER,
        created_at DATETIME DEFAULT GETDATE()
    );
    """)

    # Thêm cột NgaySinh cho BenhNhan nếu chưa có
    cur.execute("""
    IF COL_LENGTH('BenhNhan', 'NgaySinh') IS NULL
        ALTER TABLE BenhNhan ADD NgaySinh DATE NULL;
    """)

    # Thêm cột PID cho BenhNhan nếu chưa có
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

    # Remove PK_ID column from BacSi if exists (old relationship)
    cur.execute("""
    IF COL_LENGTH('BacSi', 'PK_ID') IS NOT NULL
    BEGIN
        -- Drop foreign key constraint if exists
        DECLARE @constraint_name NVARCHAR(128)
        SELECT @constraint_name = name 
        FROM sys.foreign_keys 
        WHERE parent_object_id = OBJECT_ID('BacSi') 
        AND referenced_object_id = OBJECT_ID('PhongKham')
        
        IF @constraint_name IS NOT NULL
        BEGIN
            DECLARE @sql NVARCHAR(MAX) = 'ALTER TABLE BacSi DROP CONSTRAINT ' + @constraint_name
            EXEC sp_executesql @sql
        END
        
        -- Drop the column
        ALTER TABLE BacSi DROP COLUMN PK_ID
    END
    """)

    # Add BS_ID to PhongKham if not exists (new relationship)
    cur.execute("""
    IF COL_LENGTH('PhongKham', 'BS_ID') IS NULL
    BEGIN
        ALTER TABLE PhongKham ADD BS_ID UNIQUEIDENTIFIER
        ALTER TABLE PhongKham ADD CONSTRAINT FK_PhongKham_BacSi 
        FOREIGN KEY (BS_ID) REFERENCES BacSi(BS_ID)
    END
    """)

    cur.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='TiepNhan' AND xtype='U')
    CREATE TABLE TiepNhan (
        TiepNhan_ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        MaTiepNhan NVARCHAR(20) UNIQUE NOT NULL,
        BN_ID UNIQUEIDENTIFIER NOT NULL FOREIGN KEY REFERENCES BenhNhan(BN_ID) ON DELETE CASCADE,
        LyDoKham NVARCHAR(200),
        Dv_ID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES DM_DichVuKyThuat(dv_id),
        PK_ID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES PhongKham(PK_ID),
        BS_ID UNIQUEIDENTIFIER FOREIGN KEY REFERENCES BacSi(BS_ID),
        user_created UNIQUEIDENTIFIER,
        created_at DATETIME DEFAULT GETDATE()
    );
    """)

    # Thêm cột BS_ID cho TiepNhan nếu chưa có
    cur.execute("""
    IF COL_LENGTH('TiepNhan', 'BS_ID') IS NULL
        ALTER TABLE TiepNhan ADD BS_ID UNIQUEIDENTIFIER 
        FOREIGN KEY REFERENCES BacSi(BS_ID);
    """)

    if seed:
        # Insert initial admin user and get its UUID
        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM [user])
        BEGIN
            DECLARE @admin_id UNIQUEIDENTIFIER = NEWID()
            INSERT INTO [user](user_id, username, role, pass) VALUES (@admin_id, 'admin','ADMIN','admin')
            
            INSERT INTO PhongKham(MaPhong, TenPhong, user_created) VALUES ('PK001','Phòng Nội tổng quát', @admin_id)
            INSERT INTO DM_DichVuKyThuat(MaDichVu, TenDichVu, GiaDichVu, user_created) VALUES ('DV001','Khám tổng quát',150000, @admin_id)
        END
        """)

    conn.commit()
    conn.close()


# Run init_db when script is executed directly
if __name__ == "__main__":
    print("Initializing database schema...")
    init_db()
    print("Database schema initialized successfully!")
