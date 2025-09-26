#!/usr/bin/env python3
"""
Module kiểm tra tình trạng migration hành chính (sử dụng từ app.py)
"""

from migration_hanh_chinh import (
    create_admin_tables, 
    populate_admin_data,
    migrate_patient_provinces,
    run_full_migration
)
from qr_utils import get_new_province_from_old
from db import get_conn

def check_migration_status():
    """Kiểm tra tình trạng migration"""
    print("\n📊 TÌNH TRẠNG MIGRATION")
    print("="*40)
    
    conn = get_conn()
    cur = conn.cursor()
    
    try:
        # Kiểm tra các bảng migration đã tồn tại
        cur.execute("""
        SELECT COUNT(*) as table_count
        FROM sysobjects 
        WHERE name IN ('DM_HanhChinhMoi', 'DM_HanhChinhCu', 'DM_HanhChinhMoi_Map_Cu') 
        AND xtype='U'
        """)
        migration_tables = cur.fetchone().table_count
        
        if migration_tables < 3:
            print("❌ Các bảng migration chưa được tạo")
            print("💡 Hãy chạy migration đầy đủ trước")
            return
        
        print("✅ Các bảng migration đã được tạo")
        
        # Thống kê dữ liệu migration
        cur.execute("SELECT COUNT(*) as total FROM DM_HanhChinhMoi")
        new_provinces = cur.fetchone().total
        
        cur.execute("SELECT COUNT(*) as total FROM DM_HanhChinhCu") 
        old_provinces = cur.fetchone().total
        
        cur.execute("SELECT COUNT(*) as total FROM DM_HanhChinhMoi_Map_Cu")
        mappings = cur.fetchone().total
        
        print(f"📊 Dữ liệu hành chính:")
        print(f"   - Tỉnh/TP mới: {new_provinces}")
        print(f"   - Tỉnh/TP cũ: {old_provinces}")
        print(f"   - Mappings: {mappings}")
        
        # Thống kê bệnh nhân
        cur.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN Tinh IS NOT NULL AND Tinh != '' THEN 1 ELSE 0 END) as has_province
        FROM BenhNhan
        """)
        
        stats = cur.fetchone()
        total = stats.total
        has_province = stats.has_province
        
        print(f"\n👥 Thống kê bệnh nhân:")
        print(f"   - Tổng số: {total}")
        print(f"   - Có thông tin tỉnh: {has_province}")
        
        if has_province > 0:
            # Kiểm tra có bao nhiêu bệnh nhân có tỉnh thuộc hành chính mới
            print(f"\n🔍 VÍ DỤ THÔNG TIN TỈNH HIỆN TẠI:")
            cur.execute("""
            SELECT TOP 5 HoTen, Tinh
            FROM BenhNhan 
            WHERE Tinh IS NOT NULL AND Tinh != ''
            ORDER BY created_at DESC
            """)
            
            for row in cur.fetchall():
                print(f"   {row.HoTen}: {row.Tinh}")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        conn.close()

def test_province_mapping():
    """Test mapping tỉnh"""
    print("\n🧪 TEST MAPPING TỈNH")
    print("="*30)
    
    # Test cases
    test_provinces = [
        "Hà Nội", "TP.Hồ Chí Minh", "Hải Phòng", 
        "Hà Giang", "Yên Bái", "Bắc Kạn",
        "Hòa Bình", "Vĩnh Phúc", "Phú Thọ",
        "Bắc Giang", "Thái Bình", "Hưng Yên",
        "Quảng Bình", "Quảng Trị", "Quảng Nam",
        "Bình Dương", "Bà Rịa - Vũng Tàu",
        "Sóc Trăng", "Hậu Giang", "Cần Thơ"
    ]
    
    print("Tỉnh cũ -> Tỉnh mới:")
    for province in test_provinces:
        new_province = get_new_province_from_old(province)
        status = "✅" if new_province != province else "➡️"
        print(f"{status} {province:20} -> {new_province}")
    
    # Test với input người dùng
    print(f"\n💡 TEST THÊM:")
    while True:
        old_name = input("Nhập tên tỉnh cũ (Enter để thoát): ").strip()
        if not old_name:
            break
        new_name = get_new_province_from_old(old_name)
        print(f"   {old_name} -> {new_name}")

if __name__ == "__main__":
    # Nếu chạy trực tiếp file này, hiển thị menu đơn giản
    print("\n🏛️ MIGRATION DỮ LIỆU HÀNH CHÍNH")
    print("="*50)
    print("1. ⚡ Chạy toàn bộ migration")
    print("2. 📋 Kiểm tra tình trạng migration") 
    print("3. 🧪 Test mapping tỉnh")
    print("0. 🔙 Thoát")
    
    while True:
        choice = input("\n👉 Chọn chức năng: ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            confirm = input("Thực hiện migration? (y/N): ").strip().lower()
            if confirm == 'y':
                run_full_migration()
        elif choice == '2':
            check_migration_status()
        elif choice == '3':
            test_province_mapping()
        else:
            print("❌ Lựa chọn không hợp lệ!")
        
        if choice != '0':
            input("\n📋 Nhấn Enter để tiếp tục...")