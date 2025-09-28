#!/usr/bin/env python3
"""
Migration tool for administrative division reorganization (NQ 202/2025/QH15)
Công cụ migration sắp xếp đơn vị hành chính
"""

import json
from db import get_conn
from datetime import datetime
from utils.message_utils import error, success, warning, info, print_separator

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

def get_new_province_from_old(old_province: str) -> str:
    if old_province in ADMIN_REORGANIZATION['unchanged']:
        return old_province
    
    for merged in ADMIN_REORGANIZATION['merged']:
        if old_province in merged['includes']:
            return merged['new']
    
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
    
    for merged in ADMIN_REORGANIZATION['merged']:
        for include in merged['includes']:
            if (old_province == include or 
                old_province == include.replace('Thành phố ', '') or
                old_province == include.replace('TP.', '')):
                return merged['new']
    
    return old_province

def migrate_patient_provinces():
    conn = get_conn()
    cur = conn.cursor()
    
    print("🔄 Bắt đầu migration thông tin tỉnh bệnh nhân...")
    
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
            
            new_province = get_new_province_from_old(old_province)
            
            if new_province != old_province:
                cur.execute("""
                UPDATE BenhNhan 
                SET Tinh = ?
                WHERE BN_ID = ?
                """, (new_province, bn_id))
                migrated_count += 1
                
                if migrated_count % 50 == 0:
                    success(f"  Đã migration {migrated_count} bệnh nhân...")
            else:
                unchanged_count += 1
                
        except Exception as e:
            error_count += 1
            error(f"  Lỗi migration bệnh nhân {bn_id}: {e}")
    
    conn.commit()
    conn.close()
    
    success(f"Hoàn thành migration:")
    print(f"   - Đã cập nhật: {migrated_count} bệnh nhân")
    print(f"   - Không thay đổi: {unchanged_count} bệnh nhân") 
    print(f"   - Lỗi: {error_count} bệnh nhân")

def run_full_migration():
    print_separator(70,"=")
    try:

        migrate_patient_provinces()
        print()
        
    except Exception as e:
        error(f"Lỗi migration: {e}")
        return False
    
    return True

def check_migration_status():
    conn = get_conn()
    cur = conn.cursor()
    
    try:
        cur.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN Tinh IS NOT NULL AND Tinh != '' THEN 1 ELSE 0 END) as has_province
        FROM BenhNhan
        """)
        
        stats = cur.fetchone()
        total = stats.total
        has_province = stats.has_province
        
        print(f"\nThống kê bệnh nhân:")
        info("   - Tổng số: {total}")
        info("   - Có thông tin tỉnh: {has_province}")
        
    except Exception as e:
        error(f"Lỗi: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_full_migration()