#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Optional, Tuple
import re
from datetime import datetime
from .message_utils import error, warning, success, info, print_separator


# Mã tỉnh thành phố (cũ - trước sắp xếp hành chính)
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

# Mapping hành chính mới theo NQ 202/2025/QH15
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
    """
    Mapping tỉnh cũ sang tỉnh mới theo NQ 202/2025/QH15
    
    Args:
        old_province: Tên tỉnh cũ
        
    Returns:
        Tên tỉnh mới sau sắp xếp
    """
    if not old_province:
        return old_province
        
    # Kiểm tra tỉnh không đổi
    if old_province in ADMIN_REORGANIZATION['unchanged']:
        return old_province
    
    # Xử lý các trường hợp đặc biệt
    name_mappings = {
        'Hà Nội': 'Thành phố Hà Nội',
        'TP.Hồ Chí Minh': 'Thành phố Hồ Chí Minh',
        'Hải Phòng': 'Thành phố Hải Phòng',
        'Đà Nẵng': 'Thành phố Đà Nẵng',
        'Cần Thơ': 'Thành phố Cần Thơ',
        'Thừa Thiên Huế': 'Thành phố Huế'
    }
    
    mapped_name = name_mappings.get(old_province, old_province)
    if mapped_name in ADMIN_REORGANIZATION['unchanged']:
        return mapped_name
    
    # Tìm trong danh sách sáp nhập
    for merged in ADMIN_REORGANIZATION['merged']:
        if mapped_name in merged['includes']:
            return merged['new']
        # Kiểm tra các biến thể tên
        for include in merged['includes']:
            if (old_province == include or 
                old_province == include.replace('Thành phố ', '') or
                old_province == include.replace('TP.', '') or
                f'Thành phố {old_province}' == include or
                f'TP.{old_province}' == include):
                return merged['new']
    
    return old_province  # Trả về tên cũ nếu không tìm thấy

def analyze_cccd(cccd: str) -> Tuple[Optional[str], Optional[str], Optional[int], Optional[str]]:
    """
    Phân tích số CCCD 12 chữ số để trích xuất thông tin
    
    Args:
        cccd: Số CCCD 12 chữ số (VD: 079215000001)
    
    Returns:
        Tuple[province_old, gender, birth_year, province_new] hoặc (None, None, None, None) nếu không hợp lệ
    """
    if not cccd or len(cccd) != 12 or not cccd.isdigit():
        return None, None, None, None
    
    try:
        # 3 số đầu: mã tỉnh
        province_code = cccd[:3]
        province_old = PROVINCE_CODES.get(province_code)
        
        # Mapping sang tỉnh mới
        province_new = get_new_province_from_old(province_old) if province_old else None
        
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
            return None, None, None, None
        
        # 2 số tiếp theo: năm sinh (2 chữ số cuối)
        year_suffix = int(cccd[4:6])
        birth_year = century_base + year_suffix
        
        return province_old, gender, birth_year, province_new
        
    except (ValueError, IndexError):
        return None, None, None, None

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
        """Convert ngay_sinh to year (automatically extracts from date formats)"""
        try:
            if not self.ngay_sinh:
                return 0
            
            # Handle various date formats
            ngay_sinh_clean = self.ngay_sinh.strip()
            
            # Format 1: DDMMYYYY (8 digits)
            if ngay_sinh_clean.isdigit() and len(ngay_sinh_clean) == 8:
                return int(ngay_sinh_clean[4:8])
            
            # Format 2: DD/MM/YYYY
            if '/' in ngay_sinh_clean and len(ngay_sinh_clean) == 10:
                parts = ngay_sinh_clean.split('/')
                if len(parts) == 3 and parts[2].isdigit() and len(parts[2]) == 4:
                    return int(parts[2])
            
            # Format 3: DD-MM-YYYY
            if '-' in ngay_sinh_clean and len(ngay_sinh_clean) == 10:
                parts = ngay_sinh_clean.split('-')
                if len(parts) == 3 and parts[2].isdigit() and len(parts[2]) == 4:
                    return int(parts[2])
            
            # Format 4: YYYY only (4 digits)
            if ngay_sinh_clean.isdigit() and len(ngay_sinh_clean) == 4:
                return int(ngay_sinh_clean)
            
            # Try to extract 4-digit year from any position in the string
            import re
            year_match = re.search(r'\b(19|20)\d{2}\b', ngay_sinh_clean)
            if year_match:
                return int(year_match.group())
            
            warning(f"Không thể trích xuất năm sinh từ: {ngay_sinh_clean}")
            return 0
            
        except (ValueError, IndexError, AttributeError) as e:
            print(f"Lỗi khi trích xuất năm sinh từ '{self.ngay_sinh}': {e}")
            return 0
    
    def get_formatted_date(self) -> str:
        try:
            if not self.ngay_sinh:
                return ""
            
            ngay_sinh_clean = self.ngay_sinh.strip()
            
            # Format 1: DDMMYYYY (8 digits) -> DD/MM/YYYY
            if ngay_sinh_clean.isdigit() and len(ngay_sinh_clean) == 8:
                day = ngay_sinh_clean[:2]
                month = ngay_sinh_clean[2:4]
                year = ngay_sinh_clean[4:8]
                return f"{day}/{month}/{year}"
            
            # Format 2: DD/MM/YYYY (already formatted)
            if '/' in ngay_sinh_clean and len(ngay_sinh_clean) == 10:
                parts = ngay_sinh_clean.split('/')
                if len(parts) == 3 and len(parts[0]) == 2 and len(parts[1]) == 2 and len(parts[2]) == 4:
                    return ngay_sinh_clean
            
            # Format 3: DD-MM-YYYY -> DD/MM/YYYY
            if '-' in ngay_sinh_clean and len(ngay_sinh_clean) == 10:
                parts = ngay_sinh_clean.split('-')
                if len(parts) == 3 and len(parts[0]) == 2 and len(parts[1]) == 2 and len(parts[2]) == 4:
                    return f"{parts[0]}/{parts[1]}/{parts[2]}"
            
            # Format 4: YYYY only -> 01/01/YYYY (default to Jan 1st)
            if ngay_sinh_clean.isdigit() and len(ngay_sinh_clean) == 4:
                return f"01/01/{ngay_sinh_clean}"
            
            return self.ngay_sinh
            
        except (ValueError, IndexError, AttributeError):
            return self.ngay_sinh

def parse_qr_code(qr_string: str) -> Optional[QRPatientInfo]:
    try:
        parts = qr_string.strip().split('|')
        
        if len(parts) < 3:
            error(f"QR code không đúng định dạng. Cần ít nhất CCCD|CMND|HoTen")
            return None
    
        while len(parts) < 6:
            parts.append('')
        
        cccd = parts[0].strip()
        cmnd = parts[1].strip()
        ho_ten = parts[2].strip()
        ngay_sinh = parts[3].strip() 
        gioi_tinh = parts[4].strip()
        dia_chi = parts[5].strip()
        
        if len(parts) > 6:
            ngay_cap = parts[6].strip()
            info(f"Đã bỏ qua Ngày cấp: {ngay_cap}")
        
        if not re.match(r'^\d{12}$', cccd):
            error(f"CCCD không hợp lệ: {cccd} (phải là 12 chữ số)")
            return None
        
        if not ho_ten:
            error("Họ tên không được để trống")
            return None
        
        extracted_province_old, extracted_gender, extracted_year, extracted_province_new = analyze_cccd(cccd)
        
        if not gioi_tinh and extracted_gender:
            gioi_tinh = extracted_gender
            success(f"Phân tích CCCD: Giới tính = {gioi_tinh}")
        
        if not ngay_sinh and extracted_year:
            ngay_sinh = str(extracted_year)
            success(f"Phân tích CCCD: Năm sinh = {extracted_year}")
        
        if not dia_chi and extracted_province_new:
            dia_chi = extracted_province_new
            success(f"Phân tích CCCD: Tỉnh/TP = {extracted_province_new} (mới)")
        elif not dia_chi and extracted_province_old:
            dia_chi = extracted_province_old
            success(f"Phân tích CCCD: Tỉnh/TP = {extracted_province_old} (cũ)")
        
        if gioi_tinh and gioi_tinh not in ['Nam', 'Nữ']:
            error(f"Giới tính không hợp lệ: {gioi_tinh} (phải là 'Nam' hoặc 'Nữ')")
            return None
        
        if ngay_sinh:
            valid_formats = [
                r'^\d{8}$',          # DDMMYYYY
                r'^\d{4}$',          # YYYY
                r'^\d{2}/\d{2}/\d{4}$',  # DD/MM/YYYY
                r'^\d{2}-\d{2}-\d{4}$'   # DD-MM-YYYY
            ]
            if not any(re.match(pattern, ngay_sinh) for pattern in valid_formats):
                error(f"Ngày sinh không hợp lệ: {ngay_sinh} (phải là DDMMYYYY, DD/MM/YYYY, DD-MM-YYYY hoặc YYYY)")
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
        error(f"Lỗi khi phân tích QR code: {e}")
        return None

def display_patient_info(qr_info: QRPatientInfo) -> None:
    print("\n" + "="*60)
    print("           THÔNG TIN BỆNH NHÂN TỪ QR CODE")
    print_separator(60,"=")
    
    print(f"📱 CCCD: {qr_info.cccd}")
    if qr_info.cmnd:
        print(f"📇 CMND: {qr_info.cmnd}")
    else:
        print("📇 CMND: (không có)")
    
    print(f"👤 Họ tên: {qr_info.ho_ten}")
    
    if qr_info.ngay_sinh:
        formatted_date = qr_info.get_formatted_date()
        nam_sinh = qr_info.get_nam_sinh()
        print(f"📅 Ngày sinh: {formatted_date}")
        if nam_sinh > 0:
            print(f"🎂 Năm sinh (tự động): {nam_sinh}")
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
    province_old, gender, birth_year, province_new = analyze_cccd(qr_info.cccd)
    if province_old:
        print(f"   🗺️  Nơi khai sinh (cũ): {province_old}")
    if province_new:
        print(f"   🗺️  Nơi khai sinh (mới): {province_new}")
    if gender:
        print(f"   👫 Giới tính (theo CCCD): {gender}")
    if birth_year:
        print(f"   🎂 Năm sinh (theo CCCD): {birth_year}")
    
    print_separator(60,"=")

def generate_username_from_qr(qr_info: QRPatientInfo) -> str:
    return f"BN{qr_info.cccd[-6:]}"

def generate_password_from_qr(qr_info: QRPatientInfo) -> str:
    return qr_info.ngay_sinh
