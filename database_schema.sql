-- ===============================================================
-- HỆ THỐNG QUẢN LÝ KHÁM BỆNH - DATABASE SCHEMA
-- ===============================================================
-- File: database_schema.sql
-- Description: Complete database schema for medical management system
-- Features: QR code patient registration, clinic management, services
-- Created: 2025
-- ===============================================================

-- ===============================================================
-- 1. CREATE DATABASE (Optional - run only if database doesn't exist)
-- ===============================================================
-- USE master;
-- GO
-- CREATE DATABASE [DangKyKhamBenh];
-- GO
-- USE [DangKyKhamBenh];
-- GO

-- ===============================================================
-- 2. DROP EXISTING TABLES (Optional - for clean rebuild)
-- ===============================================================
-- DROP TABLE IF EXISTS TiepNhan;
-- DROP TABLE IF EXISTS BenhNhan;
-- DROP TABLE IF EXISTS PhongKham;
-- DROP TABLE IF EXISTS BacSi;
-- DROP TABLE IF EXISTS DM_DichVuKyThuat;
-- DROP TABLE IF EXISTS [user];

-- ===============================================================
-- 3. CREATE TABLES
-- ===============================================================

-- 3.1 User Table (System Authentication)
-- ===============================================================
CREATE TABLE [user] (
    user_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    username NVARCHAR(50) UNIQUE NOT NULL,
    role NVARCHAR(20) NOT NULL,
    pass NVARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT GETDATE()
);

-- 3.2 BacSi Table (Doctors)
-- ===============================================================
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

-- 3.3 PhongKham Table (Clinics/Rooms)
-- ===============================================================
CREATE TABLE PhongKham (
    PK_ID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    MaPhong NVARCHAR(20) UNIQUE NOT NULL,
    TenPhong NVARCHAR(100) NOT NULL,
    BS_ID UNIQUEIDENTIFIER NULL,
    user_created UNIQUEIDENTIFIER,
    created_at DATETIME DEFAULT GETDATE()
);

-- 3.4 DM_DichVuKyThuat Table (Medical Services)
-- ===============================================================
CREATE TABLE DM_DichVuKyThuat (
    dv_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    MaDichVu NVARCHAR(20) UNIQUE NOT NULL,
    TenDichVu NVARCHAR(100) NOT NULL,
    GiaDichVu INT NOT NULL,
    user_created UNIQUEIDENTIFIER,
    created_at DATETIME DEFAULT GETDATE()
);

-- 3.5 BenhNhan Table (Patients) - Supports QR Code Registration
-- ===============================================================
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

-- 3.6 TiepNhan Table (Patient Registration/Reception)
-- ===============================================================
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

-- ===============================================================
-- 4. CREATE FOREIGN KEY CONSTRAINTS
-- ===============================================================

-- 4.1 PhongKham -> BacSi (One doctor per clinic)
ALTER TABLE PhongKham 
ADD CONSTRAINT FK_PhongKham_BacSi 
FOREIGN KEY (BS_ID) REFERENCES BacSi(BS_ID);

-- 4.2 TiepNhan -> BenhNhan (Patient registration)
ALTER TABLE TiepNhan 
ADD CONSTRAINT FK_TiepNhan_BenhNhan
FOREIGN KEY (BN_ID) REFERENCES BenhNhan(BN_ID) ON DELETE CASCADE;

-- 4.3 TiepNhan -> DM_DichVuKyThuat (Service selection)
ALTER TABLE TiepNhan 
ADD CONSTRAINT FK_TiepNhan_DichVu
FOREIGN KEY (Dv_ID) REFERENCES DM_DichVuKyThuat(dv_id);

-- 4.4 TiepNhan -> PhongKham (Clinic assignment)
ALTER TABLE TiepNhan 
ADD CONSTRAINT FK_TiepNhan_PhongKham
FOREIGN KEY (PK_ID) REFERENCES PhongKham(PK_ID);

-- 4.5 TiepNhan -> BacSi (Doctor assignment)
ALTER TABLE TiepNhan 
ADD CONSTRAINT FK_TiepNhan_BacSi
FOREIGN KEY (BS_ID) REFERENCES BacSi(BS_ID);

-- ===============================================================
-- 5. CREATE INDEXES FOR PERFORMANCE
-- ===============================================================

-- Indexes for frequently searched columns
CREATE INDEX IX_BenhNhan_SoCCCD ON BenhNhan(SoCCCD);
CREATE INDEX IX_BenhNhan_SoCMND ON BenhNhan(SoCMND);
CREATE INDEX IX_BenhNhan_PID ON BenhNhan(PID);
CREATE INDEX IX_TiepNhan_MaTiepNhan ON TiepNhan(MaTiepNhan);
CREATE INDEX IX_TiepNhan_created_at ON TiepNhan(created_at);
CREATE INDEX IX_BacSi_MaBacSi ON BacSi(MaBacSi);
CREATE INDEX IX_PhongKham_MaPhong ON PhongKham(MaPhong);
CREATE INDEX IX_DichVu_MaDichVu ON DM_DichVuKyThuat(MaDichVu);

-- ===============================================================
-- 6. INSERT INITIAL DATA
-- ===============================================================

-- 6.1 Create Admin User
INSERT INTO [user](user_id, username, role, pass) 
VALUES (NEWID(), 'admin', 'ADMIN', 'admin');

-- 6.2 Insert Sample Clinics
INSERT INTO PhongKham(PK_ID, MaPhong, TenPhong) VALUES
(NEWID(), 'PK001', N'Phòng Nội tổng quát'),
(NEWID(), 'PK002', N'Phòng Nhi khoa'),
(NEWID(), 'PK003', N'Phòng Sản phụ khoa'),
(NEWID(), 'PK004', N'Phòng Tai Mũi Họng'),
(NEWID(), 'PK005', N'Phòng Mắt'),
(NEWID(), 'PK006', N'Phòng Da liễu'),
(NEWID(), 'PK007', N'Phòng Tim mạch'),
(NEWID(), 'PK008', N'Phòng Thần kinh'),
(NEWID(), 'PK009', N'Phòng Cơ xương khớp'),
(NEWID(), 'PK010', N'Phòng Ung bướu'),
(NEWID(), 'PK011', N'Phòng Cấp cứu'),
(NEWID(), 'PK012', N'Phòng X-Quang'),
(NEWID(), 'PK013', N'Phòng Siêu âm'),
(NEWID(), 'PK014', N'Phòng Xét nghiệm'),
(NEWID(), 'PK015', N'Phòng Phục hồi chức năng');

-- 6.3 Insert Sample Medical Services
INSERT INTO DM_DichVuKyThuat(dv_id, MaDichVu, TenDichVu, GiaDichVu) VALUES
(NEWID(), 'DV001', N'Khám tổng quát', 150000),
(NEWID(), 'DV002', N'Khám chuyên khoa Nhi', 200000),
(NEWID(), 'DV003', N'Khám Sản phụ khoa', 250000),
(NEWID(), 'DV004', N'Khám Tai Mũi Họng', 180000),
(NEWID(), 'DV005', N'Khám Mắt', 180000),
(NEWID(), 'DV006', N'Khám Da liễu', 200000),
(NEWID(), 'DV007', N'Khám Tim mạch', 300000),
(NEWID(), 'DV008', N'Khám Thần kinh', 280000),
(NEWID(), 'DV009', N'Khám Cơ xương khớp', 250000),
(NEWID(), 'DV010', N'Khám Ung bướu', 350000),
(NEWID(), 'DV011', N'Cấp cứu', 500000),
(NEWID(), 'DV012', N'Chụp X-Quang', 120000),
(NEWID(), 'DV013', N'Siêu âm tổng quát', 200000),
(NEWID(), 'DV014', N'Siêu âm thai', 250000),
(NEWID(), 'DV015', N'Xét nghiệm máu tổng quát', 150000),
(NEWID(), 'DV016', N'Xét nghiệm sinh hóa', 300000),
(NEWID(), 'DV017', N'Xét nghiệm nước tiểu', 80000),
(NEWID(), 'DV018', N'Chụp CT Scanner', 800000),
(NEWID(), 'DV019', N'Chụp MRI', 1200000),
(NEWID(), 'DV020', N'Nội soi dạ dày', 600000),
(NEWID(), 'DV021', N'Điện tim', 100000),
(NEWID(), 'DV022', N'Đo huyết áp 24h', 300000),
(NEWID(), 'DV023', N'Phục hồi chức năng', 200000),
(NEWID(), 'DV024', N'Vật lý trị liệu', 150000),
(NEWID(), 'DV025', N'Tư vấn dinh dưỡng', 120000);

-- 6.4 Insert Sample Doctors
INSERT INTO BacSi(BS_ID, MaBacSi, HoTen, ChuyenKhoa, SoDienThoai, Email) VALUES
(NEWID(), 'BS001', N'BS. Nguyễn Văn An', N'Nội tổng quát', '0901234567', 'bs.an@hospital.com'),
(NEWID(), 'BS002', N'TS.BS. Trần Thị Bình', N'Nhi khoa', '0907654321', 'bs.binh@hospital.com'),
(NEWID(), 'BS003', N'PGS.TS. Lê Văn Cường', N'Sản phụ khoa', '0912345678', 'bs.cuong@hospital.com'),
(NEWID(), 'BS004', N'BS. Phạm Thị Dung', N'Tai Mũi Họng', '0987654321', 'bs.dung@hospital.com'),
(NEWID(), 'BS005', N'BS. Hoàng Minh Tuan', N'Mắt', '0934567890', 'bs.tuan@hospital.com'),
(NEWID(), 'BS006', N'BS. Đinh Thị Hoa', N'Da liễu', '0923456789', 'bs.hoa@hospital.com'),
(NEWID(), 'BS007', N'GS.TS. Vũ Công Minh', N'Tim mạch', '0945678901', 'bs.minh@hospital.com'),
(NEWID(), 'BS008', N'PGS. Ngô Thị Linh', N'Thần kinh', '0956789012', 'bs.linh@hospital.com'),
(NEWID(), 'BS009', N'BS. Bùi Văn Khoa', N'Cơ xương khớp', '0967890123', 'bs.khoa@hospital.com'),
(NEWID(), 'BS010', N'TS.BS. Mai Thị Lan', N'Ung bướu', '0978901234', 'bs.lan@hospital.com'),
(NEWID(), 'BS011', N'BS. Trịnh Văn Nam', N'Cấp cứu', '0989012345', 'bs.nam@hospital.com'),
(NEWID(), 'BS012', N'BS. Lý Thị Oanh', N'Chẩn đoán hình ảnh', '0990123456', 'bs.oanh@hospital.com'),
(NEWID(), 'BS013', N'BS. Đỗ Minh Phú', N'Chẩn đoán hình ảnh', '0901234560', 'bs.phu@hospital.com'),
(NEWID(), 'BS014', N'BS. Cao Thị Quyên', N'Xét nghiệm', '0912345601', 'bs.quyen@hospital.com'),
(NEWID(), 'BS015', N'BS. Lương Văn Sơn', N'Phục hồi chức năng', '0923456012', 'bs.son@hospital.com');

-- ===============================================================
-- 7. USEFUL QUERIES FOR SYSTEM OPERATION
-- ===============================================================

-- 7.1 View all patients with their latest registration
/*
SELECT 
    bn.HoTen,
    bn.SoCCCD,
    tn.MaTiepNhan,
    tn.LyDoKham,
    pk.TenPhong,
    bs.HoTen AS TenBacSi,
    dv.TenDichVu,
    tn.created_at
FROM BenhNhan bn
LEFT JOIN TiepNhan tn ON bn.BN_ID = tn.BN_ID
LEFT JOIN PhongKham pk ON tn.PK_ID = pk.PK_ID
LEFT JOIN BacSi bs ON tn.BS_ID = bs.BS_ID
LEFT JOIN DM_DichVuKyThuat dv ON tn.Dv_ID = dv.dv_id
ORDER BY tn.created_at DESC;
*/

-- 7.2 View clinic workload
/*
SELECT 
    pk.TenPhong,
    bs.HoTen AS BacSiChinh,
    COUNT(tn.TiepNhan_ID) AS SoLuotKham,
    SUM(dv.GiaDichVu) AS TongDoanhThu
FROM PhongKham pk
LEFT JOIN BacSi bs ON pk.BS_ID = bs.BS_ID
LEFT JOIN TiepNhan tn ON pk.PK_ID = tn.PK_ID
LEFT JOIN DM_DichVuKyThuat dv ON tn.Dv_ID = dv.dv_id
GROUP BY pk.TenPhong, bs.HoTen
ORDER BY SoLuotKham DESC;
*/

-- 7.3 Find patient by CCCD (for QR code lookup)
/*
SELECT * FROM BenhNhan WHERE SoCCCD = '058012345678';
*/

-- 7.4 Daily registration report
/*
SELECT 
    CAST(tn.created_at AS DATE) AS NgayKham,
    COUNT(*) AS SoLuotTiepNhan,
    COUNT(DISTINCT tn.BN_ID) AS SoBenhNhanKhacNhau,
    SUM(dv.GiaDichVu) AS DoanhThuNgay
FROM TiepNhan tn
LEFT JOIN DM_DichVuKyThuat dv ON tn.Dv_ID = dv.dv_id
WHERE tn.created_at >= DATEADD(day, -7, GETDATE())
GROUP BY CAST(tn.created_at AS DATE)
ORDER BY NgayKham DESC;
*/

-- ===============================================================
-- 8. QR CODE INTEGRATION NOTES
-- ===============================================================
/*
QR Code Format: CCCD|CMND|HoTen|NgaySinh|GioiTinh|DiaChi
Example: 058012345678|23456789|Nguyễn Văn Test|15071990|Nam|123 Đường ABC, Quận 1, TP.HCM

The system automatically:
1. Parses QR code data
2. Creates patient record in BenhNhan table
3. Generates PID and user account
4. Ready for TiepNhan registration
*/

-- ===============================================================
-- END OF SCHEMA
-- ===============================================================