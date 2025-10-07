
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from utils.message_utils import error, success, warning, info

# ===== Abstracts =====
class AbsEntity(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

    def print_obj(self) -> None:
        print(str(self))


# ===== Nghiệp vụ =====
class User(AbsEntity):
    def __init__(self, user_id: str, username: str, role: str):
        self._user_id = user_id
        self._username = username
        self._role = role

    def __str__(self) -> str:
        return f"[User: id={self._user_id}, username={self._username}, role={self._role}]"

    @property
    def user_id(self) -> str: return self._user_id


class PhongKham(AbsEntity):
    def __init__(self, pk_id: str, ma_phong: str, ten_phong: str, bac_si: Optional['BacSi'] = None):
        self._pk_id = pk_id
        self._ma_phong = ma_phong
        self._ten_phong = ten_phong
        self._bac_si = bac_si
        self.ten_bac_si = None  # Will be set by repository when needed for backward compatibility

    def __str__(self) -> str:
        if self._bac_si:
            return f"[PhongKham: {self._ma_phong} - {self._ten_phong} - BS: {self._bac_si.ho_ten}]"
        elif hasattr(self, 'ten_bac_si') and self.ten_bac_si:
            return f"[PhongKham: {self._ma_phong} - {self._ten_phong} - BS: {self.ten_bac_si}]"
        else:
            return f"[PhongKham: {self._ma_phong} - {self._ten_phong}]"

    @property
    def pk_id(self) -> str: return self._pk_id
    @property
    def ma_phong(self) -> str: return self._ma_phong
    @property
    def ten_phong(self) -> str: return self._ten_phong
    @property
    def bac_si(self) -> Optional['BacSi']: return self._bac_si


class DichVu(AbsEntity):
    def __init__(self, dv_id: str, ma_dv: str, ten_dv: str, gia: int):
        self._dv_id = dv_id
        self._ma_dv = ma_dv
        self._ten_dv = ten_dv
        self._gia = gia

    def __str__(self) -> str:
        return f"[DichVu: {self._ma_dv} - {self._ten_dv} : {self._gia:,}đ]"

    @property
    def dv_id(self) -> str: return self._dv_id
    @property
    def ma_dv(self) -> str: return self._ma_dv
    @property
    def ten_dv(self) -> str: return self._ten_dv
    @property
    def gia(self) -> int: return self._gia


class BacSi(AbsEntity):
    def __init__(self, bs_id: str, ma_bs: str, ho_ten: str, chuyen_khoa: str = "", so_dt: str = "", email: str = ""):
        self._bs_id = bs_id
        self._ma_bs = ma_bs
        self._ho_ten = ho_ten
        self._chuyen_khoa = chuyen_khoa
        self._so_dt = so_dt
        self._email = email

    def __str__(self) -> str:
        return f"[BacSi: {self._ma_bs} - {self._ho_ten} - {self._chuyen_khoa}]"

    @property
    def bs_id(self) -> str: return self._bs_id
    @property
    def ma_bs(self) -> str: return self._ma_bs
    @property
    def ho_ten(self) -> str: return self._ho_ten
    @property
    def chuyen_khoa(self) -> str: return self._chuyen_khoa
    @property
    def so_dt(self) -> str: return self._so_dt
    @property
    def email(self) -> str: return self._email


class BenhNhan(AbsEntity):
    def __init__(self, bn_id: str, ma_bn: str, pid: str, ho_ten: str, gioi_tinh: str, nam_sinh: int, so_cccd: str):
        self._bn_id = bn_id
        self._ma_bn = ma_bn
        self._pid = pid
        self._ho_ten = ho_ten
        self._gioi_tinh = gioi_tinh
        self._nam_sinh = nam_sinh
        self._so_cccd = so_cccd

    def __str__(self) -> str:
        return f"[BenhNhan: {self._ma_bn} - PID:{self._pid} - {self._ho_ten} - {self._gioi_tinh} - {self._nam_sinh} - CCCD:{self._so_cccd}]"

    @property
    def bn_id(self) -> str: return self._bn_id
    @property
    def ma_bn(self) -> str: return self._ma_bn
    @property
    def pid(self) -> str: return self._pid
    @property
    def so_cccd(self) -> str: return self._so_cccd
    @property
    def nam_sinh(self) -> int: return self._nam_sinh
    @property
    def ho_ten(self) -> str: return self._ho_ten
    @property
    def gioi_tinh(self) -> str: return self._gioi_tinh
    
    @staticmethod
    def lay_nam_sinh(ngay_sinh_str: str) -> int:
        """lấy năm sinh từ chuỗi ngày sinh với các định dạng khác nhau.
        Hỗ trợ các định dạng:"""
        try:
            if not ngay_sinh_str:
                return 0
            
            ngay_sinh_clean = ngay_sinh_str.strip()
            
            # Format 1: DDMMYYYY (8 ký tự, không dấu phân cách)
            if ngay_sinh_clean.isdigit() and len(ngay_sinh_clean) == 8:
                return int(ngay_sinh_clean[4:8])
            
            # Format 2: DD/MM/YYYY (dấu phân cách '/')
            if '/' in ngay_sinh_clean and len(ngay_sinh_clean) == 10:
                parts = ngay_sinh_clean.split('/')
                if len(parts) == 3 and parts[2].isdigit() and len(parts[2]) == 4:
                    return int(parts[2])
            
            # Format 3: DD-MM-YYYY (dấu phân cách '-')
            if '-' in ngay_sinh_clean and len(ngay_sinh_clean) == 10:
                parts = ngay_sinh_clean.split('-')
                if len(parts) == 3 and parts[2].isdigit() and len(parts[2]) == 4:
                    return int(parts[2])
            
            # Format 4: YYYY only (4 ký tự)
            if ngay_sinh_clean.isdigit() and len(ngay_sinh_clean) == 4:
                return int(ngay_sinh_clean)
            
            # Tìm 4 ký tự liên tiếp bắt đầu bằng 19xx hoặc 20xx trong chuỗi
            import re
            year_match = re.search(r'\b(19|20)\d{2}\b', ngay_sinh_clean)
            if year_match:
                return int(year_match.group())
            
            return 0
            
        except (ValueError, IndexError, AttributeError):
            return 0


class TiepNhan(AbsEntity):
    def __init__(self, tn_id: str, ma_tn: str, bn: BenhNhan, ly_do: str, dv: DichVu, pk: PhongKham, bs: Optional[BacSi] = None, created_at: str = ""):
        self._tn_id = tn_id
        self._ma_tn = ma_tn
        self._bn = bn
        self._ly_do = ly_do
        self._dv = dv
        self._pk = pk
        self._bs = bs
        self._created_at = created_at

    def __str__(self) -> str:
        bs_info = f" | BS: {self._bs.ma_bs}-{self._bs.ho_ten} ({self._bs.chuyen_khoa})" if self._bs else " | BS: Chưa chọn"
        dv_info = f"{self._dv._ma_dv}-{self._dv._ten_dv} ({self._dv._gia:,}đ)" if self._dv else "Chưa chọn dịch vụ"
        pk_info = f"{self._pk._ma_phong}-{self._pk._ten_phong}" if self._pk else "Chưa chọn phòng khám"
        date_info = f" | Ngày: {self._created_at[:10]}" if self._created_at else ""
        return (f"[TiepNhan: {self._ma_tn} | BN: {self._bn.ma_bn}-{self._bn._ho_ten} ({self._bn._gioi_tinh}, {self._bn._nam_sinh}) | "
                f"DV: {dv_info} | PK: {pk_info}{bs_info} | Lý do: {self._ly_do}{date_info}]")

    @property
    def tn_id(self) -> str: return self._tn_id
    @property  
    def ma_tn(self) -> str: return self._ma_tn
    @property
    def bac_si(self) -> Optional[BacSi]: return self._bs
    @property
    def created_at(self) -> str: return self._created_at

# ===== Domain service =====
class ChiPhiKham:
    """Tính chi phí dựa trên dịch vụ."""
    @staticmethod
    def tinh_chi_phi(dv: DichVu, pk: PhongKham) -> int:
        # Chỉ tính chi phí dịch vụ, không có phụ phí
        return dv.gia
