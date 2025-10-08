#!/usr/bin/env python3

import re
from datetime import datetime
from typing import Tuple, Optional
from .qr_utils import phantich_cccd, lay_thongtin_tinhmoi_tu_tinhcu
from .message_utils import error, warning, success, print_separator

def validate_cccd_format(cccd: str) -> Tuple[bool, str]:
    cccd = cccd.strip()
    
    if not cccd:
        return False, "CCCD không được để trống!"
    
    if not cccd.isdigit():
        return False, "CCCD chỉ được chứa số!"
    
    if len(cccd) != 12:
        return False, f"CCCD phải có đúng 12 chữ số! (Hiện tại: {len(cccd)} chữ số)"
    
    return True, ""

def validate_birth_date_format(ngay_sinh: str) -> Tuple[bool, str, str]:
    if not ngay_sinh:
        return False, "Ngày sinh không được để trống!", ""
    
    ngay_sinh = ngay_sinh.strip()
    
    #DD/MM/YYYY 
    if re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', ngay_sinh):
        try:
            parts = ngay_sinh.split('/')
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            
            datetime(year, month, day)
            
            formatted = f"{day:02d}/{month:02d}/{year}"
            return True, "", formatted
        except ValueError:
            return False, f"Ngày sinh không hợp lệ: {ngay_sinh}", ""
    
    #DD-MM-YYYY
    elif re.match(r'^\d{1,2}-\d{1,2}-\d{4}$', ngay_sinh):
        try:
            parts = ngay_sinh.split('-')
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            
            datetime(year, month, day)
            
            formatted = f"{day:02d}/{month:02d}/{year}"
            return True, "", formatted
        except ValueError:
            return False, f"Ngày sinh không hợp lệ: {ngay_sinh}", ""
    
    #DDMMYYYY
    elif re.match(r'^\d{8}$', ngay_sinh):
        try:
            day = int(ngay_sinh[:2])
            month = int(ngay_sinh[2:4])
            year = int(ngay_sinh[4:8])
            
            datetime(year, month, day)
            
            formatted = f"{day:02d}/{month:02d}/{year}"
            return True, "", formatted
        except ValueError:
            return False, f"Ngày sinh không hợp lệ: {ngay_sinh}", ""
    
    #YYYY only
    elif re.match(r'^\d{4}$', ngay_sinh):
        try:
            year = int(ngay_sinh)
            if year < 1900 or year > datetime.now().year:
                return False, f"Năm sinh không hợp lệ: {year}", ""
            
            # Default to January 1st
            formatted = f"01/01/{year}"
            return True, "", formatted
        except ValueError:
            return False, f"Năm sinh không hợp lệ: {ngay_sinh}", ""
    
    else:
        return False, (
            f"Định dạng ngày sinh không đúng: {ngay_sinh}\n"
            "Các định dạng được hỗ trợ:\n"
            "  - DD/MM/YYYY (ví dụ: 15/07/1986)\n"
            "  - DD-MM-YYYY (ví dụ: 15-07-1986)\n"
            "  - DDMMYYYY (ví dụ: 15071986)\n"
            "  - YYYY (ví dụ: 1986)"
        ), ""

def Hien_thi_thong_tin_xac_nhan_benhnhan(ho_ten: str, gioi_tinh: str, ngay_sinh: str, so_cccd: str) -> None:
    print("\n" + "="*60)
    print("           THÔNG TIN BỆNH NHÂN VỪA TạO")
    print_separator(60,"=")
    
    print(f"📱 CCCD: {so_cccd}")
    print(f"👤 Họ tên: {ho_ten}")
    print(f"📅 Ngày sinh: {ngay_sinh}")
    print(f"⚤ Giới tính: {gioi_tinh}")
    
    try:
        nam_sinh = int(ngay_sinh.split('/')[-1])
        print(f"🎂 Năm sinh (tự động): {nam_sinh}")
    except:
        pass
    
    username = f"{so_cccd}"
    print(f"\n🔑 Thông tin đăng nhập được tạo:")
    print(f"   📧 Username: {username}")
    print(f"   🔒 Password: Dựa trên CCCD và ngày sinh(4 số cuối CCCD + ngày sinh (01/11/2025 => 011125))")
    
    print_separator(60,"=")

def nhap_thong_tin_cccd() -> str:
    while True:
        cccd = input("Số CCCD (12 chữ số): ").strip()
        is_valid, error_msg = validate_cccd_format(cccd)
        
        if is_valid:
            return cccd
        else:
            error(error_msg)
            print("Vui lòng nhập lại!")

def nhap_thong_tin_ngaysinh() -> str:
    print("\nCác định dạng ngày sinh được hỗ trợ:")
    print("  - DD/MM/YYYY (ví dụ: 15/07/1986)")
    print("  - DD-MM-YYYY (ví dụ: 15-07-1986)")
    print("  - DDMMYYYY (ví dụ: 15071986)")
    print("  - YYYY (ví dụ: 1986)")
    
    while True:
        ngay_sinh = input("Ngày sinh: ").strip()
        is_valid, error_msg, formatted_date = validate_birth_date_format(ngay_sinh)
        
        if is_valid:
            return formatted_date
        else:
            error(error_msg)
            print("Vui lòng nhập lại!")

def nhap_thong_tin_gioitinh(cccd: str) -> str:
    _, gioitinh_cccd, _, _ = phantich_cccd(cccd)
    
    if gioitinh_cccd:
        print(f"💡 Hệ thống phân tích từ CCCD: Giới tính = {gioitinh_cccd}")
        xac_nhan = input(f"Xác nhận giới tính là '{gioitinh_cccd}'? (y/n): ").strip().lower()
        if not xac_nhan or xac_nhan in ['y', 'yes']:
            return gioitinh_cccd
    
    while True:
        gioi_tinh = input("Giới tính (Nam/Nữ/Khác): ").strip()
        if gioi_tinh in ['Nam', 'Nữ', 'Khác']:
            return gioi_tinh
        else:
            error("Giới tính phải là 'Nam', 'Nữ' hoặc 'Khác'!")
            print("Vui lòng nhập lại!")

def nhap_thong_tin_diachi_tinh(cccd: str) -> str:
    tinh_cu, _, _, tinh_moi = phantich_cccd(cccd)
    recommended_province = tinh_moi if tinh_moi else tinh_cu
    
    if recommended_province:
        print(f"💡 Hệ thống phân tích từ CCCD: Tỉnh/TP = {recommended_province}")
        if tinh_cu and tinh_moi and tinh_cu != tinh_moi:
            print(f"   (Cũ: {tinh_cu} → Mới: {tinh_moi})")
        
        xac_nhan = input(f"Xác nhận tỉnh/TP là '{recommended_province}'? (y/n): ").strip().lower()
        if not xac_nhan or xac_nhan in ['y', 'yes']:
            return recommended_province
    
    while True:
        tinh = input("Tỉnh/Thành phố: ").strip()
        if tinh:
            return tinh
        else:
            error("Tỉnh/Thành phố không được để trống!")
            print("Vui lòng nhập lại!")

def input_gioitinh_with_validation() -> str:
    while True:
        gioi_tinh = input("Giới tính (Nam/Nữ/Khác): ").strip()
        if gioi_tinh in ['Nam', 'Nữ', 'Khác']:
            return gioi_tinh
        else:
            error("Giới tính phải là 'Nam', 'Nữ' hoặc 'Khác'!")
            print("Vui lòng nhập lại!")

def Hien_thi_thong_tin_benhnhan(benh_nhan) -> None:
    print("\n" + "="*60)
    print("           THÔNG TIN BỆNH NHÂN ĐÃ TỒN TẠI")
    print_separator(60,"=")
    
    print(f"📱 CCCD: {benh_nhan.so_cccd}")
    print(f"🆔 Mã BN: {benh_nhan.ma_bn}")
    print(f"📋 PID: {benh_nhan.pid}")
    print(f"👤 Họ tên: {benh_nhan._ho_ten}")
    print(f"⚤ Giới tính: {benh_nhan._gioi_tinh}")
    print(f"🎂 Năm sinh: {benh_nhan.nam_sinh}")

def nhap_thong_tin_hoten() -> str:
    while True:
        ho_ten = input("Họ tên: ").strip()
        if ho_ten:
            return ho_ten
        else:
            error("Họ tên không được để trống!")
            print("Vui lòng nhập lại!")

def nhap_thong_tin_diachi_phuongxa() -> str:
    phuong_xa = input("Phường/Xã (có thể để trống): ").strip()
    return phuong_xa

def display_benh_nhan_summary(benh_nhan) -> None:
    print("\n" + "="*50)
    print("         THÔNG TIN BỆNH NHÂN")
    print_separator(50,"=")
    
    print(f"🆔 Mã BN: {benh_nhan.ma_bn}")
    print(f"📋 PID: {benh_nhan.pid}")
    print(f"👤 Họ tên: {benh_nhan._ho_ten}")
    print(f"⚤ Giới tính: {benh_nhan._gioi_tinh}")
    print(f"🎂 Năm sinh: {benh_nhan.nam_sinh}")
    print(f"📱 CCCD: {benh_nhan.so_cccd}")
    print_separator(50,"=")

def display_reception_summary(tiep_nhan, chi_phi: int) -> None:

    print("\n" + "="*60)
    print("           THÔNG TIN ĐĂNG KÝ TIẾP NHẬN")
    print_separator(60,"=")
    
    print(f"📋 Mã tiếp nhận: {tiep_nhan._ma_tn}")
    print(f"📅 Ngày đăng ký: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    print(f"\n👳 THÔNG TIN BỆNH NHÂN:")
    print(f"   🆔 Mã BN: {tiep_nhan._bn.ma_bn}")
    print(f"   📋 PID: {tiep_nhan._bn.pid}")
    print(f"   👤 Họ tên: {tiep_nhan._bn._ho_ten}")
    print(f"   ⚤ Giới tính: {tiep_nhan._bn._gioi_tinh}")
    print(f"   🎂 Năm sinh: {tiep_nhan._bn.nam_sinh}")
    print(f"   📱 CCCD: {tiep_nhan._bn.so_cccd}")
    
    print(f"\n🩺 THÔNG TIN DỊCH VỤ:")
    if tiep_nhan._dv:
        print(f"   📝 Mã DV: {tiep_nhan._dv._ma_dv}")
        print(f"   💊 Tên DV: {tiep_nhan._dv._ten_dv}")
        print(f"   💰 Giá DV: {tiep_nhan._dv._gia:,}đ")
    else:
        error("Chưa có thông tin dịch vụ")
    
    print(f"\n🏥 THÔNG TIN PHÒNG KHÁM:")
    if tiep_nhan._pk:
        print(f"   🚪 Mã phòng: {tiep_nhan._pk._ma_phong}")
        print(f"   🏥 Tên phòng: {tiep_nhan._pk._ten_phong}")
    else:
         error("Chưa có thông tin phòng khám")
    
    print(f"\n👨‍⚕️ THÔNG TIN BÁC SĨ:")
    if tiep_nhan._bs:
        print(f"   🆔 Mã BS: {tiep_nhan._bs.ma_bs}")
        print(f"   👤 Họ tên: {tiep_nhan._bs.ho_ten}")
        print(f"   🩺 Chuyên khoa: {tiep_nhan._bs.chuyen_khoa}")
    else:
         error("Chưa chọn bác sĩ")
    
    print(f"\n📋 THÔNG TIN KHÁM:")
    print(f"   📝 Lý do khám: {tiep_nhan._ly_do}")
    print(f"   💰 Chi phí tạm tính: {chi_phi:,}đ")
    
    print_separator(60,"=")

def xac_nhan_thong_tin(message: str) -> bool:
    response = input(f"{message} (y/n): ").strip().lower()
    return not response or response in ['y', 'yes']

def input_province_with_validation() -> str:
    while True:
        tinh = input("Tỉnh/Thành phố: ").strip()
        if tinh:
            return tinh
        else:
            error("Tỉnh/Thành phố không được để trống!")
            print("Vui lòng nhập lại!")