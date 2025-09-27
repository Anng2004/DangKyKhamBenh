import pyodbc

# Cấu hình kết nối SQL Server - THAY ĐỔI THEO MÔิI TRƯỜNG CỦA BẠN
CONN_STR = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"                    # VD: localhost, DESKTOP-ABC\\SQLEXPRESS
    "Database=DangKyKhamBenh;"            # Tên database - sẽ tự tạo nếu chưa có
    "UID=SA;"                             # Username SQL Server  
    "PWD=Admin@123;"                      # Password SQL Server
    "TrustServerCertificate=yes;"
)

# Connection string cho master database để tạo database mới
MASTER_CONN_STR = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;" 
    "Database=master;"
    "UID=SA;"
    "PWD=Admin@123;"
    "TrustServerCertificate=yes;"
)

def create_database_if_not_exists():
    """Tạo database nếu chưa tồn tại"""
    try:
        # Extract database name from connection string
        import re
        db_match = re.search(r'Database=([^;]+)', CONN_STR)
        if not db_match:
            print("❌ Không tìm thấy tên database trong connection string")
            return False
        
        database_name = db_match.group(1)
        print(f"🔍 Kiểm tra database: {database_name}")
        
        # Kết nối đến master database
        conn = pyodbc.connect(MASTER_CONN_STR)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Kiểm tra xem database đã tồn tại chưa
        cur.execute("SELECT name FROM sys.databases WHERE name = ?", (database_name,))
        if not cur.fetchone():
            print(f"🔧 Tạo database {database_name}...")
            cur.execute(f"CREATE DATABASE [{database_name}]")
            print("✅ Database được tạo thành công!")
        else:
            print(f"ℹ️  Database {database_name} đã tồn tại")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Lỗi khi tạo database: {e}")
        print("💡 Hãy kiểm tra:")
        print("   - SQL Server đã chạy chưa?")
        print("   - Thông tin kết nối trong CONN_STR đã đúng chưa?")
        print("   - User có quyền tạo database không?")
        return False

def get_conn():
    try:
        return pyodbc.connect(CONN_STR)
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
        print("💡 Hãy chạy: python db.py để khởi tạo database")
        raise

def init_db(seed: bool = True) -> None:
    # Tạo database trước nếu chưa có
    if not create_database_if_not_exists():
        return False
    
    conn = get_conn()
    cur = conn.cursor()

    # Tạo bảng User
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

    # Tạo bảng PhongKham
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

    # Tạo bảng DM_DichVuKyThuat
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

    # Tạo bảng BenhNhan
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

    # Tạo bảng BacSi
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

    # Tạo bảng TiepNhan
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

    # Tạo Foreign Keys
    
    # Drop existing FK constraints first (if any)
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
    
    # FK cho PhongKham -> BacSi (NO ACTION - không cho xóa bác sĩ khi còn phòng khám)
    cur.execute("""
    ALTER TABLE PhongKham ADD CONSTRAINT FK_PhongKham_BacSi 
    FOREIGN KEY (BS_ID) REFERENCES BacSi(BS_ID) ON DELETE NO ACTION
    """)
    
    # FK cho TiepNhan -> BenhNhan (NO ACTION - bảo vệ tính toàn vẹn dữ liệu)
    cur.execute("""
    ALTER TABLE TiepNhan ADD CONSTRAINT FK_TiepNhan_BenhNhan
    FOREIGN KEY (BN_ID) REFERENCES BenhNhan(BN_ID) ON DELETE NO ACTION
    """)
    
    # FK cho TiepNhan -> DichVu (NO ACTION - không cho xóa dịch vụ khi còn tiếp nhận)
    cur.execute("""
    ALTER TABLE TiepNhan ADD CONSTRAINT FK_TiepNhan_DichVu
    FOREIGN KEY (Dv_ID) REFERENCES DM_DichVuKyThuat(dv_id) ON DELETE NO ACTION
    """)
    
    # FK cho TiepNhan -> PhongKham (NO ACTION - không cho xóa phòng khám khi còn tiếp nhận)
    cur.execute("""
    ALTER TABLE TiepNhan ADD CONSTRAINT FK_TiepNhan_PhongKham
    FOREIGN KEY (PK_ID) REFERENCES PhongKham(PK_ID) ON DELETE NO ACTION
    """)
    
    # FK cho TiepNhan -> BacSi (NO ACTION - không cho xóa bác sĩ khi còn tiếp nhận)
    cur.execute("""
    ALTER TABLE TiepNhan ADD CONSTRAINT FK_TiepNhan_BacSi
    FOREIGN KEY (BS_ID) REFERENCES BacSi(BS_ID) ON DELETE NO ACTION
    """)

    if seed:
        # Insert initial admin user
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


# Run init_db when script is executed directly
if __name__ == "__main__":
    print("="*60)
    print("     🏥 KHỞI TẠO DATABASE - HỆ THỐNG QUẢN LÝ KHÁM BỆNH")
    print("="*60)
    print("")
    print("💡 Hướng dẫn:")
    print("   1. Đảm bảo SQL Server đã chạy")
    print("   2. Kiểm tra thông tin kết nối trong file db.py")
    print("   3. User cần có quyền tạo database")
    print("")
    
    try:
        success = init_db(seed=True)
        if success:
            print("")
            print("🎉 Khởi tạo database thành công!")
            print("")
            print("📋 Thông tin đăng nhập:")
            print("   👤 Username: admin")
            print("   🔒 Password: admin")
            print("")
            print("🚀 Bước tiếp theo:")
            print("   python import_data.py  # Import dữ liệu mẫu")
            print("   python app.py          # Chạy ứng dụng")
        else:
            print("")
            print("❌ Khởi tạo database thất bại!")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
