#!/usr/bin/env python3
"""
cập nhật dữ liệu hành chính sát nhập (NQ 202/2025/QH15)
"""

import json
from db import get_conn
from datetime import datetime
from utils.message_utils import error, success, warning, info, print_separator

# Dữ liệu sắp xếp hành chính theo NQ 202/2025/QH15
THONG_TIN_SAT_NHAP = {
    "sat_nhap": [
        {"Don_vi_moi": "Tuyên Quang", "don_vi_truoc_sat_nhap": ["Hà Giang", "Tuyên Quang"]},
        {"Don_vi_moi": "Lào Cai", "don_vi_truoc_sat_nhap": ["Lào Cai", "Yên Bái"]},
        {"Don_vi_moi": "Thái Nguyên", "don_vi_truoc_sat_nhap": ["Bắc Kạn", "Thái Nguyên"]},
        {"Don_vi_moi": "Phú Thọ", "don_vi_truoc_sat_nhap": ["Hòa Bình", "Vĩnh Phúc", "Phú Thọ"]},
        {"Don_vi_moi": "Bắc Ninh", "don_vi_truoc_sat_nhap": ["Bắc Giang", "Bắc Ninh"]},
        {"Don_vi_moi": "Hưng Yên", "don_vi_truoc_sat_nhap": ["Thái Bình", "Hưng Yên"]},
        {"Don_vi_moi": "Thành phố Hải Phòng", "don_vi_truoc_sat_nhap": ["Hải Dương", "Thành phố Hải Phòng"]},
        {"Don_vi_moi": "Ninh Bình", "don_vi_truoc_sat_nhap": ["Hà Nam", "Ninh Bình", "Nam Định"]},
        {"Don_vi_moi": "Quảng Trị", "don_vi_truoc_sat_nhap": ["Quảng Bình", "Quảng Trị"]},
        {"Don_vi_moi": "Thành phố Đà Nẵng", "don_vi_truoc_sat_nhap": ["Quảng Nam", "Thành phố Đà Nẵng"]},
        {"Don_vi_moi": "Quảng Ngãi", "don_vi_truoc_sat_nhap": ["Quảng Ngãi", "Kon Tum"]},
        {"Don_vi_moi": "Gia Lai", "don_vi_truoc_sat_nhap": ["Gia Lai", "Bình Định"]},
        {"Don_vi_moi": "Đắk Lắk", "don_vi_truoc_sat_nhap": ["Phú Yên", "Đắk Lắk"]},
        {"Don_vi_moi": "Khánh Hòa", "don_vi_truoc_sat_nhap": ["Khánh Hòa", "Ninh Thuận"]},
        {"Don_vi_moi": "Lâm Đồng", "don_vi_truoc_sat_nhap": ["Đắk Nông", "Lâm Đồng", "Bình Thuận"]},
        {"Don_vi_moi": "Thành phố Hồ Chí Minh", "don_vi_truoc_sat_nhap": ["Bình Dương", "Thành phố Hồ Chí Minh", "Bà Rịa - Vũng Tàu"]},
        {"Don_vi_moi": "Đồng Nai", "don_vi_truoc_sat_nhap": ["Bình Phước", "Đồng Nai"]},
        {"Don_vi_moi": "Tây Ninh", "don_vi_truoc_sat_nhap": ["Long An", "Tây Ninh"]},
        {"Don_vi_moi": "Thành phố Cần Thơ", "don_vi_truoc_sat_nhap": ["Sóc Trăng", "Hậu Giang", "Thành phố Cần Thơ"]},
        {"Don_vi_moi": "Vĩnh Long", "don_vi_truoc_sat_nhap": ["Bến Tre", "Vĩnh Long", "Trà Vinh"]},
        {"Don_vi_moi": "Đồng Tháp", "don_vi_truoc_sat_nhap": ["Tiền Giang", "Đồng Tháp"]},
        {"Don_vi_moi": "Cà Mau", "don_vi_truoc_sat_nhap": ["Bạc Liêu", "Cà Mau"]},
        {"Don_vi_moi": "An Giang", "don_vi_truoc_sat_nhap": ["Kiên Giang", "An Giang"]}
    ],
    "giu_nguyen": [
        "Thành phố Hà Nội", "Cao Bằng", "Điện Biên", "Hà Tĩnh",
        "Lai Châu", "Lạng Sơn", "Nghệ An", "Quảng Ninh",
        "Thanh Hóa", "Sơn La", "Thành phố Huế"
    ]
}

def lay_thongtin_tinhmoi_tu_tinhcu(don_vi_hanh_chinh_cu: str) -> str:
    if don_vi_hanh_chinh_cu in THONG_TIN_SAT_NHAP['giu_nguyen']:
        return don_vi_hanh_chinh_cu
    
    for sat_nhap in THONG_TIN_SAT_NHAP['sat_nhap']:
        if don_vi_hanh_chinh_cu in sat_nhap['don_vi_truoc_sat_nhap']:
            return sat_nhap['Don_vi_moi']
    
    ten_day_du = {
        'Hà Nội': 'Thành phố Hà Nội',
        'TP.Hồ Chí Minh': 'Thành phố Hồ Chí Minh',
        'Hải Phòng': 'Thành phố Hải Phòng',
        'Đà Nẵng': 'Thành phố Đà Nẵng',
        'Cần Thơ': 'Thành phố Cần Thơ',
        'Thừa Thiên Huế': 'Thành phố Huế'
    }
    
    if don_vi_hanh_chinh_cu in ten_day_du:
        return ten_day_du[don_vi_hanh_chinh_cu]
    
    for sat_nhap in THONG_TIN_SAT_NHAP['sat_nhap']:
        for include in sat_nhap['don_vi_truoc_sat_nhap']:
            if (don_vi_hanh_chinh_cu == include or 
                don_vi_hanh_chinh_cu == include.replace('Thành phố ', '') or
                don_vi_hanh_chinh_cu == include.replace('TP.', '')):
                return sat_nhap['Don_vi_moi']
    
    return don_vi_hanh_chinh_cu

def CapNhat_BenhNhan_DonviHanhChinh():
    conn = get_conn()
    cur = conn.cursor()
    
    print("🔄 Bắt đầu cập nhật thông tin tỉnh - bệnh nhân...")
    
    cur.execute("SELECT BN_ID, Tinh FROM BenhNhan WHERE Tinh IS NOT NULL AND Tinh != ''")
    benh_nhans = cur.fetchall()
    
    SoLuong_CapNhat = 0
    SoLuong_KhongThayDoi = 0
    SoLuong_Loi = 0
    
    print(f"📊 Tìm thấy {len(benh_nhans)} bệnh nhân có thông tin tỉnh")
    
    for benh_nhan in benh_nhans:
        try:
            bn_id = benh_nhan.BN_ID
            don_vi_hanh_chinh_cu = benh_nhan.Tinh.strip()
            
            don_vi_hanh_chinh_moi = lay_thongtin_tinhmoi_tu_tinhcu(don_vi_hanh_chinh_cu)
            
            if don_vi_hanh_chinh_moi != don_vi_hanh_chinh_cu:
                cur.execute("""
                UPDATE BenhNhan 
                SET Tinh = ?
                WHERE BN_ID = ?
                """, (don_vi_hanh_chinh_moi, bn_id))
                SoLuong_CapNhat += 1
                
                if SoLuong_CapNhat % 50 == 0:
                    success(f"  Đã cập nhật {SoLuong_CapNhat} bệnh nhân...")
            else:
                SoLuong_KhongThayDoi += 1
                
        except Exception as e:
            SoLuong_Loi += 1
            error(f"  Lỗi cập nhật bệnh nhân {bn_id}: {e}")
    
    conn.commit()
    conn.close()
    
    success(f"Hoàn thành cập nhật:")
    print(f"   - Đã cập nhật: {SoLuong_CapNhat} bệnh nhân")
    print(f"   - Không thay đổi: {SoLuong_KhongThayDoi} bệnh nhân") 
    print(f"   - Lỗi: {SoLuong_Loi} bệnh nhân")

def cap_nhat_tatca():
    print_separator(70,"=")
    try:

        CapNhat_BenhNhan_DonviHanhChinh()
        print()
        
    except Exception as e:
        error(f"Lỗi Cập Nhật: {e}")
        return False
    
    return True

def kiemtra_trangthai_capnhat():
    conn = get_conn()
    cur = conn.cursor()
    
    try:
        cur.execute("""
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN Tinh IS NOT NULL AND Tinh != '' THEN 1 ELSE 0 END) as co_tinh
        FROM BenhNhan
        """)
        
        stats = cur.fetchone()
        total = stats.total
        co_tinh = stats.co_tinh
        
        print(f"\nThống kê bệnh nhân:")
        info("   - Tổng số: {total}")
        info("   - Có thông tin tỉnh: {co_tinh}")
        
    except Exception as e:
        error(f"Lỗi: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    cap_nhat_tatca()