#!/usr/bin/env python3
"""
Migration tool for administrative division reorganization (NQ 202/2025/QH15)
Công cụ migration sắp xếp đơn vị hành chính
"""

import json
from db import get_conn
from datetime import datetime

# Dữ liệu sắp xếp hành chính theo NQ 202/2025/QH15
ADMIN_REORGANIZATION = {
    "merged": [
        {"new": "Tuyên Quang", "includes": ["Hà Giang", "Tuyên Quang"]},
        {"new": "Lào Cai", "includes": ["Lào Cai", "Yên Bái"]},
        {"new": "Thái Nguyên", "includes": ["Bắc Kạn", "Thái Nguyên"]},
        {"new": "Phú Thọ", "includes": ["Hòa Bình", "Vĩnh Phúc", "Phú Thọ"]},
        {"new": "Bắc Ninh", "includes": ["Bắc Giang", "Bắc Ninh"]},
        {"new": "Hưng Yên", "includes": ["Thái Bình", "Hưng Yên"]},
        {"new": "Thành phố Hải Phòng", "includes": ["Hải Dương", "Thành phố Hải Phòng"]},
        {"new": "Ninh Bình", "includes": ["Hà Nam", "Ninh Bình", "Nam Định"]},
        {"new": "Quảng Trị", "includes": ["Quảng Bình", "Quảng Trị"]},
        {"new": "Thành phố Đà Nẵng", "includes": ["Quảng Nam", "Thành phố Đà Nẵng"]},
        {"new": "Quảng Ngãi", "includes": ["Quảng Ngãi", "Kon Tum"]},
        {"new": "Gia Lai", "includes": ["Gia Lai", "Bình Định"]},
        {"new": "Đắk Lắk", "includes": ["Phú Yên", "Đắk Lắk"]},
        {"new": "Khánh Hòa", "includes": ["Khánh Hòa", "Ninh Thuận"]},
        {"new": "Lâm Đồng", "includes": ["Đắk Nông", "Lâm Đồng", "Bình Thuận"]},
        {"new": "Thành phố Hồ Chí Minh", "includes": ["Bình Dương", "Thành phố Hồ Chí Minh", "Bà Rịa - Vũng Tàu"]},
        {"new": "Đồng Nai", "includes": ["Bình Phước", "Đồng Nai"]},
        {"new": "Tây Ninh", "includes": ["Long An", "Tây Ninh"]},
        {"new": "Thành phố Cần Thơ", "includes": ["Sóc Trăng", "Hậu Giang", "Thành phố Cần Thơ"]},
        {"new": "Vĩnh Long", "includes": ["Bến Tre", "Vĩnh Long", "Trà Vinh"]},
        {"new": "Đồng Tháp", "includes": ["Tiền Giang", "Đồng Tháp"]},
        {"new": "Cà Mau", "includes": ["Bạc Liêu", "Cà Mau"]},
        {"new": "An Giang", "includes": ["Kiên Giang", "An Giang"]}
    ],
    "unchanged": [
        "Thành phố Hà Nội", "Cao Bằng", "Điện Biên", "Hà Tĩnh",
        "Lai Châu", "Lạng Sơn", "Nghệ An", "Quảng Ninh",
        "Thanh Hóa", "Sơn La", "Thành phố Huế"
    ]
}

def create_admin_tables():
    """Tạo các bảng mới cho hệ thống hành chính"""
    conn = get_conn()
    cur = conn.cursor()
    
    print("🏛️ Tạo bảng hệ thống hành chính mới...")
    
    # 1. Bảng DM_HanhChinhMoi (Danh mục hành chính mới)
    print("  📋 Tạo bảng DM_HanhChinhMoi...")
    cur.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='DM_HanhChinhMoi' AND xtype='U')
    CREATE TABLE DM_HanhChinhMoi (
        MaHanhChinhMoi NVARCHAR(10) PRIMARY KEY,
        TenHanhChinhMoi NVARCHAR(100) NOT NULL,
        CapHanhChinh NVARCHAR(20) NOT NULL DEFAULT N'Tỉnh',
        TrangThai BIT DEFAULT 1,
        NgayHieuLuc DATE DEFAULT '2025-01-01',
        GhiChu NVARCHAR(200),
        created_at DATETIME DEFAULT GETDATE()
    );
    """)
    
    # 2. Bảng DM_HanhChinhCu (Danh mục hành chính cũ)
    print("  📋 Tạo bảng DM_HanhChinhCu...")
    cur.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='DM_HanhChinhCu' AND xtype='U')
    CREATE TABLE DM_HanhChinhCu (
        MaHanhChinhCu NVARCHAR(10) PRIMARY KEY,
        TenHanhChinhCu NVARCHAR(100) NOT NULL,
        CapHanhChinh NVARCHAR(20) NOT NULL DEFAULT N'Tỉnh',
        TrangThai BIT DEFAULT 0,
        NgayHetHieuLuc DATE DEFAULT '2024-12-31',
        GhiChu NVARCHAR(200),
        created_at DATETIME DEFAULT GETDATE()
    );
    """)
    
    # 3. Bảng DM_HanhChinhMoi_Map_Cu (Mapping giữa mới và cũ)
    print("  📋 Tạo bảng DM_HanhChinhMoi_Map_Cu...")
    cur.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='DM_HanhChinhMoi_Map_Cu' AND xtype='U')
    CREATE TABLE DM_HanhChinhMoi_Map_Cu (
        MapID UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
        MaHanhChinhMoi NVARCHAR(10) NOT NULL,
        MaHanhChinhCu NVARCHAR(10) NOT NULL,
        TyLeDanSo DECIMAL(5,2) DEFAULT 100.0,
        GhiChu NVARCHAR(200),
        created_at DATETIME DEFAULT GETDATE(),
        
        FOREIGN KEY (MaHanhChinhMoi) REFERENCES DM_HanhChinhMoi(MaHanhChinhMoi),
        FOREIGN KEY (MaHanhChinhCu) REFERENCES DM_HanhChinhCu(MaHanhChinhCu)
    );
    """)
    
    # 4. Không cần thêm cột TinhMoi - sẽ cập nhật trực tiếp cột Tinh
    print("  ✅ Sẽ cập nhật trực tiếp cột Tinh hiện có...")
    
    conn.commit()
    conn.close()
    print("✅ Tạo bảng hành chính thành công!")

def populate_admin_data():
    """Populate dữ liệu vào các bảng hành chính"""
    conn = get_conn()
    cur = conn.cursor()
    
    print("📊 Import dữ liệu hành chính...")
    
    # Mã tỉnh mapping (giữ nguyên từ qr_utils.py)
    province_codes = {
        '001': 'Hà Nội', '002': 'Hà Giang', '004': 'Cao Bằng', '006': 'Bắc Kạn',
        '008': 'Tuyên Quang', '010': 'Lào Cai', '011': 'Điện Biên', '012': 'Lai Châu',
        '014': 'Sơn La', '015': 'Yên Bái', '017': 'Hoà Bình', '019': 'Thái Nguyên',
        '020': 'Lạng Sơn', '022': 'Quảng Ninh', '024': 'Bắc Giang', '025': 'Phú Thọ',
        '026': 'Vĩnh Phúc', '027': 'Bắc Ninh', '030': 'Hải Dương', '031': 'Hải Phòng',
        '033': 'Hưng Yên', '034': 'Thái Bình', '035': 'Hà Nam', '036': 'Nam Định',
        '037': 'Ninh Bình', '038': 'Thanh Hóa', '040': 'Nghệ An', '042': 'Hà Tĩnh',
        '044': 'Quảng Bình', '045': 'Quảng Trị', '046': 'Thừa Thiên Huế',
        '048': 'Đà Nẵng', '049': 'Quảng Nam', '051': 'Quảng Ngãi', '052': 'Bình Định',
        '054': 'Phú Yên', '056': 'Khánh Hòa', '058': 'Ninh Thuận', '060': 'Bình Thuận',
        '062': 'Kon Tum', '064': 'Gia Lai', '066': 'Đắk Lắk', '067': 'Đắk Nông',
        '068': 'Lâm Đồng', '070': 'Bình Phước', '072': 'Tây Ninh', '074': 'Bình Dương',
        '075': 'Đồng Nai', '077': 'Bà Rịa - Vũng Tàu', '079': 'TP.Hồ Chí Minh',
        '080': 'Long An', '082': 'Tiền Giang', '083': 'Bến Tre', '084': 'Trà Vinh',
        '086': 'Vĩnh Long', '087': 'Đồng Tháp', '089': 'An Giang', '091': 'Kiên Giang',
        '092': 'Cần Thơ', '093': 'Hậu Giang', '094': 'Sóc Trăng', '095': 'Bạc Liêu',
        '096': 'Cà Mau'
    }
    
    # 1. Import dữ liệu hành chính cũ
    print("  📥 Import dữ liệu hành chính cũ...")
    for code, name in province_codes.items():
        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM DM_HanhChinhCu WHERE MaHanhChinhCu = ?)
        INSERT INTO DM_HanhChinhCu(MaHanhChinhCu, TenHanhChinhCu, GhiChu)
        VALUES (?, ?, N'Đơn vị hành chính trước sắp xếp')
        """, (code, code, name))
    
    # 2. Import dữ liệu hành chính mới
    print("  📥 Import dữ liệu hành chính mới...")
    new_code = 1
    
    # Tỉnh/thành không thay đổi
    for province in ADMIN_REORGANIZATION['unchanged']:
        ma_moi = f"M{new_code:03d}"
        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM DM_HanhChinhMoi WHERE MaHanhChinhMoi = ?)
        INSERT INTO DM_HanhChinhMoi(MaHanhChinhMoi, TenHanhChinhMoi, GhiChu)
        VALUES (?, ?, N'Đơn vị không thay đổi')
        """, (ma_moi, ma_moi, province))
        new_code += 1
    
    # Tỉnh/thành sáp nhập
    for merged in ADMIN_REORGANIZATION['merged']:
        ma_moi = f"M{new_code:03d}"
        cur.execute("""
        IF NOT EXISTS (SELECT 1 FROM DM_HanhChinhMoi WHERE MaHanhChinhMoi = ?)
        INSERT INTO DM_HanhChinhMoi(MaHanhChinhMoi, TenHanhChinhMoi, GhiChu)
        VALUES (?, ?, ?)
        """, (ma_moi, ma_moi, merged['new'], f"Sáp nhập từ: {', '.join(merged['includes'])}"))
        new_code += 1
    
    # 3. Tạo mapping giữa mới và cũ
    print("  🔗 Tạo mapping hành chính mới-cũ...")
    
    # Mapping cho đơn vị không đổi
    for province in ADMIN_REORGANIZATION['unchanged']:
        # Tìm mã cũ
        old_code = None
        for code, name in province_codes.items():
            if name == province or f"Thành phố {name}" == province or f"TP.{name}" == province:
                old_code = code
                break
        
        if old_code:
            # Tìm mã mới
            cur.execute("SELECT MaHanhChinhMoi FROM DM_HanhChinhMoi WHERE TenHanhChinhMoi = ?", (province,))
            row = cur.fetchone()
            if row:
                ma_moi = row.MaHanhChinhMoi
                cur.execute("""
                IF NOT EXISTS (SELECT 1 FROM DM_HanhChinhMoi_Map_Cu WHERE MaHanhChinhMoi = ? AND MaHanhChinhCu = ?)
                INSERT INTO DM_HanhChinhMoi_Map_Cu(MaHanhChinhMoi, MaHanhChinhCu, TyLeDanSo, GhiChu)
                VALUES (?, ?, 100.0, N'Giữ nguyên')
                """, (ma_moi, old_code, ma_moi, old_code))
    
    # Mapping cho đơn vị sáp nhập
    for merged in ADMIN_REORGANIZATION['merged']:
        # Tìm mã mới
        cur.execute("SELECT MaHanhChinhMoi FROM DM_HanhChinhMoi WHERE TenHanhChinhMoi = ?", (merged['new'],))
        row = cur.fetchone()
        if row:
            ma_moi = row.MaHanhChinhMoi
            
            # Tạo mapping cho từng đơn vị cũ
            for old_province in merged['includes']:
                old_code = None
                for code, name in province_codes.items():
                    if (name == old_province or 
                        f"Thành phố {name}" == old_province or 
                        f"TP.{name}" == old_province or
                        name.replace("TP.", "Thành phố ") == old_province):
                        old_code = code
                        break
                
                if old_code:
                    ty_le = round(100.0 / len(merged['includes']), 2)  # Chia đều tỷ lệ
                    cur.execute("""
                    IF NOT EXISTS (SELECT 1 FROM DM_HanhChinhMoi_Map_Cu WHERE MaHanhChinhMoi = ? AND MaHanhChinhCu = ?)
                    INSERT INTO DM_HanhChinhMoi_Map_Cu(MaHanhChinhMoi, MaHanhChinhCu, TyLeDanSo, GhiChu)
                    VALUES (?, ?, ?, N'Sáp nhập')
                    """, (ma_moi, old_code, ma_moi, old_code, ty_le))
    
    conn.commit()
    conn.close()
    print("✅ Import dữ liệu hành chính thành công!")

def get_new_province_from_old(old_province: str) -> str:
    """
    Mapping tỉnh cũ sang tỉnh mới
    
    Args:
        old_province: Tên tỉnh cũ
        
    Returns:
        Tên tỉnh mới sau sắp xếp
    """
    # Kiểm tra tỉnh không đổi
    if old_province in ADMIN_REORGANIZATION['unchanged']:
        return old_province
    
    # Kiểm tra tỉnh sáp nhập
    for merged in ADMIN_REORGANIZATION['merged']:
        if old_province in merged['includes']:
            return merged['new']
    
    # Xử lý các trường hợp đặc biệt
    name_mappings = {
        'Hà Nội': 'Thành phố Hà Nội',
        'TP.Hồ Chí Minh': 'Thành phố Hồ Chí Minh',
        'Hải Phòng': 'Thành phố Hải Phòng',
        'Đà Nẵng': 'Thành phố Đà Nẵng',
        'Cần Thơ': 'Thành phố Cần Thơ',
        'Thừa Thiên Huế': 'Thành phố Huế'
    }
    
    if old_province in name_mappings:
        return name_mappings[old_province]
    
    # Tìm trong danh sách sáp nhập
    for merged in ADMIN_REORGANIZATION['merged']:
        for include in merged['includes']:
            if (old_province == include or 
                old_province == include.replace('Thành phố ', '') or
                old_province == include.replace('TP.', '')):
                return merged['new']
    
    return old_province  # Trả về tên cũ nếu không tìm thấy

def migrate_patient_provinces():
    """Migration thông tin tỉnh của bệnh nhân - cập nhật trực tiếp cột Tinh"""
    conn = get_conn()
    cur = conn.cursor()
    
    print("🔄 Bắt đầu migration thông tin tỉnh bệnh nhân...")
    
    # Lấy tất cả bệnh nhân có thông tin tỉnh
    cur.execute("SELECT BN_ID, Tinh FROM BenhNhan WHERE Tinh IS NOT NULL AND Tinh != ''")
    patients = cur.fetchall()
    
    migrated_count = 0
    unchanged_count = 0
    error_count = 0
    
    print(f"📊 Tìm thấy {len(patients)} bệnh nhân có thông tin tỉnh")
    
    for patient in patients:
        try:
            bn_id = patient.BN_ID
            old_province = patient.Tinh.strip()
            
            # Mapping sang tỉnh mới
            new_province = get_new_province_from_old(old_province)
            
            # Chỉ cập nhật nếu tên tỉnh thay đổi
            if new_province != old_province:
                cur.execute("""
                UPDATE BenhNhan 
                SET Tinh = ?
                WHERE BN_ID = ?
                """, (new_province, bn_id))
                migrated_count += 1
                
                if migrated_count % 50 == 0:
                    print(f"  ✅ Đã migration {migrated_count} bệnh nhân...")
            else:
                unchanged_count += 1
                
        except Exception as e:
            error_count += 1
            print(f"  ❌ Lỗi migration bệnh nhân {bn_id}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Hoàn thành migration:")
    print(f"   - Đã cập nhật: {migrated_count} bệnh nhân")
    print(f"   - Không thay đổi: {unchanged_count} bệnh nhân") 
    print(f"   - Lỗi: {error_count} bệnh nhân")

def run_full_migration():
    """Chạy toàn bộ migration hành chính"""
    print("🚀 Bắt đầu migration hệ thống hành chính (NQ 202/2025/QH15)")
    print("=" * 70)
    
    try:
        # 1. Tạo bảng
        create_admin_tables()
        print()
        
        # 2. Populate dữ liệu  
        populate_admin_data()
        print()
        
        # 3. Migration bệnh nhân
        migrate_patient_provinces()
        print()
        
        print("=" * 70)
        print("✅ HOÀN THÀNH MIGRATION HỆ THỐNG HÀNH CHÍNH!")
        print("📊 Các bảng đã được tạo:")
        print("   - DM_HanhChinhMoi: Danh mục hành chính mới")
        print("   - DM_HanhChinhCu: Danh mục hành chính cũ") 
        print("   - DM_HanhChinhMoi_Map_Cu: Bảng mapping")
        print("   - BenhNhan: Cập nhật cột Tinh với tên mới")
        
    except Exception as e:
        print(f"❌ Lỗi migration: {e}")
        return False
    
    return True

if __name__ == "__main__":
    run_full_migration()