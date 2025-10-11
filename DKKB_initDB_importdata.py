# import_data.py - Import dữ liệu mẫu cho hệ thống

import sys
from MSSQLServer import MSSQLConnection
from utils.message_utils import error, success, warning, info, print_separator

class InitDB:
    @classmethod
    def create_database_if_not_exists(cls, database_name="DangKyKhamBenh"):
        try:
            import re
            db_match = re.search(r'Database=([^;]+)', f"Database={database_name}")
            if not db_match:
                error("Không tìm thấy tên database trong connection string")
                return False
            
            database_name = db_match.group(1)
            print(f"🔍 Kiểm tra database: {database_name}")
            
            conn = MSSQLConnection(database="master")
            conn.connect()
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
        conn.connect()
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
class Import_data:
    @classmethod
    def kiem_tra_ton_tai_DB(cls):
        """Kiểm tra database và các bảng cần thiết đã tồn tại chưa."""
        try:
            conn = MSSQLConnection(database="DangKyKhamBenh")
            conn.connect()
            cur = conn.cursor()
            
            cur.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME IN ('user', 'PhongKham', 'DM_DichVuKyThuat', 'BacSi')")
            table_count = cur.fetchone()[0]
            
            conn.close()
            return table_count >= 4
        except Exception as e:
            error(f"Lỗi kết nối database: {e}")
            return False
    @staticmethod
    def import_phong_kham():
        conn = MSSQLConnection(database="DangKyKhamBenh")
        conn.connect()
        cur = conn.cursor()
        
        phong_kham_data = [
            ('PK002', 'Phòng Nhi khoa'),
            ('PK003', 'Phòng Sản phụ khoa'),
            ('PK004', 'Phòng Tai Mũi Họng'),
            ('PK005', 'Phòng Mắt'),
            ('PK006', 'Phòng Da liễu'),
            ('PK007', 'Phòng Tim mạch'),
            ('PK008', 'Phòng Thần kinh'),
            ('PK009', 'Phòng Cơ xương khớp'),
            ('PK010', 'Phòng Ung bướu'),
            ('PK011', 'Phòng Cấp cứu'),
            ('PK012', 'Phòng X-Quang'),
            ('PK013', 'Phòng Siêu âm'),
            ('PK014', 'Phòng Xét nghiệm'),
            ('PK015', 'Phòng Phục hồi chức năng'),
            ('PK016', 'Phòng Vật lý trị liệu'),
            ('PK017', 'Phòng Tư vấn dinh dưỡng'),
        ]
        
        print("🏥 Đang import dữ liệu Phòng khám...")
        for ma_phong, ten_phong in phong_kham_data:
            try:
                cur.execute("SELECT COUNT(*) FROM PhongKham WHERE MaPhong = ?", (ma_phong,))
                exists = cur.fetchone()[0]
                
                if exists == 0:
                    cur.execute("""
                        INSERT INTO PhongKham(PK_ID, MaPhong, TenPhong) 
                        VALUES (NEWID(), ?, ?)
                    """, (ma_phong, ten_phong))
                    success(f"Đã thêm: {ma_phong} - {ten_phong}")
                else:
                    warning(f"Đã tồn tại: {ma_phong} - {ten_phong}")
            except Exception as e:
                error(f"Lỗi khi thêm {ma_phong}: {e}")
        conn.commit()
        conn.close()
    @staticmethod
    def import_dich_vu():
        conn = MSSQLConnection(database="DangKyKhamBenh")
        conn.connect()
        cur = conn.cursor()
        
        dich_vu_data = [
            ('DV002', 'Khám chuyên khoa Nhi', 120000),
            ('DV003', 'Khám Sản phụ khoa', 150000),
            ('DV004', 'Khám Tai Mũi Họng', 100000),
            ('DV005', 'Khám Mắt', 80000),
            ('DV006', 'Khám Da liễu', 90000),
            ('DV007', 'Khám Tim mạch', 200000),
            ('DV008', 'Khám Thần kinh', 180000),
            ('DV009', 'Khám Cơ xương khớp', 130000),
            ('DV010', 'Khám Ung bướu', 250000),
            ('DV011', 'Cấp cứu', 300000),
            ('DV012', 'Chụp X-Quang', 150000),
            ('DV013', 'Siêu âm tổng quát', 200000),
            ('DV014', 'Siêu âm thai', 180000),
            ('DV015', 'Xét nghiệm máu tổng quát', 100000),
            ('DV016', 'Xét nghiệm sinh hóa', 150000),
            ('DV017', 'Xét nghiệm nước tiểu', 50000),
            ('DV018', 'Chụp CT Scanner', 500000),
            ('DV019', 'Chụp MRI', 800000),
            ('DV020', 'Nội soi dạ dày', 300000),
            ('DV021', 'Điện tim', 80000),
            ('DV022', 'Đo huyết áp 24h', 200000),
            ('DV023', 'Phục hồi chức năng', 150000),
            ('DV024', 'Vật lý trị liệu', 120000),
            ('DV025', 'Tư vấn dinh dưỡng', 100000)
        ]
        
        print("🩺 Đang import dữ liệu Dịch vụ...")
        for ma_dv, ten_dv, gia in dich_vu_data:
            try:
                cur.execute("SELECT COUNT(*) FROM DM_DichVuKyThuat WHERE MaDichVu = ?", (ma_dv,))
                exists = cur.fetchone()[0]
                
                if exists == 0:
                    cur.execute("""
                        INSERT INTO DM_DichVuKyThuat(dv_id, MaDichVu, TenDichVu, GiaDichVu) 
                        VALUES (NEWID(), ?, ?, ?)
                    """, (ma_dv, ten_dv, gia))
                    success(f"Đã thêm: {ma_dv} - {ten_dv} - {gia:,}đ")
                else:
                    warning(f"Đã tồn tại: {ma_dv} - {ten_dv}")
            except Exception as e:
                error(f"Lỗi khi thêm {ma_dv}: {e}")

        conn.commit()
        conn.close()
    @staticmethod
    def import_bac_si():
        conn = MSSQLConnection(database="DangKyKhamBenh")
        conn.connect()
        cur = conn.cursor()
        
        bac_si_data = [
            ('BS001', 'BS. Nguyễn Văn An', 'Nội tổng quát', '0901234567', 'bs.an@hospital.com'),
            ('BS002', 'TS.BS. Trần Thị Bình', 'Nhi khoa', '0907654321', 'bs.binh@hospital.com'),
            ('BS003', 'PGS.TS. Lê Văn Cường', 'Sản phụ khoa', '0912345678', 'bs.cuong@hospital.com'),
            ('BS004', 'BS. Phạm Thị Dung', 'Tai Mũi Họng', '0987654321', 'bs.dung@hospital.com'),
            ('BS005', 'BS. Hoàng Minh Tuan', 'Mắt', '0934567890', 'bs.tuan@hospital.com'),
            ('BS006', 'BS. Đinh Thị Hoa', 'Da liễu', '0923456789', 'bs.hoa@hospital.com'),
            ('BS007', 'GS.TS. Vũ Công Minh', 'Tim mạch', '0945678901', 'bs.minh@hospital.com'),
            ('BS008', 'PGS. Ngô Thị Linh', 'Thần kinh', '0956789012', 'bs.linh@hospital.com'),
            ('BS009', 'BS. Bùi Văn Khoa', 'Cơ xương khớp', '0967890123', 'bs.khoa@hospital.com'),
            ('BS010', 'TS.BS. Mai Thị Lan', 'Ung bướu', '0978901234', 'bs.lan@hospital.com'),
            ('BS011', 'BS. Trịnh Văn Nam', 'Cấp cứu', '0989012345', 'bs.nam@hospital.com'),
            ('BS012', 'BS. Lý Thị Oanh', 'Chẩn đoán hình ảnh', '0990123456', 'bs.oanh@hospital.com'),
            ('BS013', 'BS. Đỗ Minh Phú', 'Chẩn đoán hình ảnh', '0901234560', 'bs.phu@hospital.com'),
            ('BS014', 'BS. Cao Thị Quyên', 'Xét nghiệm', '0912345601', 'bs.quyen@hospital.com'),
            ('BS015', 'BS. Lương Văn Sơn', 'Phục hồi chức năng', '0923456012', 'bs.son@hospital.com'),
        ]
        
        info("👨‍⚕️ Đang import dữ liệu Bác sĩ...")
        for ma_bs, ho_ten, chuyen_khoa, sdt, email in bac_si_data:
            try:
                cur.execute("SELECT COUNT(*) FROM BacSi WHERE MaBacSi = ?", (ma_bs,))
                exists = cur.fetchone()[0]
                
                if exists == 0:
                    cur.execute("""
                        INSERT INTO BacSi(MaBacSi, HoTen, ChuyenKhoa, SoDienThoai, Email) 
                        VALUES (?, ?, ?, ?, ?)
                    """, (ma_bs, ho_ten, chuyen_khoa, sdt, email))
                    success(f"  Đã thêm: {ma_bs} - {ho_ten} - {chuyen_khoa}")
                else:
                    warning(f"  Đã tồn tại: {ma_bs} - {ho_ten}")
            except Exception as e:
                error(f"  Lỗi khi thêm {ma_bs}: {e}")
        
        conn.commit()
        conn.close()
    @staticmethod
    def phancong_bacsi_phongkham():
        conn = MSSQLConnection(database="DangKyKhamBenh")
        conn.connect()
        cur = conn.cursor()
        
        ds_phan_cong_bs_pk = [
            ('BS001', 'PK001'),
            ('BS002', 'PK002'),
            ('BS003', 'PK003'),
            ('BS004', 'PK004'),
            ('BS005', 'PK005'),
            ('BS006', 'PK006'),
            ('BS007', 'PK007'),
            ('BS008', 'PK008'),
            ('BS009', 'PK009'),
            ('BS010', 'PK010'),
            ('BS011', 'PK011'),
            ('BS012', 'PK012'),
            ('BS013', 'PK012'),
            ('BS014', 'PK014'),
            ('BS015', 'PK015'),
        ]
        
        print("🔄 Đang gán bác sĩ vào phòng khám...")
        for ma_bs, ma_pk in ds_phan_cong_bs_pk:
            try:
                cur.execute("SELECT BS_ID FROM BacSi WHERE MaBacSi = ?", (ma_bs,))
                bs_row = cur.fetchone()
                if not bs_row:
                    error(f"Không tìm thấy bác sĩ {ma_bs}")
                    continue
                bs_id = bs_row[0]
                
                cur.execute("SELECT PK_ID FROM PhongKham WHERE MaPhong = ?", (ma_pk,))
                pk_row = cur.fetchone()
                if not pk_row:
                    error(f"Không tìm thấy phòng khám {ma_pk}")
                    continue
                pk_id = pk_row[0]
                
                cur.execute("SELECT BS_ID FROM PhongKham WHERE PK_ID = ?", (pk_id,))
                bs_ht = cur.fetchone()
                
                if not bs_ht or bs_ht.BS_ID is None:
                    cur.execute("UPDATE PhongKham SET BS_ID = ? WHERE PK_ID = ?", (bs_id, pk_id))
                    success(f"Đã gán bác sĩ {ma_bs} vào phòng khám {ma_pk}")
                else:
                    warning(f"Phòng khám {ma_pk} đã có bác sĩ chính")

            except Exception as e:
                error(f"Lỗi khi gán {ma_bs}: {e}")

        conn.commit()
        conn.close()
    def show_statistics():
        conn = MSSQLConnection(database="DangKyKhamBenh")
        conn.connect()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM PhongKham")
        pk_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM DM_DichVuKyThuat")
        dv_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM BacSi")
        bs_count = cur.fetchone()[0]
        
        conn.close()
        
        print("\n" + "="*50)
        print("           📊 THỐNG KÊ SAU IMPORT")
        print_separator(50,"=")
        print(f"🏥 Tổng số Phòng khám: {pk_count}")
        print(f"🩺 Tổng số Dịch vụ: {dv_count}")
        print(f"👨‍⚕️ Tổng số Bác sĩ: {bs_count}")
        print_separator(50,"=")
    def import_pk_dv_bs():
        print_separator(60,"=")
        print("     🚀 IMPORT DỮ LIỆU MẪU - PHÒNG KHÁM, DỊCH VỤ & BÁC SĨ")
        print_separator(60,"=")
        
        try:
            Import_data.import_phong_kham()
            print()
            
            Import_data.import_dich_vu()
            print()
            
            Import_data.import_bac_si()
            print()
            
            Import_data.show_statistics()
            
            print("\nImport hoàn tất!")
            
        except Exception as e:
            error(f"Lỗi trong quá trình import: {e}")
    def main():
        """Chạy import dữ liệu mẫu."""
        print("Bắt đầu import dữ liệu mẫu...")
        print_separator(60,"=")
        
        try:
            if not Import_data.kiem_tra_ton_tai_DB():
                warning("Database 'DangKyKhamBenh' chưa tồn tại hoặc chưa có bảng cần thiết.")
                print("💡 Vui lòng chạy init_db() để tạo database và schema trước khi import dữ liệu.")
                sys.exit(1)
            Import_data.import_phong_kham()
            print()
            
            Import_data.import_dich_vu()
            print()
            
            Import_data.import_bac_si()
            print()
            
            Import_data.phancong_bacsi_phongkham()
            print()
            
            print_separator(60,"=")
            success("Hoàn thành import dữ liệu mẫu!")
            conn = MSSQLConnection(database="DangKyKhamBenh")
            conn.connect()
            cur = conn.cursor()
            
            cur.execute("SELECT COUNT(*) FROM PhongKham")
            pk_count = cur.fetchone()[0]
            print(f"   • Phòng khám: {pk_count} records")
            
            cur.execute("SELECT COUNT(*) FROM DM_DichVuKyThuat")
            dv_count = cur.fetchone()[0]
            print(f"   • Dịch vụ: {dv_count} records")
            
            cur.execute("SELECT COUNT(*) FROM BacSi")
            bs_count = cur.fetchone()[0]
            print(f"   • Bác sĩ: {bs_count} records")
            
            conn.close()
            
        except Exception as e:
            error(f"Lỗi khi import dữ liệu: {e}")
            print("💡 Vui lòng kiểm tra:")
            print("   1. Database server đã khởi động?")
            print("   2. Cấu hình kết nối trong db.py đã đúng?")
            print("   3. Đã chạy init_db() để tạo schema?")
            sys.exit(1)

if __name__ == "__main__":
        Import_data.main()