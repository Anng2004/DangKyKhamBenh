#!/usr/bin/env python3
"""QR Code utilities for patient registration"""

from dataclasses import dataclass
from typing import Optional
import re
from datetime import datetime

@dataclass
class QRPatientInfo:
    """Data class for patient information from QR code"""
    cccd: str
    cmnd: str
    ho_ten: str
    ngay_sinh: str
    gioi_tinh: str
    dia_chi: str
    
    def get_nam_sinh(self) -> int:
        """Convert ngay_sinh (DDMMYYYY) to year"""
        try:
            if len(self.ngay_sinh) == 8:
                return int(self.ngay_sinh[4:8])
            return 0
        except:
            return 0
    
    def get_formatted_date(self) -> str:
        """Convert ngay_sinh to formatted date string"""
        try:
            if len(self.ngay_sinh) == 8:
                day = self.ngay_sinh[:2]
                month = self.ngay_sinh[2:4]
                year = self.ngay_sinh[4:8]
                return f"{day}/{month}/{year}"
            return self.ngay_sinh
        except:
            return self.ngay_sinh

def parse_qr_code(qr_string: str) -> Optional[QRPatientInfo]:
    """
    Parse QR code string to extract patient information
    
    Format: "CCCD|CMND|HoTen|NgaySinh|GioiTinh|DiaChi"
    Example: "0580xxxxxxxxx|2xxxxxx|Nguyễn Văn An|20041999|Nam|Quận 2, Hồ Chí Minh"
    """
    try:
        # Split the QR string by pipe character
        parts = qr_string.strip().split('|')
        
        if len(parts) != 6:
            print(f"❌ QR code không đúng định dạng. Cần 6 phần tử, nhận được {len(parts)}")
            return None
        
        # Validate CCCD (should be 12 digits)
        cccd = parts[0].strip()
        if not re.match(r'^\d{12}$', cccd):
            print(f"❌ CCCD không hợp lệ: {cccd} (phải là 12 chữ số)")
            return None
        
        # Validate birth date (should be 8 digits DDMMYYYY)
        ngay_sinh = parts[3].strip()
        if not re.match(r'^\d{8}$', ngay_sinh):
            print(f"❌ Ngày sinh không hợp lệ: {ngay_sinh} (phải là DDMMYYYY)")
            return None
            
        # Validate gender
        gioi_tinh = parts[4].strip()
        if gioi_tinh not in ['Nam', 'Nữ']:
            print(f"❌ Giới tính không hợp lệ: {gioi_tinh} (phải là 'Nam' hoặc 'Nữ')")
            return None
        
        return QRPatientInfo(
            cccd=cccd,
            cmnd=parts[1].strip(),
            ho_ten=parts[2].strip(),
            ngay_sinh=ngay_sinh,
            gioi_tinh=gioi_tinh,
            dia_chi=parts[5].strip()
        )
        
    except Exception as e:
        print(f"❌ Lỗi khi phân tích QR code: {e}")
        return None

def display_patient_info(qr_info: QRPatientInfo) -> None:
    """Display patient information for confirmation"""
    print("\n" + "="*60)
    print("           THÔNG TIN BỆNH NHÂN TỪ QR CODE")
    print("="*60)
    print(f"📱 CCCD: {qr_info.cccd}")
    print(f"📇 CMND: {qr_info.cmnd}")
    print(f"👤 Họ tên: {qr_info.ho_ten}")
    print(f"📅 Ngày sinh: {qr_info.get_formatted_date()}")
    print(f"⚤ Giới tính: {qr_info.gioi_tinh}")
    print(f"🏠 Địa chỉ: {qr_info.dia_chi}")
    print("="*60)

def generate_username_from_qr(qr_info: QRPatientInfo) -> str:
    """Generate username from QR patient info"""
    # Use last 6 digits of CCCD as username
    return f"BN{qr_info.cccd[-6:]}"

def generate_password_from_qr(qr_info: QRPatientInfo) -> str:
    """Generate password from QR patient info"""
    # Use birth date as password for simplicity
    return qr_info.ngay_sinh

if __name__ == "__main__":
    # Test the parsing function
    test_qr = "0580xxxxxxxxx|2xxxxxx|Nguyễn Văn An|20041999|Nam|Quận 2, Hồ Chí Minh"
    
    print("🧪 Testing QR code parsing...")
    qr_info = parse_qr_code(test_qr)
    
    if qr_info:
        display_patient_info(qr_info)
        print(f"\n🔑 Username: {generate_username_from_qr(qr_info)}")
        print(f"🔒 Password: {generate_password_from_qr(qr_info)}")
        print("✅ QR parsing test successful!")
    else:
        print("❌ QR parsing test failed!")