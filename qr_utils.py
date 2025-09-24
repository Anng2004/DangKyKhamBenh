#!/usr/bin/env python3
"""QR Code utilities for patient registration with CCCD analysis"""

from dataclasses import dataclass
from typing import Optional, Tuple
import re
from datetime import datetime

# Mã tỉnh thành phố
PROVINCE_CODES = {
    '001': 'Hà Nội',
    '002': 'Hà Giang', '004': 'Cao Bằng', '006': 'Bắc Kạn', '008': 'Tuyên Quang',
    '010': 'Lào Cai', '011': 'Điện Biên', '012': 'Lai Châu', '014': 'Sơn La',
    '015': 'Yên Bái', '017': 'Hoà Bình', '019': 'Thái Nguyên', '020': 'Lạng Sơn',
    '022': 'Quảng Ninh', '024': 'Bắc Giang', '025': 'Phú Thọ', '026': 'Vĩnh Phúc',
    '027': 'Bắc Ninh', '030': 'Hải Dương', '031': 'Hải Phòng', '033': 'Hưng Yên',
    '034': 'Thái Bình', '035': 'Hà Nam', '036': 'Nam Định', '037': 'Ninh Bình',
    '038': 'Thanh Hóa', '040': 'Nghệ An', '042': 'Hà Tĩnh', '044': 'Quảng Bình',
    '045': 'Quảng Trị', '046': 'Thừa Thiên Huế', '048': 'Đà Nẵng', '049': 'Quảng Nam',
    '051': 'Quảng Ngãi', '052': 'Bình Định', '054': 'Phú Yên', '056': 'Khánh Hòa',
    '058': 'Ninh Thuận', '060': 'Bình Thuận', '062': 'Kon Tum', '064': 'Gia Lai',
    '066': 'Đắk Lắk', '067': 'Đắk Nông', '068': 'Lâm Đồng', '070': 'Bình Phước',
    '072': 'Tây Ninh', '074': 'Bình Dương', '075': 'Đồng Nai', '077': 'Bà Rịa - Vũng Tàu',
    '079': 'TP.Hồ Chí Minh', '080': 'Long An', '082': 'Tiền Giang', '083': 'Bến Tre',
    '084': 'Trà Vinh', '086': 'Vĩnh Long', '087': 'Đồng Tháp', '089': 'An Giang',
    '091': 'Kiên Giang', '092': 'Cần Thơ', '093': 'Hậu Giang', '094': 'Sóc Trăng',
    '095': 'Bạc Liêu', '096': 'Cà Mau'
}

def analyze_cccd(cccd: str) -> Tuple[Optional[str], Optional[str], Optional[int]]:
    """
    Phân tích số CCCD 12 chữ số để trích xuất thông tin
    
    Args:
        cccd: Số CCCD 12 chữ số (VD: 079215000001)
    
    Returns:
        Tuple[province, gender, birth_year] hoặc (None, None, None) nếu không hợp lệ
    """
    if not cccd or len(cccd) != 12 or not cccd.isdigit():
        return None, None, None
    
    try:
        # 3 số đầu: mã tỉnh
        province_code = cccd[:3]
        province = PROVINCE_CODES.get(province_code)
        
        # Số thứ 4: mã giới tính và thế kỷ
        gender_code = cccd[3]
        if gender_code == '0':      # Nam thế kỷ 20
            gender = 'Nam'
            century_base = 1900
        elif gender_code == '1':    # Nữ thế kỷ 20
            gender = 'Nữ'
            century_base = 1900
        elif gender_code == '2':    # Nam thế kỷ 21
            gender = 'Nam'
            century_base = 2000
        elif gender_code == '3':    # Nữ thế kỷ 21
            gender = 'Nữ'
            century_base = 2000
        else:
            return None, None, None
        
        # 2 số tiếp theo: năm sinh (2 chữ số cuối)
        year_suffix = int(cccd[4:6])
        birth_year = century_base + year_suffix
        
        return province, gender, birth_year
        
    except (ValueError, IndexError):
        return None, None, None

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
            elif self.ngay_sinh.isdigit() and len(self.ngay_sinh) == 4:
                return int(self.ngay_sinh)
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
            elif self.ngay_sinh.isdigit() and len(self.ngay_sinh) == 4:
                return f"01/01/{self.ngay_sinh}"  # Default to Jan 1st if only year
            return self.ngay_sinh
        except:
            return self.ngay_sinh

def parse_qr_code(qr_string: str) -> Optional[QRPatientInfo]:
    """
    Parse QR code string to extract patient information
    
    Supports multiple formats:
    1. Full format: "CCCD|CMND|HoTen|NgaySinh|GioiTinh|DiaChi"
    2. Minimal format: "CCCD||HoTen|||DiaChi" (auto-extract from CCCD)
    
    Example: "058186000028|2345678|Nguyễn Thị Test|15071986|Nữ|Ninh Thuận"
    """
    try:
        # Split the QR string by pipe character
        parts = qr_string.strip().split('|')
        
        if len(parts) < 3:
            print(f"❌ QR code không đúng định dạng. Cần ít nhất CCCD|CMND|HoTen")
            return None
        
        # Pad parts to 6 elements if needed
        while len(parts) < 6:
            parts.append('')
        
        cccd = parts[0].strip()
        cmnd = parts[1].strip()
        ho_ten = parts[2].strip()
        ngay_sinh = parts[3].strip() 
        gioi_tinh = parts[4].strip()
        dia_chi = parts[5].strip()
        
        # Validate CCCD (should be 12 digits)
        if not re.match(r'^\d{12}$', cccd):
            print(f"❌ CCCD không hợp lệ: {cccd} (phải là 12 chữ số)")
            return None
        
        if not ho_ten:
            print("❌ Họ tên không được để trống")
            return None
        
        # Auto-extract information from CCCD if missing
        extracted_province, extracted_gender, extracted_year = analyze_cccd(cccd)
        
        # Use extracted gender if not provided in QR
        if not gioi_tinh and extracted_gender:
            gioi_tinh = extracted_gender
            print(f"✅ Phân tích CCCD: Giới tính = {gioi_tinh}")
        
        # Use extracted year if birth date not provided
        if not ngay_sinh and extracted_year:
            ngay_sinh = str(extracted_year)
            print(f"✅ Phân tích CCCD: Năm sinh = {extracted_year}")
        
        # Use extracted province for address if address is empty
        if not dia_chi and extracted_province:
            dia_chi = extracted_province
            print(f"✅ Phân tích CCCD: Tỉnh/TP = {extracted_province}")
        
        # Validate final data
        if gioi_tinh and gioi_tinh not in ['Nam', 'Nữ']:
            print(f"❌ Giới tính không hợp lệ: {gioi_tinh} (phải là 'Nam' hoặc 'Nữ')")
            return None
        
        # Validate birth date if provided (should be 8 digits DDMMYYYY or 4 digits YYYY)
        if ngay_sinh:
            if not (re.match(r'^\d{8}$', ngay_sinh) or re.match(r'^\d{4}$', ngay_sinh)):
                print(f"❌ Ngày sinh không hợp lệ: {ngay_sinh} (phải là DDMMYYYY hoặc YYYY)")
                return None
        
        return QRPatientInfo(
            cccd=cccd,
            cmnd=cmnd,  # CMND có thể để trống
            ho_ten=ho_ten,
            ngay_sinh=ngay_sinh or '',
            gioi_tinh=gioi_tinh or '',
            dia_chi=dia_chi or ''
        )
        
    except Exception as e:
        print(f"❌ Lỗi khi phân tích QR code: {e}")
        return None

def display_patient_info(qr_info: QRPatientInfo) -> None:
    """Display patient information for confirmation"""
    print("\n" + "="*60)
    print("           THÔNG TIN BỆNH NHÂN TỪ QR CODE")
    print("="*60)
    
    # Hiển thị thông tin cơ bản
    print(f"📱 CCCD: {qr_info.cccd}")
    if qr_info.cmnd:
        print(f"📇 CMND: {qr_info.cmnd}")
    else:
        print("📇 CMND: (không có)")
    
    print(f"👤 Họ tên: {qr_info.ho_ten}")
    
    if qr_info.ngay_sinh:
        print(f"📅 Ngày sinh: {qr_info.get_formatted_date()}")
    else:
        print("📅 Ngày sinh: (không có)")
    
    if qr_info.gioi_tinh:
        print(f"⚤ Giới tính: {qr_info.gioi_tinh}")
    else:
        print("⚤ Giới tính: (không có)")
    
    if qr_info.dia_chi:
        print(f"🏠 Địa chỉ: {qr_info.dia_chi}")
    else:
        print("🏠 Địa chỉ: (không có)")
    
    # Hiển thị thông tin phân tích từ CCCD
    print("\n📊 PHÂN TÍCH CCCD:")
    province, gender, birth_year = analyze_cccd(qr_info.cccd)
    if province:
        print(f"   🗺️  Nơi khai sinh: {province}")
    if gender:
        print(f"   👫 Giới tính (theo CCCD): {gender}")
    if birth_year:
        print(f"   🎂 Năm sinh (theo CCCD): {birth_year}")
    
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
    # Test cases for QR code parsing with CCCD analysis
    
    print("🧪 Testing QR code parsing with CCCD analysis...")
    print("\n" + "="*80)
    
    # Test Case 1: Full QR code format
    print("TEST 1: QR đầy đủ thông tin")
    test_qr1 = "079215000001||Nguyễn Văn Test|15072015|Nam|TP.Hồ Chí Minh"
    qr_info1 = parse_qr_code(test_qr1)
    if qr_info1:
        display_patient_info(qr_info1)
    
    print("\n" + "="*80)
    
    # Test Case 2: Minimal QR code (auto-extract from CCCD)
    print("TEST 2: QR tối thiểu, tự phân tích từ CCCD")  
    test_qr2 = "058186000028||Nguyễn Thị Linh|||"
    qr_info2 = parse_qr_code(test_qr2)
    if qr_info2:
        display_patient_info(qr_info2)
    
    print("\n" + "="*80)
    
    # Test Case 3: CCCD analysis only
    print("TEST 3: Phân tích trực tiếp số CCCD")
    cccd_examples = [
        "079215000001",  # TP.HCM, Nam, 2015
        "058186000028",  # Ninh Thuận, Nữ, 1986  
        "001195000123",  # Hà Nội, Nữ, 1995 (chữ số thứ 4 = 1)
        "031302000456"   # Hải Phòng, Nữ, 2002 (chữ số thứ 4 = 3)
    ]
    
    for cccd in cccd_examples:
        province, gender, birth_year = analyze_cccd(cccd)
        print(f"CCCD {cccd}: {province}, {gender}, {birth_year}")
    
    print("\n✅ Hoàn thành test!")
    print("\nHướng dẫn sử dụng:")
    print("- QR đầy đủ: CCCD|CMND|HoTen|NgaySinh|GioiTinh|DiaChi")
    print("- QR tối thiểu: CCCD||HoTen|||")
    print("- Hệ thống sẽ tự động phân tích CCCD để bổ sung thông tin thiếu")